from django.contrib.auth.models import AbstractUser
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50, verbose_name='Адрес')
    lat = models.DecimalField(max_digits=8, decimal_places=6, verbose_name='Долгота')
    lng = models.DecimalField(max_digits=8, decimal_places=6, verbose_name='Широта')

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class User(AbstractUser):
    USER = 'User'
    ADMIN = 'Admin'
    MODERATOR = 'Moderator'
    STATUS = [
        ('User', 'Пользователь'),
        ("Admin", 'Администратор'),
        ("Moderator", 'Модератор')
    ]

    role = models.CharField(choices=STATUS, max_length=20, default=USER, verbose_name='Должность')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', null=True)
    location = models.ManyToManyField(Location, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} {self.first_name}'

    @property
    def total_ads(self):
        return self.ads_set.count()




