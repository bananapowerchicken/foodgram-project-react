from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, TagViewSet


app_name = 'api'

router = DefaultRouter()

router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
