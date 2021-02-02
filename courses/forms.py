from .models import Course, Module
from django.forms.models import inlineformset_factory
from django import forms
ModuleFormSet = inlineformset_factory(
    Course, Module, fields=['name', 'description'], 
    extra=2, can_delete=True, 
    widgets={
        'name': forms.TextInput(attrs={'placeholder': 'Module Name', 'class': 'form-control'}),
        'description': forms.Textarea(attrs={'placeholder': 'Module Overview', 'class': 'form-control'})
        })


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username or Email', 'class': 'form-control'}))
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))