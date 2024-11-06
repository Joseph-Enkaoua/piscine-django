from django import forms
from .models import Tips

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



# from django import forms
# from .models import *


# class RegisterForm(forms.ModelForm):
#   username = forms.CharField(widget=forms.TextInput(attrs={'id': 'entry-field'}), max_length=150, help_text="Enter a username")
#   password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'entry-field'}), help_text="Enter a password", max_length=128)
#   verify_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'entry-field'}), help_text="Re-enter your password", max_length=128)

#   class Meta:
#     model = CostumUser
#     fields = ['username']

#   def clean(self):
#     cleaned_data = super().clean()
#     username = cleaned_data.get('username')
#     password = cleaned_data.get('password')
#     verify_password = cleaned_data.get('verify_password')
#     if CostumUser.objects.filter(username=username).exists():
#       self.add_error('username', 'Username already exists')
#     elif password != verify_password:
#       self.add_error('verify_password', 'Passwords do not match')
#     return cleaned_data
  
#   def save(self, commit=True):
#     user = super().save(commit=False)
#     user.set_password(self.cleaned_data['password'])
#     if commit:
#       user.save()
#     return user
