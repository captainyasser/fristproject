from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta

def task_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')  # تنسيق: YYYY-MM-DD
        repeat = request.POST.get('repeat')
        Task.objects.create(
            title=title,
            due_date=due_date,
            repeat=repeat
        )
        return redirect('task_list')
    
    tasks = Task.objects.filter(is_completed=False)
    # حساب وقت التذكير تلقائيًا لكل مهمة
    tasks_json = json.dumps(
        [{'id': task.id, 
          'title': task.title, 
          'due_date': task.due_date.strftime('%Y-%m-%d'), 
          'reminder_date': (task.due_date - timedelta(days=2)).strftime('%Y-%m-%d') if task.repeat in ['monthly', 'quarterly'] else None} 
         for task in tasks],
        cls=DjangoJSONEncoder
    )
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'tasks_json': tasks_json})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.repeat == 'none':
        task.delete()
    else:
        task.is_completed = True
        task.save()
        new_due_date = task.due_date
        if task.repeat == 'daily':
            new_due_date += timedelta(days=1)
        elif task.repeat == 'monthly':
            new_due_date += timedelta(days=30)
        elif task.repeat == 'quarterly':
            new_due_date += timedelta(days=90)
        Task.objects.create(
            title=task.title,
            due_date=new_due_date,
            repeat=task.repeat
        )
    return redirect('task_list')