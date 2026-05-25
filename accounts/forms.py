from django import forms 
# from .models import CustomUser, Customer, Staff
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from nyondo.accounts.models import CustomUser
from nyondo.finance.models import CustomerProfile, CreditTransaction

# class CustomUserForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = "__all__"
#         # error_messages = {
#         #     'category_name': {
#         #         'required':'Please fill the category name'
#         #     },
#         #     'description': {
#         #         'required':'Description is required'
#         #     }
#         # }

#     def clean_user_name(self):
#         user_name = self.cleaned_data.get('user_name')  # either use .get or [] and type inside
#         if len(user_name) > 10:
#             raise forms.ValidationError('User name should not be more than 10 characters')
        
#         return user_name

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            ('username', 'email', 'password1', 'password2', 'is_customer', 'is_staff_member')
        ]
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
        password1 = forms.CharField(
            label='Password',
            widget=forms.PasswordInput,
            min_length=8,
            widget=forms.PasswordInput(attrs={"class": "form-control"})
        )
        password2 = forms.CharField(
            label='Confirm Password',
            widget=forms.PasswordInput,
            min_length=8,
            widget=forms.PasswordInput(attrs={"class": "form-control"})
        )