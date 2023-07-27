from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer, TagSerializer, RecipeSerializer
from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet
from recipes.models import Tag, Recipe


CustomUser = get_user_model()

class CustomUserViewSet(UserViewSet):
    http_method_names = ('get', 'post')  # 'patch', 'delete',
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
