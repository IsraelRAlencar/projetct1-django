from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewsTests(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_returns_status_code_404_if_no_recipe_found(self):  # noqa E501
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 100000}))  # noqa E501
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))  # noqa E501
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_unpublished_recipes(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:category', args=(recipe.category.id,))) # noqa E501
        self.assertEqual(response.status_code, 404)
