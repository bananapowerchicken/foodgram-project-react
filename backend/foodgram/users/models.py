from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """ Модель пользователя"""
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name', 
        'username',
    ]

    email = models.EmailField(
        'Адрес электронной почты',
        max_length = 254,
        unique=True,
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,        
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank = False,
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,  
        blank = False,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
 