from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer, RecipeShortSerializer, TagSerializer, RecipeSerializer, RecipeCreateSerializer, SubscribeSerializer, IngredientSerializer
from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet
from recipes.models import Tag, Recipe, Ingredient
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from users.models import Subscribe
from recipes.models import Favorite, ShoppingCart
from rest_framework.response import Response
from rest_framework import status
from reportlab.pdfgen import canvas  
from django.http import HttpResponse



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
    # serializer_class = RecipeSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return RecipeCreateSerializer            
        return RecipeSerializer
    
    # serializer_class = get_serializer_class(self)
    
    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Этот рецепт уже добавлен'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Этого рецепта не существует'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
            detail=True,
            methods=['post', 'delete'],
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(Favorite, request.user, pk)
        else:
            return self.delete_from(Favorite, request.user, pk)
    
    @action(
            detail=True,
            methods=['post', 'delete'],
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        else:
            return self.delete_from(ShoppingCart, request.user, pk)
    
    @staticmethod
    def getpdf(request): 
        response = HttpResponse(content_type='application/pdf') 
        response['Content-Disposition'] = 'attachment; filename="file.pdf"' 
        p = canvas.Canvas(response) 
        p.setFont("Times-Roman", 55) 
        p.drawString(100,700, "Hello, Javatpoint.") 
        p.showPage() 
        p.save() 
        return response

    @action(detail=False)
    def download_shopping_cart(self, request):
        # queryset = []
        return self.getpdf(request)