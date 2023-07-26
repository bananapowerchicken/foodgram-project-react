from django.db import models

class Tag(models.Model):
    name = models.CharField('Название', max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField('Описание', max_length=200, unique=True)
