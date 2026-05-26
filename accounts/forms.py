from django import forms 
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        min_length=8,
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        min_length=8,
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'is_staff_member']
        error_messages = {
            'username': {
                'required': 'Please enter a username.',
                'unique': 'This username is already taken.'
            },
            'email': {
                'required': 'Please enter an email address.',
                'invalid': 'Please enter a valid email address.'
            },
            'password1': {
                'required': 'Please enter a password.',
                'min_length': 'Password must be at least 8 characters long.'
            },
            'password2': {
                'required': 'Please confirm your password.',
                'min_length': 'Password must be at least 8 characters long.'
            }
        }


# Provide legacy name expected by views
UserRegistrationForm = CustomUserCreationForm
