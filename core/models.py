import os
from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories', default="default.png")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def category_image(self):
        if self.image:
            return self.image.url
        return "/media/categories/default.png"
