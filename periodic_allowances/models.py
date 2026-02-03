# E:\yasser\emapi2025\myproject\periodic_allowances\models.py
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from decimal import Decimal
from em_data.models import Employee
from ranks.models import Rank
from tarkyat.models import Promotion  # import للترقيات


class PeriodicAllowance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='periodic_allowances', verbose_name="الموظف")
    allowance_year = models.IntegerField(verbose_name="العام", help_text="العام الذي تُمنح فيه العلاوة (مثل 2025)")
    stored_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="القيمة المخزنة", help_text="القيمة المدخلة يدويًا أو تلقائيًا")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "علاوة دورية"
        verbose_name_plural = "العلاوات الدورية"
        unique_together = ['employee', 'allowance_year']  # تجنب التكرار لنفس الموظف والعام
        ordering = ['-allowance_year']

    def __str__(self):
        stored_display = self.stored_value if self.stored_value is not None else "غير محدد"
        return f"{self.employee.name} - {self.allowance_year}: {stored_display} جنيه"

    def clean(self):
        # التحقق من عدم وجود قيمة سلبية (إذا كانت موجودة)
        if self.stored_value is not None and self.stored_value < 0:
            raise ValidationError("القيمة لا يمكن أن تكون سلبية.")

    @staticmethod
    def get_allowance_date(year):
        """تحديد تاريخ العلاوة الدقيق لعام معين"""
        if year in [2023, 2024]:
            return datetime(year, 4, 1).date()  # 1/4
        else:
            return datetime(year, 7, 1).date()  # 1/7 (افتراضي، بما في ذلك 2025 فصاعدًا)

    @staticmethod
    def get_rank_at_date(employee, target_date):
        """حساب الدرجة الفعالة في تاريخ معين (آخر ترقية قبل التاريخ، fallback للدرجة الحالية)"""
        promotion = Promotion.objects.filter(
            employee=employee,
            promotion_date__lte=target_date
        ).order_by('-promotion_date').first()
        rank = promotion.to_rank if promotion else employee.rank
        return rank.name if rank else 'غير محدد'

    @staticmethod
    def get_calculated_value(employee, target_date=None):
        """حساب القيمة الديناميكية بناءً على الدرجة في التاريخ المحدد والتاريخ"""
        if not target_date:
            target_date = datetime.now().date()
        
        # حساب الدرجة في هذا التاريخ
        rank_name = PeriodicAllowance.get_rank_at_date(employee, target_date)
        
        if not rank_name:
            return Decimal('0.00')
        
        # قيم قديمة (قبل 1/7/2012)
        old_values = {
            'أمين شرطة ممتاز أول': Decimal('5.5'),
            'أمين شرطة ممتاز ثان': Decimal('5'),
            'أمين شرطة ممتاز': Decimal('4'),
            'أمين شرطة أول': Decimal('3'),
            'أمين شرطة ثان': Decimal('3'),
            'أمين شرطة ثالث': Decimal('3'),
            'مساعد شرطة ممتاز': Decimal('5'),
            'مساعد شرطة أول': Decimal('4'),
            'مساعد شرطة ثان': Decimal('3'),
            'مساعد شرطة ثالث': Decimal('3'),
            'مراقب شرطة ممتاز': Decimal('2.5'),
            'مراقب شرطة أول': Decimal('2'),
            'مراقب شرطة ثان': Decimal('1.5'),
            'مراقب شرطة ثالث': Decimal('1.5'),
            'مندوب شرطة ممتاز': Decimal('2'),
            'مندوب شرطة أول': Decimal('1.5'),
            'مندوب شرطة ثان': Decimal('1.5'),
            'مندوب شرطة ثالث': Decimal('1.5'),
            'رقيب أول': Decimal('2'),
            'رقيب': Decimal('1.5'),
            'عريف': Decimal('1.5'),
            'جندي': Decimal('1.5'),
            'معاون أمن ممتاز أول': Decimal('2'),
            'معاون أمن ممتاز ثان': Decimal('1.5'),
            'معاون أمن ممتاز': Decimal('1.5'),
            'معاون أمن أول': Decimal('1.5'),
            'معاون أمن ثان': Decimal('1.5'),
            'معاون أمن ثالث': Decimal('1.5'),
        }
        
        # قيم جديدة (بعد 1/7/2012)
        new_values = {
            'أمين شرطة ممتاز أول': Decimal('30'),
            'أمين شرطة ممتاز ثان': Decimal('25'),
            'أمين شرطة ممتاز': Decimal('20'),
            'أمين شرطة أول': Decimal('17'),
            'أمين شرطة ثان': Decimal('13'),
            'أمين شرطة ثالث': Decimal('10'),
            'مساعد شرطة ممتاز': Decimal('25'),
            'مساعد شرطة أول': Decimal('17'),
            'مساعد شرطة ثان': Decimal('13'),
            'مساعد شرطة ثالث': Decimal('10'),
            'مراقب شرطة ممتاز': Decimal('20'),
            'مراقب شرطة أول': Decimal('17'),
            'مراقب شرطة ثان': Decimal('13'),
            'مراقب شرطة ثالث': Decimal('10'),
            'مندوب شرطة ممتاز': Decimal('17'),
            'مندوب شرطة أول': Decimal('13'),
            'مندوب شرطة ثان': Decimal('13'),
            'مندوب شرطة ثالث': Decimal('10'),
            'رقيب أول': Decimal('10'),
            'رقيب': Decimal('9'),
            'عريف': Decimal('8'),
            'جندي': Decimal('7'),
            'معاون أمن ممتاز أول': Decimal('10'),
            'معاون أمن ممتاز ثان': Decimal('9'),
            'معاون أمن ممتاز': Decimal('8'),
            'معاون أمن أول': Decimal('7'),
            'معاون أمن ثان': Decimal('7'),
            'معاون أمن ثالث': Decimal('7'),
        }
        
        change_date = datetime(2012, 7, 1).date()
        if target_date >= change_date:  # التغيير بناءً على تاريخ العلاوة، لا التعيين
            value = new_values.get(rank_name, Decimal('0.00'))
        else:
            value = old_values.get(rank_name, Decimal('0.00'))
        
        return value

    def is_eligible(self, target_date=None):
        """التحقق من الأهلية: عام كامل من التعيين قبل تاريخ العلاوة، لم يتقاعد"""
        if not target_date:
            target_date = self.get_allowance_date(self.allowance_year)
        
        if not self.employee.date_of_appointment:
            return False
        
        # تحقق مرور عام كامل قبل تاريخ العلاوة
        one_year_after_appointment = self.employee.date_of_appointment + timedelta(days=365)
        if target_date < one_year_after_appointment:
            return False
        
        # حساب تاريخ التقاعد المتوقع
        if self.employee.date_of_birth:
            retirement_date = self.employee.date_of_birth + timedelta(days=60*365.25)  # تقريبي لـ 60 عام
            if target_date > retirement_date:
                return False
        
        return True

    @property
    def allowance_date(self):
        """تاريخ العلاوة الدقيق لهذا السجل"""
        return self.get_allowance_date(self.allowance_year)

    @property
    def difference(self):
        """الفرق بين المحسوبة والمخزنة للعرض"""
        calculated = PeriodicAllowance.get_calculated_value(self.employee)
        stored = self.stored_value if self.stored_value is not None else Decimal('0.00')
        return calculated - stored

    @property
    def has_difference(self):
        """هل هناك فرق؟ للتصميم"""
        return self.difference != 0