from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer, TagSerializer
from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet
from recipes.models import Tag


CustomUser = get_user_model()

class CustomUserViewSet(UserViewSet):
    http_method_names = ('get', 'post')  # 'patch', 'delete',
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
