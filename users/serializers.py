from rest_framework import serializers

from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'


    # first_name = models.CharField(max_length=30, verbose_name='Имя')
    # last_name = models.CharField(max_length=30, null=True, verbose_name='Фамилия')
    # username = models.CharField(max_length=30, unique=True, verbose_name='Логин')
    # password = models.CharField(max_length=30, verbose_name='Пароль')
    # role = models.CharField(choices=STATUS, max_length=20, default='member', verbose_name='Должность')
    # age = models.PositiveSmallIntegerField(verbose_name='Возраст')
    # location = models.ManyToManyField(Location, verbose_name='Адрес')