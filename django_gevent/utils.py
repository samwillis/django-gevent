from settings import get_setting
from django.utils.importlib import import_module
import os
import gevent

def make_django_green(monkey_patch_done=False):
    if not monkey_patch_done:
        # Make python sockets green
        from gevent import monkey
        monkey.patch_all()
    
    # Make other stuff green
    for setting in get_setting('DJANGO_GEVENT_MAKE_GREEN'):
        module_name = '.'.join(setting.split('.')[:-1])
        function_name = setting.split('.')[-1]
        make_green_function = getattr(import_module(module_name), function_name)
        make_green_function()

def number_of_cpus():
    try:
        import multiprocessing
    except ImportError:
        if not hasattr(os, "sysconf"):
            raise RuntimeError("No sysconf detected - can't find number of cpu's.")
        return os.sysconf("SC_NPROCESSORS_ONLN")
    else:
        return multiprocessing.cpu_count()

def gunicorn_post_fork(server, worker):
    make_django_green(monkey_patch_done=True)
    worker.log.info("Made Django Green")

def gunicorn_on_starting(server):    
    from django.conf import settings
    from django_gevent import get_version
    import django
    server.log.info("Django version %s" %  django.get_version())
    server.log.info("Using settings %r" % settings.SETTINGS_MODULE)
    server.log.info("Gevent version %s" % gevent.__version__)
    server.log.info("Django_gevent version %s" % get_version())
