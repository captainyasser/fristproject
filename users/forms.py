from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser  # استيراد نموذج المستخدم المخصص
from institutes.models import Institute

class CustomUserForm(UserCreationForm):
    institute = forms.ModelChoiceField(queryset=Institute.objects.all(), required=True, label="المعهد")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'institute']
