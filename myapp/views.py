
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.decorators import login_required


# @login_required
# def home(request):
#     return render(request, 'adminlte/index.html')



# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('home')  # إعادة التوجيه إذا كان المستخدم مسجلاً بالفعل

#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')  # تغيير الصفحة بعد تسجيل الدخول
#         else:
#             messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")

#     return render(request, "login.html")




# def custom_login_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
            
#             # توجيه المستخدم إلى الصفحة المطلوبة بعد تسجيل الدخول
#             next_url = request.GET.get('next') or 'home'
#             return redirect(next_url)
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})







# def logout_view(request):
#     logout(request)
#     return redirect('')  # العودة إلى صفحة تسجيل الدخول بعد تسجيل الخروج




# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user) 
#             return redirect('/')
#     else:
#         form = UserCreationForm()
    
#     return render(request, 'register.html', {'form': form})
