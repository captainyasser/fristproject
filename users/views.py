from django.shortcuts import render, redirect
from users.forms import CustomUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def add_user(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # استبدله بالصفحة التي تعرض المستخدمين
    else:
        form = CustomUserForm()
    return render(request, 'users/add_user.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # إعادة التوجيه إذا كان المستخدم مسجلاً بالفعل

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # تغيير الصفحة بعد تسجيل الدخول
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('')  # العودة إلى صفحة تسجيل الدخول بعد تسجيل الخروج



@login_required
def home(request):
    return render(request, 'adminlte/index.html')