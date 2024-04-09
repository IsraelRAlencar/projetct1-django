from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict

from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields['preparation_steps'], 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Portions', 'Portions'),
                    ('Units', 'Units'),
                    ('People', 'People'),
                    ('Servings', 'Servings'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Hours', 'Hours'),
                    ('Minutes', 'Minutes'),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_errors['description'].append('Title and description must be different') # noqa E501 

        if self._my_errors:
            raise forms.ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('Title must be at least 5 characters long') # noqa E501

        return title

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')

        if is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append('Preparation time cannot be negative') # noqa E501

        return preparation_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')

        if not is_positive_number(servings):
            self._my_errors['servings'].append('Servings cannot be negative') # noqa E501

        return servings
