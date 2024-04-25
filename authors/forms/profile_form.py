from collections import defaultdict
from django import forms
from authors.models import Profile
from utils.django_forms import add_placeholder, add_attr


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_placeholder(self.fields['bio'], 'Write a short Bio about yourself')
        add_attr(self.fields['bio'], 'class', 'span-2')

    class Meta:
        model = Profile
        fields = [
            'bio',
            'profile_cover',
        ]
        widgets = {
            'profile_cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
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
