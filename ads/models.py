from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Категория')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Ads(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Объявление')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.TextField(null=True, verbose_name='Описание')
    is_published = models.BooleanField(default=False, verbose_name='Статус размещения')
    image = models.ImageField(upload_to='pictures/', null=True, blank=True, verbose_name='Фото')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='ads',
                                 verbose_name='Категория')

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name








