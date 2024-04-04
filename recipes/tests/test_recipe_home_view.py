from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeHomeViewsTests(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        recipe = self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn(recipe.title, content)

        response_context = response.context['recipes']
        self.assertEqual(len(response_context), 1)

    def test_recipe_home_template_dont_load_unpublished_recipes(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_shows_correct_number_recipes(self):
        for i in range(1, 21):
            self.make_recipe(
                title=f'Test recipe {i}',
                slug=f'test-{i}',
                author_data={'username': f'user_{i}'}
            )

        response = self.client.get(reverse('recipes:home'))
        response_context_recipe = response.context['recipes']
        self.assertEqual(len(response_context_recipe), 9)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_batch(qtd=8)

        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 2)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_batch(qtd=8)

        response = self.client.get(reverse('recipes:home') + '?page=invalid')
        self.assertEqual(response.context['recipes'].number, 1)

        response = self.client.get(reverse('recipes:home') + '?page=2')
        self.assertEqual(response.context['recipes'].number, 2)
