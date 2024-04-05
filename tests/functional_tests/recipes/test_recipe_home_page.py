
from unittest.mock import patch
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.functional_tests.recipes.base_recipes import RecipeBaseFunctionalTest # noqa
import pytest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        # Usuario abre a pagina
        self.browser.get(self.live_server_url)

        # ve o campo de busca com texto "Search for a recipe..."
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe..."]'
        )

        # ele digita "Recipe Title 1" no campo de busca
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            recipes[0].title,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        self.browser.get(self.live_server_url)

        self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        ).click()

        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
