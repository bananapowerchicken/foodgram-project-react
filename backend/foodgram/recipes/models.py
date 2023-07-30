from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField('Название', max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField('Описание', max_length=200, unique=True)

class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

# пока только тэги и автор
class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.PositiveIntegerField()  # дб больше 1 - валидатор
    # through - вручную указать связь
    # кавычки - когда модель объявлена после этой в коде, позволяет все 
    # равно ее обработать
    # так же есть полезная through_fields - поля связи явно
    # through_fields=('recipe', 'ingredient')
    ingredient = models.ManyToManyField(Ingredient, 
                                        through='IngredientInRecipe')
    image = models.ImageField(upload_to='recipes/')

class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    # кол-во ингредиентов вручную указываем с специально созданной
    # связи ингредиент в рецепте, по сути доп поле в таблице связей