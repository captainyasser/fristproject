import os
from django.contrib.auth.decorators import login_required
import subprocess
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Database settings (better to move these to settings.py)
DB_NAME = "yasser"
DB_USER = "root"
DB_PASSWORD = ""
BACKUP_DIR = os.path.join(settings.MEDIA_ROOT, "backups")

# Ensure backup directory exists
os.makedirs(BACKUP_DIR, exist_ok=True)

def create_backup():
    """Helper function to create database backup."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{DB_NAME}_backup_{timestamp}.sql"
    filepath = os.path.join(BACKUP_DIR, filename)

    command = f"mysqldump -u {DB_USER} --password={DB_PASSWORD} {DB_NAME} > {filepath}"
    subprocess.run(command, shell=True)
    return filename

@login_required(login_url='/login/')
def backup_database(request):
    """Create a new database backup."""
    create_backup()
    return redirect("backup_page")

@login_required(login_url='/login/')
def restore_database(request, filename):
    """Restore database from backup file."""
    filepath = os.path.join(BACKUP_DIR, filename)
    command = f"mysql -u {DB_USER} --password={DB_PASSWORD} {DB_NAME} < {filepath}"
    subprocess.run(command, shell=True)
    return redirect("backup_page")

@login_required(login_url='/login/')
def delete_backup(request, filename):
    """Delete a backup file."""
    filepath = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect("backup_page")

@login_required(login_url='/login/')
def bulk_delete_backup(request):
    """Delete multiple backup files."""
    if request.method == "POST":
        filenames = request.POST.getlist("selected_backups")
        for filename in filenames:
            filepath = os.path.join(BACKUP_DIR, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
    return redirect("backup_page")

@login_required(login_url='/login/')
def download_backup(request, filename):
    """Download a backup file."""
    filepath = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
    return redirect("backup_page")

@login_required(login_url='/login/')
def upload_backup(request):
    """Upload a backup file."""
    if request.method == "POST" and request.FILES.get("backup_file"):
        uploaded_file = request.FILES["backup_file"]
        fs = FileSystemStorage(location=BACKUP_DIR)
        fs.save(uploaded_file.name, uploaded_file)
    return redirect("backup_page")

@login_required(login_url='/login/')
def backup_page(request):
    """Display backup management page."""
    backups = sorted(os.listdir(BACKUP_DIR), key=lambda f: os.path.getctime(os.path.join(BACKUP_DIR, f)), reverse=True)
    return render(request, "backup/backup.html", {"backups": backups})