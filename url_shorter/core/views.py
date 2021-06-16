import functools
import traceback
from django.shortcuts import redirect, reverse
from .exceptions import EmptyUrlException, SubpartAlreadyExistsException


def error_response(exception):
    """Отправляется страница с ошибкой"""
    return redirect(reverse('index')+'?exception='+str(exception))

def base_view(fn):
    """Декоратор для всех view, обрабатывает исключения"""
    @functools.wraps(fn)
    def inner(requests, *args, **kwargs):
        try:
            return fn(requests, *args, **kwargs)
        except (EmptyUrlException, SubpartAlreadyExistsException) as e:
            return error_response(e)
        except Exception as e:
            print("Ошибка")
    return inner