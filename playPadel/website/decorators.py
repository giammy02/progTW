from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def cliente_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='playPadel:login'):
    '''
    Decorator for views that checks that the logged-in user is a client,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_cliente,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def gestore_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='playPadel:login'):
    '''
    Decorator for views that checks that the logged-in user is a gestore,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
