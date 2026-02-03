# F:\emapi-edit\myproject\penalties\views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import PenaltyLevel, PenaltyApplied, ViolationCategory, ViolationType, PenaltyRecord, ViolationPreset, PenaltyAmount
from .forms import PenaltyLevelForm, PenaltyAppliedForm, ViolationCategoryForm, ViolationTypeForm, PenaltyRecordForm, ViolationPresetForm, PenaltyAmountForm
from django.db.models import Count
from django.http import JsonResponse 
from datetime import date
import json

class PenaltiesDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'penalties/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['penalty_count'] = PenaltyRecord.objects.count()
        context['type_count'] = ViolationType.objects.count()
        context['category_count'] = ViolationCategory.objects.count()
        context['latest_penalties'] = PenaltyRecord.objects.order_by('-created_at')[:5]
        return context

# Penalty Levels
class PenaltyLevelListView(LoginRequiredMixin, ListView):
    model = PenaltyLevel
    template_name = 'penalties/level_list.html'
    context_object_name = 'levels'

class PenaltyLevelCreateView(LoginRequiredMixin, CreateView):
    model = PenaltyLevel
    form_class = PenaltyLevelForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:level_list')
    extra_context = {'title': 'إضافة نوع جزاء', 'header': 'إدارة أنواع الجزاءات'}

class PenaltyLevelUpdateView(LoginRequiredMixin, UpdateView):
    model = PenaltyLevel
    form_class = PenaltyLevelForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:level_list')
    extra_context = {'title': 'تعديل نوع جزاء', 'header': 'إدارة أنواع الجزاءات'}

class PenaltyLevelDeleteView(LoginRequiredMixin, DeleteView):
    model = PenaltyLevel
    template_name = 'penalties/confirm_delete.html'
    success_url = reverse_lazy('penalties:level_list')

# Penalty Applied
class PenaltyAppliedListView(LoginRequiredMixin, ListView):
    model = PenaltyApplied
    template_name = 'penalties/applied_list.html'
    context_object_name = 'applied_penalties'

class PenaltyAppliedCreateView(LoginRequiredMixin, CreateView):
    model = PenaltyApplied
    form_class = PenaltyAppliedForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:applied_list')
    extra_context = {'title': 'إضافة جزاء موقع', 'header': 'إدارة الجزاءات الموقعة'}

class PenaltyAppliedUpdateView(LoginRequiredMixin, UpdateView):
    model = PenaltyApplied
    form_class = PenaltyAppliedForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:applied_list')
    extra_context = {'title': 'تعديل جزاء موقع', 'header': 'إدارة الجزاءات الموقعة'}

class PenaltyAppliedDeleteView(LoginRequiredMixin, DeleteView):
    model = PenaltyApplied
    template_name = 'penalties/confirm_delete.html'
    success_url = reverse_lazy('penalties:applied_list')

# Violation Categories
class ViolationCategoryListView(LoginRequiredMixin, ListView):
    model = ViolationCategory
    template_name = 'penalties/category_list.html'
    context_object_name = 'categories'

class ViolationCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ViolationCategory
    form_class = ViolationCategoryForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:category_list')
    extra_context = {'title': 'إضافة تصنيف مخالفة', 'header': 'إدارة تصنيفات المخالفات'}

class ViolationCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ViolationCategory
    form_class = ViolationCategoryForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:category_list')
    extra_context = {'title': 'تعديل تصنيف مخالفة', 'header': 'إدارة تصنيفات المخالفات'}

class ViolationCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = ViolationCategory
    template_name = 'penalties/confirm_delete.html'
    success_url = reverse_lazy('penalties:category_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.violation_types.exists():
             messages.error(request, "لا يمكن حذف هذا التصنيف لأنه مرتبط بأنواع مخالفات.")
             return redirect('penalties:category_list')
        if PenaltyRecord.objects.filter(category=self.object).exists():
             messages.error(request, "لا يمكن حذف هذا التصنيف لأنه مرتبط بسجلات جزاءات.")
             return redirect('penalties:category_list')
        return super().delete(request, *args, **kwargs)

# Violation Types
class ViolationTypeListView(LoginRequiredMixin, ListView):
    model = ViolationType
    template_name = 'penalties/type_list.html'
    context_object_name = 'types'

class ViolationTypeCreateView(LoginRequiredMixin, CreateView):
    model = ViolationType
    form_class = ViolationTypeForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:type_list')
    extra_context = {'title': 'إضافة نوع مخالفة', 'header': 'إدارة أنواع المخالفات'}

class ViolationTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = ViolationType
    form_class = ViolationTypeForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:type_list')
    extra_context = {'title': 'تعديل نوع مخالفة', 'header': 'إدارة أنواع المخالفات'}

class ViolationTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = ViolationType
    template_name = 'penalties/confirm_delete.html'
    success_url = reverse_lazy('penalties:type_list')

# Penalty Records
class PenaltyRecordListView(LoginRequiredMixin, ListView):
    model = PenaltyRecord
    template_name = 'penalties/record_list.html'
    context_object_name = 'records'
    ordering = ['-penalty_date']
    
    def get_queryset(self):
        qs = super().get_queryset()
        employee_id = self.request.GET.get('employee_id')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        category_id = self.request.GET.get('category_id')
        
        if employee_id:
             qs = qs.filter(employee__id=employee_id)
        if date_from:
             qs = qs.filter(penalty_date__gte=date_from)
        if date_to:
             qs = qs.filter(penalty_date__lte=date_to)
        if category_id:
             qs = qs.filter(category__id=category_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ViolationCategory.objects.all()
        return context

class PenaltyRecordCreateView(LoginRequiredMixin, CreateView):
    model = PenaltyRecord
    form_class = PenaltyRecordForm
    template_name = 'penalties/record_form.html'
    success_url = reverse_lazy('penalties:record_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass extra data for JS
        context['violation_types'] = json.dumps(list(ViolationType.objects.values('id', 'name', 'category_id', 'description_template', 'is_absence')))
        context['penalty_applied_list'] = json.dumps(list(PenaltyApplied.objects.values('id', 'penalty_level_id', 'name')))
        context['penalty_levels'] = json.dumps(list(PenaltyLevel.objects.values('id', 'name')))
        context['violation_presets'] = json.dumps(list(ViolationPreset.objects.filter(is_active=True).values('id', 'name', 'text', 'violation_type_id')))
        context['penalty_amounts'] = json.dumps(list(PenaltyAmount.objects.filter(is_active=True).values('id', 'name', 'penalty_applied_id', 'penalty_applied__penalty_level_id')))
        return context

class PenaltyRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = PenaltyRecord
    form_class = PenaltyRecordForm
    template_name = 'penalties/record_form.html'
    success_url = reverse_lazy('penalties:record_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass extra data for JS
        context['violation_types'] = json.dumps(list(ViolationType.objects.values('id', 'name', 'category_id', 'description_template', 'is_absence')))
        context['penalty_applied_list'] = json.dumps(list(PenaltyApplied.objects.values('id', 'penalty_level_id', 'name')))
        context['penalty_levels'] = json.dumps(list(PenaltyLevel.objects.values('id', 'name')))
        context['violation_presets'] = json.dumps(list(ViolationPreset.objects.filter(is_active=True).values('id', 'name', 'text', 'violation_type_id')))
        context['penalty_amounts'] = json.dumps(list(PenaltyAmount.objects.filter(is_active=True).values('id', 'name', 'penalty_applied_id', 'penalty_applied__penalty_level_id')))
        return context
    

class PenaltyRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = PenaltyRecord
    template_name = 'penalties/confirm_delete.html'
    success_url = reverse_lazy('penalties:record_list')

# Violation Presets
class ViolationPresetListView(LoginRequiredMixin, ListView):
    model = ViolationPreset
    template_name = 'penalties/preset_list.html'
    context_object_name = 'presets'

class ViolationPresetCreateView(LoginRequiredMixin, CreateView):
    model = ViolationPreset
    form_class = ViolationPresetForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:preset_list')
    extra_context = {'title': 'إضافة نص مخالفة جاهز', 'header': 'إدارة نصوص المخالفات الجاهزة'}

class ViolationPresetUpdateView(LoginRequiredMixin, UpdateView):
    model = ViolationPreset
    form_class = ViolationPresetForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:preset_list')
    extra_context = {'title': 'تعديل نص مخالفة', 'header': 'إدارة نصوص المخالفات الجاهزة'}

class ViolationPresetDeleteView(LoginRequiredMixin, DeleteView):
    model = ViolationPreset
    template_name = 'penalties/confirm_delete.html'
    success_url = reverse_lazy('penalties:preset_list')

# Penalty Extract Report
class PenaltyExtractView(LoginRequiredMixin, TemplateView):
    template_name = 'penalties/penalty_extract.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_id = self.kwargs.get('employee_id')
        
        from em_data.models import Employee
        employee = get_object_or_404(Employee, id=employee_id)
        penalties = PenaltyRecord.objects.filter(employee=employee).order_by('penalty_date')
        
        context['employee'] = employee
        context['penalties'] = penalties
        context['total_penalties'] = penalties.count()
        
        return context

# Penalty Extract Select Employee
class PenaltyExtractSelectView(LoginRequiredMixin, TemplateView):
    template_name = 'penalties/penalty_extract_select.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from em_data.models import Employee
        
        # Get employees who have penalties
        employees_with_penalties = Employee.objects.filter(
            penalties__isnull=False
        ).distinct().order_by('name')
        
        context['employees'] = employees_with_penalties
        return context



from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import PenaltyAmount # Moved to top
# from .forms import PenaltyAmountForm # Moved to top

# =========================
# Penalty Amount Views
# =========================

class PenaltyAmountListView(LoginRequiredMixin, ListView):
    model = PenaltyAmount
    template_name = 'penalties/amount_list.html'
    context_object_name = 'amounts'

class PenaltyAmountCreateView(LoginRequiredMixin, CreateView):
    model = PenaltyAmount
    form_class = PenaltyAmountForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:amount_list')
    extra_context = {'title': 'إضافة مقدار جزاء', 'header': 'إدارة مقادير الجزاءات'}

class PenaltyAmountUpdateView(LoginRequiredMixin, UpdateView):
    model = PenaltyAmount
    form_class = PenaltyAmountForm
    template_name = 'penalties/form.html'
    success_url = reverse_lazy('penalties:amount_list')
    extra_context = {'title': 'تعديل مقدار جزاء', 'header': 'إدارة مقادير الجزاءات'}

class PenaltyAmountDeleteView(LoginRequiredMixin, DeleteView):
    model = PenaltyAmount
    template_name = 'penalties/confirm_delete.html'
    success_url = reverse_lazy('penalties:amount_list')
