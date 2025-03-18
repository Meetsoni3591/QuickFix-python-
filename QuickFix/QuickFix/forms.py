# myapp/forms.py
from django import forms
from .models import ServiceDetail

class EmailForm(forms.Form):
    email = forms.EmailField()

class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceDetail
        fields = [
            'category', 'area', 'avilable', 'price', 'experience', 'desc', 'service_image'
        ]