from users.models import CustomUser, Subscribe
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from recipes.models import Tag, Recipe, IngredientInRecipe
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework import status


User = get_user_model()

# сериалайзеры отвечают, например, за выводлимый вид в postman рез-та запроса

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = tuple(CustomUser.REQUIRED_FIELDS) + (
            CustomUser.USERNAME_FIELD,
            'password',
        )

class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
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
        read_only_fields = ('email', 'username')

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

# вот тут по умолчанию выводятся id автора и тегов, это нужно пофиксить
# автор дб объект user
# тег - список tag objects

class IngredientInRecipeSerializer(serializers.ModelSerializer):
    # определяем поля из модели ингредиента ручками
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    id = serializers.ReadOnlyField(source='ingredient.id ')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  # это рабочий фикс  вывода тегов
    # замена истояника получения данных, был - модкль рецепта, стал - ингр в рецепте
    # чтобы получить ингредиент - используй атрибут в source от recipe
    # вебинар 1:15:25
    ingredient = IngredientInRecipeSerializer(many=True, source='ingredientinrecipe_set')
    # author = CustomUserSerializer(many=True)
    class Meta:
        model = Recipe
        fields = '__all__'