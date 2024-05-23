from collections import defaultdict
from django.core.exceptions import ValidationError

from utils.strings import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass # noqa E501
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_servings()
        self.clean_preparation_time()

        cleaned_data = self.data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self.errors['description'].append('Title and description must be different') # noqa E501 

        if self.errors:
            raise self.ErrorClass(self.errors)

    def clean_title(self):
        title = self.data.get('title')

        if len(title) < 5:
            self.errors['title'].append('Title must be at least 5 characters long') # noqa E501

        return title

    def clean_preparation_time(self):
        preparation_time = self.data.get('preparation_time')

        if not is_positive_number(preparation_time):
            self.errors['preparation_time'].append('Preparation time cannot be negative') # noqa E501

        return preparation_time

    def clean_servings(self):
        servings = self.data.get('servings')

        if not is_positive_number(servings):
            self.errors['servings'].append('Servings cannot be negative') # noqa E501

        return servings
