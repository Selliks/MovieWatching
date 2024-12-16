from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()


def admin_required(view_func):
    """ Is it an admin """

    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'roles'):
            raise PermissionDenied("Access is allowed only to the admin")

        user_roles = request.user.roles.all().values_list('name', flat=True)
        if User.ROLE_ADMIN not in user_roles:
            raise PermissionDenied("Access is allowed only to the admin")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def author_required(view_func):
    """ Is it an admin or an author """

    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'roles'):
            raise PermissionDenied("Access is allowed only to the author or admin")

        user_roles = request.user.roles.all().values_list('name', flat=True)
        if User.ROLE_AUTHOR not in user_roles and User.ROLE_ADMIN not in user_roles:
            raise PermissionDenied("Access is allowed only to the author or admin")

        return view_func(request, *args, **kwargs)

    return _wrapped_view

