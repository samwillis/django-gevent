from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def get_setting(setting):
    if hasattr(settings, setting):
        return getattr(settings, setting)
    else:
        raise ImproperlyConfigured('The %s setting is requied, see the django_gevent docs for help configuring.' % setting)
