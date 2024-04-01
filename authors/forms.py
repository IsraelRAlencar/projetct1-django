from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'first_name': 'Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'email': 'The e-mail must be valid',
        }
        error_messages = {
            'username': {
                'required': 'The username is required',
            },
            'password': {
                'required': 'The password is required',
            }
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'E-mail'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password'
            }),
        }
