from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TaskFile
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def task_list(request):
    if request.method == 'POST':
        if 'title' in request.POST:
            title = request.POST.get('title')
            due_date = request.POST.get('due_date')
            repeat_type = request.POST.get('repeat_type')
            repeat_interval = request.POST.get('repeat_interval', 1)
            reminder_days = request.POST.get('reminder_days', 0)
            notes = request.POST.get('notes')
            try:
                repeat_interval = int(repeat_interval)
                reminder_days = int(reminder_days)
            except ValueError:
                repeat_interval = 1
                reminder_days = 0
            task = Task.objects.create(
                title=title,
                due_date=due_date,
                repeat_type=repeat_type,
                repeat_interval=repeat_interval,
                reminder_days=reminder_days,
                notes=notes
            )
            files = request.FILES.getlist('files')
            for file in files:
                TaskFile.objects.create(task=task, file=file)
            return redirect('tasks:task_list')

    filter_status = request.GET.get('filter', 'pending')
    if filter_status == 'completed':
        tasks = Task.objects.filter(is_completed=True).order_by('-due_date')
    else:
        tasks = Task.objects.filter(is_completed=False).order_by('due_date')
    
    tasks_json = json.dumps(
        [{
            'id': task.id,
            'title': task.title,
            'due_date': task.due_date.strftime('%Y-%m-%d'),
            'reminder_date': (task.due_date - timedelta(days=task.reminder_days)).strftime('%Y-%m-%d') if task.reminder_days > 0 else None,
            'reminder_days': task.reminder_days,
            'notified': False
        } for task in tasks],
        cls=DjangoJSONEncoder
    )
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'tasks_json': tasks_json,
        'filter_status': filter_status
    })

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for file in files:
            TaskFile.objects.create(task=task, file=file)
        return redirect('tasks:task_detail', task_id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.repeat_type == 'none':
        for file in task.files.all():
            file.file.delete()
        task.delete()
    else:
        task.is_completed = True
        task.save()
        new_due_date = task.due_date
        if task.repeat_type == 'daily':
            new_due_date += timedelta(days=task.repeat_interval)
        elif task.repeat_type == 'monthly':
            new_due_date += relativedelta(months=task.repeat_interval)
        elif task.repeat_type == 'quarterly':
            new_due_date += relativedelta(months=task.repeat_interval * 3)
        new_task = Task.objects.create(
            title=task.title,
            due_date=new_due_date,
            repeat_type=task.repeat_type,
            repeat_interval=task.repeat_interval,
            reminder_days=task.reminder_days,
            notes=task.notes
        )
        for file in task.files.all():
            TaskFile.objects.create(task=new_task, file=file.file)
    return redirect('tasks:task_list')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.due_date = request.POST.get('due_date')
        task.repeat_type = request.POST.get('repeat_type')
        task.repeat_interval = int(request.POST.get('repeat_interval', 1))
        task.reminder_days = int(request.POST.get('reminder_days', 0))
        task.notes = request.POST.get('notes')
        task.save()
        files = request.FILES.getlist('files')
        for file in files:
            TaskFile.objects.create(task=task, file=file)
        return redirect('tasks:task_list')
    return render(request, 'tasks/edit_task.html', {'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    for file in task.files.all():
        file.file.delete()
    task.delete()
    return redirect('tasks:task_list')

def delete_file(request, file_id):
    file = get_object_or_404(TaskFile, id=file_id)
    file.file.delete()
    file.delete()
    return redirect('tasks:task_detail', task_id=file.task.id)

def get_notifications(request):
    today = date.today()
    
    # 1. التنبيهات التي مر تاريخها ولم تكتم (للصوت والتحذير)
    overdue_unmuted = Task.objects.filter(
        due_date__lt=today, 
        is_completed=False, 
        is_muted=False
    )
    
    # 2. التنبيهات المستحقة التنفيذ (للشريط المتحرك والقائمة)
    # تشمل: المتأخرة، ومستحقة اليوم، والتي اقترب موعدها حسب reminder_days
    pending_tasks = Task.objects.filter(is_completed=False).order_by('due_date')
    
    notifications = []
    marquee_messages = []
    
    for task in pending_tasks:
        is_overdue = task.due_date < today
        is_due_today = task.due_date == today
        is_due_soon = False
        
        if task.reminder_days > 0:
            reminder_date = task.due_date - timedelta(days=task.reminder_days)
            if reminder_date <= today < task.due_date:
                is_due_soon = True
        
        # إضافة للتنبيهات إذا كان مستحق أو متأخر أو اقترب موعده
        if is_overdue or is_due_today or is_due_soon:
            notif_type = 'overdue' if is_overdue else ('today' if is_due_today else 'soon')
            
            notifications.append({
                'id': task.id,
                'title': task.title,
                'due_date': task.due_date.strftime('%Y-%m-%d'),
                'is_overdue': is_overdue,
                'is_muted': task.is_muted,
                'type': notif_type
            })
            
            # الشريط المتحرك يعرض فقط المستحقة للتنفيذ (اليوم أو متأخرة)
            if (is_overdue or is_due_today) and not task.is_completed:
                status_text = "متأخرة" if is_overdue else "مستحقة اليوم"
                marquee_messages.append({
                    'text': f"{task.title} ({status_text})",
                    'type': notif_type,
                    'id': task.id
                })

    return JsonResponse({
        'notifications': notifications,
        'marquee_items': marquee_messages, # Changed from marquee_text
        'has_urgent_sound': overdue_unmuted.exists(),
        'unread_count': len(notifications)
    })

@csrf_exempt 
@require_POST
def mute_notification(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_muted = True
    task.save()
    return JsonResponse({'success': True})