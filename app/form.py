from dataclasses import field
from django.forms import ModelForm, Form
from django.contrib.auth.models import User
class SignupForm():
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']