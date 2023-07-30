from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer, TagSerializer, RecipeSerializer, SubscribeSerializer, IngredientSerializer
from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet
from recipes.models import Tag, Recipe, Ingredient
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from users.models import Subscribe
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, viewsets


CustomUser = get_user_model()

class CustomUserViewSet(UserViewSet):
    # http_method_names = ('get', 'post')  # 'patch', 'delete',
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(
            detail=True,
            methods=['post', 'delete'],
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(CustomUser, id = author_id)

        if request.method == 'POST':
            serializer = SubscribeSerializer(author,
                                            data=request.data,
                                            context={"request": request})
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(subscriber=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        if request.method == 'DELETE':
            subscription = get_object_or_404(Subscribe,
                                             subscriber=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    # подумат над списком подписок
    @action(
        detail=False,
        # permission_classes=[IsAuthenticated]
        methods = ['get']
    )
    def subscriptions(self, request):
        # user = request.user
        # # queryset = CustomUser.objects.filter(follower_user=user)
        # # queryset = CustomUser.all()
        # authors = Subscribe.objects.filter(subscriber=user)
        # print(authors[0].author.first_name)
        
        # queryset = authors  #.following.all()
        # pages = self.paginate_queryset(queryset)
        # # pages = queryset
        # serializer = SubscribeSerializer(pages,
        #                                  many=True,
        #                                  context={'request': request})
        # return self.get_paginated_response(serializer.data)

        user = request.user
        queryset = CustomUser.objects.filter(following__subscriber=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(pages,
                                         many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

class IngredientViewSet(ModelViewSet):
    http_method_names = ('get')
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # pagination_class = None

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
