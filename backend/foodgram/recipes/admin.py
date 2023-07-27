from django.contrib import admin
from .models import Tag, Recipe, Ingredient, IngredientInRecipe

# фича джанго
# позволит нам внедрить ингредиенты в рецепты без прокидывания в админку промежуточной таблицы
# отдельным некрасивым пунктом
class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1  # 1 доп форма для создания

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInRecipeInline, )

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass
