from django import forms


class TextForm(forms.Form):
  entry = forms.CharField(
    label="", 
    widget=forms.TextInput(attrs={'id': 'entry-field'})
  )