from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, TagViewSet, RecipeViewSet #, SubscribeViewSet


app_name = 'api'

router = DefaultRouter()

router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
# router.register('subscribe', SubscribeViewSet, basename='subscribe')

urlpatterns = [
    path('', include(router.urls)),
]
