from django import forms 
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser, ROLE_CHOICES


class CustomUserCreationForm(UserCreationForm):
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
        fields = ['username', 'email', 'role', 'password1', 'password2']
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
        user.is_staff_member = user.role in ['sales_attendant', 'store_manager', 'accounts_admin']
        if user.role in ['store_manager', 'accounts_admin']:
            user.is_staff = True
        if commit:
            user.save()
        return user


# Provide legacy name expected by views
UserRegistrationForm = CustomUserCreationForm
