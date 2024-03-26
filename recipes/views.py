from django.shortcuts import render
from utils.recipes.factory import make_recipe
from .models import Recipe


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')

    return render(request, 'recipes/pages/home.html', {
        'recipes': recipes,
    })


def category(request, category_id):
    recipes = Recipe.objects.filter(
            is_published=True,
            category__id=category_id
        ).order_by('-id')

    return render(request, 'recipes/pages/category.html', {
        'recipes': recipes,
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', {
        'recipe': make_recipe(),
        'is_detail_page': True,
    })
