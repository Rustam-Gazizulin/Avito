from rest_framework.permissions import BasePermission

from users.models import User


class AdsUpdatePermission(BasePermission):
    message = "Нет прав на изменение данных"

    def has_permission(self, request, view):
        if request.user.role == User.ADMIN:
            return True
        if request.method == 'PATCH':
            return request.user.is_authenticated and request.user.ads_set.exists()
        return True


class IsOwnerIsStaff(BasePermission):
    message = 'Редактировать может только владелец или модератор'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner or request.user.role in [User.ADMIN, User.MODERATOR]:
            return True
        return False



