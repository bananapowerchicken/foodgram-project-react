from django.contrib import admin
from .models import CustomUser, Subscribe


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')

@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    pass