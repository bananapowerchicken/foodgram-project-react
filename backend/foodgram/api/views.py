from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer
from djoser.views import UserViewSet

CustomUser = get_user_model()

class CustomUserViewSet(UserViewSet):
    http_method_names = ('get', 'post')  # 'patch', 'delete',
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer