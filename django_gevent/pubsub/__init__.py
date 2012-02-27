from django_gevent.settings import get_setting
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

def load_backend():
    backend_settings = get_setting('DJANGO_GEVENT_PUBSUB')
    if 'backend' in backend_settings:
        backend_path = backend_settings['backend']
    else:
        raise ImproperlyConfigured("DJANGO_GEVENT_PUBSUB['backend'] not set, required to the django_gevent PubSubQueue to function.")
        
    backend_module_name = '.'.join(backend_path.split('.')[:-1])
    backend_class_name = backend_path.split('.')[-1]
    backend_class = getattr(import_module(backend_module_name), backend_class_name)
    return backend_class

class PubSubQueue(object):
    
    def __init__(self, history_to_keep=100):
        self.history_to_keep = history_to_keep
        self.backend = load_backend()(history_to_keep)
    
    def put(self, channel, obj):
        self.backend.put(channel, obj)
    
    def get(self, channel):
        oid, obj = self.backend.get(channel)
        return oid, obj
    
    def get_history(self, channel, last_id):
        return list(self.backend.get_history(channel, last_id))


