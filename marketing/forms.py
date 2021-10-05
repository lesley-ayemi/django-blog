from django import forms
# from django.forms import fields, widge
from .models import SignUp

class SubscribeForm(forms.ModelForm):
    email = forms.EmailField(label='', 
    widget=forms.EmailInput(
        attrs={'placeholder':'Enter your email'}
        ))
    class Meta:
        model = SignUp
        fields = ['email']

    def clean_email(self, *args, **kwargs):
        self.cleaned_data.get("email")
        qs = SignUp.objects.filter(email__iexact=email)
        if qs.exists(): 
            print('exists')
            raise forms.ValidationError('This email already exists')
        return email