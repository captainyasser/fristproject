# departments/views.py
from rest_framework import generics, permissions
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Department
from .serializers import DepartmentSerializer
from rest_framework.authtoken.models import Token

# كلاس مخصص للتحكم في الصلاحيات
class StaffOnlyForWrite(permissions.BasePermission):
    def has_permission(self, request, view):
        # العرض (GET) متاح لأي مستخدم مسجل
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return request.user.is_authenticated
        # الإضافة، التعديل، الحذف (POST, PUT, DELETE) للـ staff بس
        return request.user.is_authenticated and request.user.is_staff

# عرض كل الأقسام وإضافة قسم جديد (API)
class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [StaffOnlyForWrite]  # عرض للكل، تعديل للـ staff

# عرض قسم معين وتعديله وحذفه (API)
class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'id'
    permission_classes = [StaffOnlyForWrite]  # عرض للكل، تعديل للـ staff

# عرض صفحة الأقسام (Template)
class DepartmentsPage(LoginRequiredMixin, View):
    def get(self, request):
        token, created = Token.objects.get_or_create(user=request.user)  # جلب أو إنشاء التوكن
        return render(request, 'departments/departments.html', {'token': token.key})