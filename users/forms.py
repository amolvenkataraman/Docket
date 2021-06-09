from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import DocketUser

# Customize the registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # Add email first name and last name
    class Meta:
        model = DocketUser
        fields = ['username', 'first_name', 'last_name', 'email', 'school', 'grade', 'password1', 'password2']
