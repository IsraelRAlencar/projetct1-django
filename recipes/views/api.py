from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status # noqa F401
from django.shortcuts import get_object_or_404
from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(recipes, many=True, context={'request': request}) # noqa E501

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data) # noqa E501
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED) # noqa E501


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    serializer = RecipeSerializer(recipe, many=False, context={'request': request}) # noqa E501
    return Response(serializer.data)

    # recipe = Recipe.objects.get_published().filter(pk=pk).first()

    # if recipe:
    #     serializer = RecipeSerializer(recipe)
    #     return Response(serializer.data)
    # else:
    #     return Response(
    #         {'error': 'Not found'},
    #         status=status.HTTP_404_NOT_FOUND
    #     )


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk,
    )

    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request}
    )

    return Response(serializer.data)
