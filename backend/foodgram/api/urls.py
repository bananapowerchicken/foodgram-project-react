from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, TagViewSet, RecipeViewSet


app_name = 'api'

router = DefaultRouter()

router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
