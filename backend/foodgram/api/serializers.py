from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.models import Subscribe

User = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            'password',
        )

class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
    
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(subscriber=user, author=obj).exists()

class SubscribeSerializer(CustomUserSerializer):

    class Meta(CustomUserSerializer.Meta):
        # model = Subscribe        
        fields = CustomUserSerializer.Meta.fields
        read_only_fields = ('email', 'username', 'first_name',
            'last_name',)

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscribe.objects.filter(author=author, subscriber=user).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Ingredient
        fields = '__all__'

# вот тут по умолчанию выводятся id автора и тегов, это нужно пофиксить
# автор дб объект user
# тег - список tag objects

class IngredientInRecipeSerializer(serializers.ModelSerializer):
    # определяем поля из модели ингредиента ручками
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

class IngredientInRecipeWriteSerializer(serializers.ModelSerializer):
    id = IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')

class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

# по сути это просмотр рецепта
class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  # это рабочий фикс  вывода тегов
    # замена истояника получения данных, был - модкль рецепта, стал - ингр в рецепте
    # чтобы получить ингредиент - используй атрибут в source от recipe
    # вебинар 1:15:25
    ingredient = IngredientInRecipeSerializer(many=True, source='ingredientinrecipe_set')

    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()

class RecipeCreateSerializer(serializers.ModelSerializer):

    ingredient = IngredientInRecipeWriteSerializer(many=True)
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    # tags = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Tag.objects.all()
    # )

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        ingredient = validated_data.pop('ingredient')
        tags = validated_data.pop('tags')
        author = self.context['request'].user
        recipe = Recipe.objects.create(author=author, **validated_data)   
        recipe.tags.set(tags)

        for i in ingredient:
            # print(i['id'], i['amount'])
            
            current_ingredient = get_object_or_404(Ingredient,
                                                id=i['id'])
                                                
            IngredientInRecipe.objects.create(
                ingredient=current_ingredient, recipe=recipe,
                amount=i['amount'])
        return recipe

    def update(self, recipe, validated_data):
        ingredient = validated_data.pop('ingredient')
        tags = validated_data.pop('tags')

        recipe.tags.clear()
        recipe.ingredient.clear()
        recipe.tags.set(tags)

        IngredientInRecipe.objects.filter(
                                    recipe=recipe,
                                    ingredient__in=recipe.ingredient.all()).delete()

        for i in ingredient:            
            current_ingredient = get_object_or_404(Ingredient,
                                                id=i['id'])
                                                
            IngredientInRecipe.objects.create(
                ingredient=current_ingredient, recipe=recipe,
                amount=i['amount'])


        return super().update(recipe, validated_data)


    def to_representation(self, instance):
            return RecipeSerializer(instance, context=self.context).data