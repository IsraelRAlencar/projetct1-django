from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewsTests(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        resolver = resolve(reverse('recipes:search'))
        self.assertIs(resolver.func.view_class, views.RecipeListViewSearch)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=<test>')
        self.assertIn(
            'Search for &quot;&lt;test&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            title=title1, slug='one', author_data={'username': 'user_one'}
        )

        recipe2 = self.make_recipe(
            title=title2, slug='two', author_data={'username': 'user_two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=This')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_template_shows_correct_number_recipes(self):
        for i in range(1, 21):
            self.make_recipe(
                title=f'Test recipe {i}',
                slug=f'test-{i}',
                author_data={'username': f'user_{i}'}
            )

        search_url = reverse('recipes:search')
        response = self.client.get(f'{search_url}?q=Test')
        response_context_recipe = response.context['recipes']
        self.assertEqual(len(response_context_recipe), 9)
