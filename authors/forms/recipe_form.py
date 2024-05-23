from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict
from authors.validators import AuthorRecipeValidator


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
        AuthorRecipeValidator(self.cleaned_data, ErrorClass=forms.ValidationError) # noqa E501

        return super_clean
