from django.core.exceptions import PermissionDenied
from models import CustomUser


def admin_required(view_func):
    """ is it an admin. """
    def _wrapped_view(request, *args, **kwargs):
        user_roles = request.user.roles.all().values_list('name', flat=True)
        if CustomUser.ROLE_ADMIN not in user_roles:
            raise PermissionDenied("Access is allowed only to the admin")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def author_required(view_func):
    """ Is it an author or an admin. """
    def _wrapped_view(request, *args, **kwargs):
        user_roles = request.user.roles.all().values_list('name', flat=True)
        if CustomUser.ROLE_AUTHOR not in user_roles and CustomUser.ROLE_ADMIN not in user_roles:
            raise PermissionDenied("Access is allowed only to the author or admin")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
