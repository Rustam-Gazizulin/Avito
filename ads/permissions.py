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
        # if obj.user == request.user:
        #     return True
        # return False
