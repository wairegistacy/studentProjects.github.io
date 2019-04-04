from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class NewProjectForm(forms.ModelForm):
    topic = forms.CharField(max_length=255, required=True, help_text='Required.')
    firstParticipant = forms.CharField(max_length=255, required=True, help_text='Required')
    level = forms.CharField(widget=forms.Select(), max_length=255, required=True)
    schoolName = forms.CharField(max_length=255, required=True, help_text='Required.')
    secondParticipant = forms.CharField(max_length=255, required=True, help_text='Required.')
    teacherInChargeName = forms.CharField(max_length=255, required=True, help_text='Required.')
    teacherInChargePhone= forms.CharField(max_length=255, required=True, help_text='Required')
    teacherInChargeEmail = forms.CharField(max_length=255, required=True, help_text='Required.')
    principalName = forms.CharField(max_length=255, required=True, help_text='Required.')
    principalPhone= forms.CharField(max_length=255, required=True, help_text='Required')
    principalEmail = forms.CharField(max_length=255, required=True, help_text='Required.')

    class Meta:
        model = Project
        fields = ['topic','level','schoolName', 'firstParticipant','secondParticipant','teacherInChargeName', 'teacherInChargePhone', 'teacherInChargeEmail', 'principalName','principalPhone', 'principalEmail']

