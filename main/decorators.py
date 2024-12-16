from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """ Is it an admin (is_superuser) """

    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("Access for an admin")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def staff_required(view_func):
    """ Is it a staff (is_staff) """

    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.is_staff:
            raise PermissionDenied("Access for a staff and an admin")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
