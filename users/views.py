from django.shortcuts import render, redirect
from users.forms import CustomUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # ضروري فقط لو فيه استثناء لـ CSRF

def add_user(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # يفضل تغييره لاحقاً لاسم واضح
    else:
        form = CustomUserForm()
    return render(request, 'users/add_user.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
            if is_ajax:
                return JsonResponse({'token': token.key})
            return redirect('home')
        else:
            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
            if is_ajax:
                return JsonResponse({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}, status=400)
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect('login')


# @login_required
# def home(request):
#     return render(request, 'adminlte/index.html')