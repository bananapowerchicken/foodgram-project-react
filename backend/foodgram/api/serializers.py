from users.models import CustomUser
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from recipes.models import Tag, Recipe, IngredientInRecipe

# сериалайзеры отвечают, например, за выводлимый вид в postman рез-та запроса

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = tuple(CustomUser.REQUIRED_FIELDS) + (
            CustomUser.USERNAME_FIELD,
            'password',
        )

class CustomUserSerializer(UserSerializer):
    # is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            # 'is_subscribed',
        )

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = '__all__'

# вот тут по умолчанию выводятся id автора и тегов, это нужно пофиксить
# автор дб объект user
# тег - список tag objects

class IngredientInRecipeSerializer(serializers.ModelSerializer):
    # определяем поля из модели ингредиента ручками
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

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