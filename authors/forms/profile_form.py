from collections import defaultdict
from django import forms
from authors.models import Profile
from utils.django_forms import add_placeholder, add_attr, strong_password
from django.forms import ValidationError
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_placeholder(self.fields['bio'], 'Write a short Bio about yourself')
        add_attr(self.fields['bio'], 'class', 'span-2 row-6')
        add_placeholder(self.fields['username'], 'Username')
        add_placeholder(self.fields['email'], 'E-mail')
        add_placeholder(self.fields['first_name'], 'Name')
        add_placeholder(self.fields['last_name'], 'Last Name')
        add_placeholder(self.fields['password'], 'Password')
        add_placeholder(self.fields['confirm_password'], 'Confirm your Password') # noqa E501

    first_name = forms.CharField(
        error_messages={'required': 'Write your name'},
        label='Name'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last Name'
    )

    username = forms.CharField(
        label='Username',
        error_messages={
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have a max of 40 characters',
        },
        min_length=4,
        max_length=40
    )

    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
        help_text='The e-mail must be valid.'
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
        label='Password',
        required=False
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Repeat your password'
        },
        required=False
    )

    class Meta:
        model = Profile
        fields = [
            'bio',
            'profile_cover',
        ]
        widgets = {
            'profile_cover': forms.FileInput(
                attrs={
                    'class': 'span-2 row-7'
                }
            )
        }

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')

        if len(bio) < 10:
            self._my_errors['bio'].append('Bio must be at least 10 characters long.') # noqa E501

        if len(bio) > 300:
            self._my_errors['bio'].append('Bio must not have more then 300 characters.') # noqa E501

        return bio

    def clean_email(self):
        email = self.cleaned_data.get('email')

        email_user = User.objects.filter(email=email)
        user = User.objects.filter(username=self.cleaned_data.get('username')).first() # noqa E501

        if email_user == user.email:
            raise ValidationError(
                'User e-mail is already registered.', code='invalid'
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password or confirm_password:
            if not password:
                self._my_errors['password'].append('Password must not be empty.') # noqa E501
            if not confirm_password:
                self._my_errors['confirm_password'].append('Password confirmation must not be empty.') # noqa E501

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
