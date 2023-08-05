# Generated by Django 3.2 on 2023-08-04 12:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20230804_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Значение не может быть меньше 1.')], verbose_name='Время приготовления рецепта'),
        ),
    ]
