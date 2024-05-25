from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status # noqa F401
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView # noqa F401
from rest_framework.viewsets import ModelViewSet # noqa F401
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 2


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', None)
        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs


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
