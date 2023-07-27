from django.contrib import admin
from .models import Tag, Recipe

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipe)
class TagAdmin(admin.ModelAdmin):
    pass
