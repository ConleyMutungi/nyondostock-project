from django import forms 
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser, ROLE_CHOICES
import re
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    def validate_uganda_phone(value):
        pattern = re.compile(r'^(?:\+256|0)7\d{8}$')
        if not pattern.match(value):
            raise ValidationError('Enter a valid Ugandan phone number (e.g. 0771234567 or +256771234567).')

    def validate_nin(value):
        if not re.fullmatch(r"\d{10,14}", value):
            raise ValidationError('Enter a valid NIN (digits only, 10–14 characters).')

    phone_number = forms.CharField(
        required=False,
        max_length=20,
        label='Phone Number',
        validators=[validate_uganda_phone],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "0771234567 or +256771234567"})
    )

    nin = forms.CharField(
        required=False,
        max_length=20,
        label='National ID (NIN)',
        validators=[validate_nin],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "National ID number"})
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='Account Role',
        initial='customer',
        widget=forms.Select(attrs={"class": "form-select"})
    )
    credit_opt_in = forms.BooleanField(
        required=False,
        label='Register for credit scheme',
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
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
        fields = ['username', 'email', 'role', 'phone_number', 'nin', 'password1', 'password2']
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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data.get('phone_number')
        user.nin = self.cleaned_data.get('nin')
        user.is_staff_member = user.role in ['sales_attendant', 'store_manager', 'accounts_admin']
        if user.role in ['store_manager', 'accounts_admin']:
            user.is_staff = True
        if commit:
            user.save()
        return user


# Provide legacy name expected by views
UserRegistrationForm = CustomUserCreationForm
