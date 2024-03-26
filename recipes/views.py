from django.shortcuts import render
from utils.recipes.factory import make_recipe
from .models import Recipe
from django.http import Http404


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

    if not recipes:
        raise Http404('Not found :(')

    return render(request, 'recipes/pages/category.html', {
        'recipes': recipes,
        'title': f'{recipes.first().category.name} | '
    })


def recipe(request, id):
    recipe = Recipe.objects.filter(pk=id, is_published=True).first()

    return render(request, 'recipes/pages/recipe-view.html', {
        'recipe': recipe,
        'is_detail_page': True,
    })
