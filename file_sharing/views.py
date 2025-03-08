from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from urllib.parse import quote
from .models import SharedFile
from .forms import FileForm
import os


@login_required(login_url='/login/')
def file_share(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            SharedFile.objects.create(file=file, user=request.user)
            messages.success(request, 'تم رفع الملفات بنجاح!')
            return redirect('file_share')
        else:
            messages.error(request, 'حدث خطأ أثناء رفع الملفات: ' + str(form.errors))  # Show form errors
    
    files = SharedFile.objects.filter(user=request.user)
    form = FileForm()
    return render(request, 'file_sharing/file_share.html', {'files': files, 'form': form})



@login_required(login_url='/login/')
def download_file(request, file_id):
    file = get_object_or_404(SharedFile, id=file_id)
    # Optional: Restrict download to file owner
    if file.user != request.user:
        messages.error(request, 'غير مسموح لك بتحميل هذا الملف.')
        return redirect('file_share')
    
    file_name = os.path.basename(file.file.name)
    encoded_file_name = quote(file_name)
    response = FileResponse(file.file, as_attachment=True, filename=file_name)
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_file_name}'
    return response

@login_required(login_url='/login/')
def delete_files(request, file_id):
    file = get_object_or_404(SharedFile, id=file_id)
    # Restrict deletion to file owner
    if file.user != request.user:
        messages.error(request, 'غير مسموح لك بحذف هذا الملف.')
        return redirect('file_share')
    
    file.file.delete()  # Delete file from storage
    file.delete()       # Delete record from database
    messages.success(request, 'تم حذف الملف بنجاح!')
    return redirect('file_share')