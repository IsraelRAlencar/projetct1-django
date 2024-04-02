import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.' # noqa E501
        ),
            code='Invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Username')
        add_placeholder(self.fields['email'], 'E-mail')
        add_placeholder(self.fields['first_name'], 'Name')
        add_placeholder(self.fields['last_name'], 'Last Name')
        add_placeholder(self.fields['password'], 'Password')
        add_placeholder(self.fields['confirm_password'], 'Confirm your Password') # noqa E501

    username = forms.CharField(
        label='Username',
        help_text='Required. Length between 4 and 40 characters. Letters, numbers and @.+-_ only.', # noqa E501
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have a max of 40 characters',
        },
        min_length=4,
        max_length=40
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your name'},
        label='Name'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last Name'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter,  one lowercase letter and one number. The length should be at least 8 characters.' # noqa E501
        ),
        validators=[strong_password],
        label='Password'
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Repeat your password'
        },
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
        help_text='The e-mail must be valid.'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            password_confirmation_error = ValidationError(
                'Passwords do not match.',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'confirm_password': [
                    password_confirmation_error,
                ],
            })
