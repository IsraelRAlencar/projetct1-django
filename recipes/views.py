from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Recipe
# from utils.recipes.factory import make_recipe


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')

    return render(request, 'recipes/pages/home.html', {
        'recipes': recipes,
    })


def category(request, category_id):

    recipes = get_list_or_404(Recipe.objects.filter(
        is_published=True,
        category__id=category_id
    ).order_by('-id'))

    return render(request, 'recipes/pages/category.html', {
        'recipes': recipes,
        'title': f'{recipes.first().category.name} | '
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', {
        'recipe': recipe,
        'is_detail_page': True,
    })
