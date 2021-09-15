from aboutme.models import Biography
from django import forms
from django import forms

class BioForm(forms.ModelForm):
    class Meta:
        model = Biography
        fields = '__all__'
        
