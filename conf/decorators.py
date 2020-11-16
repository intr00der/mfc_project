from django.http import Http404


def for_staff_only(func):
    """
    Allows to see file only if you are staff
    """

    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        raise Http404()

    return wrapper
