from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Tips, CustomUser

class TipForm(forms.ModelForm):
    class Meta:
        model = Tips
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'style': 'width: 100%;',
                'placeholder': 'Share your tip here...',
            }),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']