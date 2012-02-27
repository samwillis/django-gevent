from base_backend import BasePubSubQueueBackend
from django_gevent.settings import get_setting
import redis

try:
   import cPickle as pickle
except:
   import pickle
   
# TODO: This can be made alot more efficient, currently on connection for each greanlet wainting for a message.

class RedisPubSubBackend(BasePubSubQueueBackend):
    
    def __init__(self, *args, **kwargs):
        super(RedisPubSubBackend, self).__init__(*args, **kwargs)
        backend_settings = get_setting('DJANGO_GEVENT_PUBSUB')
        if not 'host' in backend_settings:
            raise ImproperlyConfigured("DJANGO_GEVENT_PUBSUB['host'] not set, required to the django_gevent PubSubQueue to function.")
        if not 'port' in backend_settings:
            raise ImproperlyConfigured("DJANGO_GEVENT_PUBSUB['port'] not set, required to the django_gevent PubSubQueue to function.")
        if not 'db' in backend_settings:
            raise ImproperlyConfigured("DJANGO_GEVENT_PUBSUB['db'] not set, required to the django_gevent PubSubQueue to function.")
        self.rcon = redis.Redis(host=backend_settings['host'], port=backend_settings['port'], db=backend_settings['db'])
    
    def _get_new_id(self, channel):
        return self.rcon.incr('django_gevent_pubsub:%s:counter' % channel)
    
    def _add_history(self, channel, obj, oid):
        dump = pickle.dumps((oid, obj))
        self.rcon.zadd('django_gevent_pubsub:%s:history' % channel, score=oid, value=dump)
        self.rcon.zrangebyscore('django_gevent_pubsub:%s:history' % channel, 0, -(self.history_to_keep+1))
        
    def put(self, channel, obj):
        oid = self._get_new_id(channel)
        dump = pickle.dumps((oid, obj))
        self.rcon.publish('django_gevent_pubsub:%s:pubsub_queue' % channel, dump)
        self._add_history(channel, obj, oid)
        
    def get(self, channel):
        rpubsub = self.rcon.pubsub()
        rpubsub.subscribe('django_gevent_pubsub:%s:pubsub_queue' % channel)
        oid, obj = pickle.loads(rpubsub.listen().next()['data'])
        return oid, obj
        
    def get_history(self, channel, last_id):
        for picked_obj in self.rcon.zrangebyscore('django_gevent_pubsub:%s:history' % channel, int(last_id)+1, '+inf'):
            oid, obj = pickle.loads(picked_obj)
            yield oid, obj



