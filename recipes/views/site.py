from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from tag.models import Tag
from ..models import Recipe
from django.db.models import Q
from utils.pagination import make_pagination
from django.http import JsonResponse
import os
from django.forms.models import model_to_dict
from django.utils import translation
# from django.utils.translation import gettext as _
# from utils.recipes.factory import make_recipe


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def theory(request, *args, **kwargs):
    recipes = Recipe.objects.get_published()

    context = {
        'recipes': recipes,
    }

    return render(
        request,
        'recipes/pages/theory.html',
        context=context,
    )


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = '-id'
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)

        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags', 'author__profile')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )

        html_language = translation.get_language()

        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range, 'html_language': html_language} # noqa E501
        )

        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_dict = recipes.object_list.values()

        return JsonResponse(
            list(recipes_dict),
            safe=False,
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} | '
        })

        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
            is_published=True
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()

        ctx.update({
            'page_title': f'Search for "{search_term}"',
            'search_term': self.request.GET.get('q', ''),
            'additional_url_query': f'&q={search_term}'
        })

        return ctx


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            tags__slug=self.kwargs.get('slug', '')
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(slug=self.kwargs.get('slug', '')).first() # noqa E501

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag'

        ctx.update({
            'page_title': page_title,

        })

        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True,
        })

        return ctx


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.created_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + recipe_dict['cover'].url[1:] # noqa E501
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )
