import gevent
from gevent.queue import Queue
from gevent.event import Event
from base_backend import BasePubSubQueueBackend


class GeventBroadcastQueue(gevent.Greenlet):
    queue = Queue()
    ready_event = Event()
    current_obj = None
    
    def __init__(self):
        gevent.Greenlet.__init__(self)
        self.start()
    
    def _run(self):
        while True:
            self.ready_event.clear()
            obj = self.queue.get()
            self.current_obj = obj
            self.ready_event.set()
    
    def put(self, obj):
        self.queue.put(obj)
    
    def get(self):
        self.ready_event.wait()
        return self.current_obj


class SimplePubSubBackend(BasePubSubQueueBackend):
    queues = {}
    historys = {}
    current_ids = {}
    
    def _get_new_id(self, channel):
        if not channel in self.current_ids:
            self.current_ids[channel] = 0
        cid = self.current_ids[channel]
        self.current_ids[channel] += 1
        return cid
    
    def _add_history(self, channel, obj, oid):
        if not channel in self.historys:
            self.historys[channel] = {
                'oids': [],
                'objs': [],
            }
    
        self.historys[channel]['oids'].append(oid)
        self.historys[channel]['objs'].append(obj)
        
        if len(self.historys[channel]['objs']) > self.history_to_keep:
            self.historys[channel]['oids'].pop(0)
            self.historys[channel]['objs'].pop(0)
        
    def put(self, channel, obj):
        if not channel in self.queues:
            self.queues[channel] = GeventBroadcastQueue()
        oid = self._get_new_id(channel)
        self.queues[channel].put((oid, obj))
        self._add_history(channel, obj, oid)
    
    def get(self, channel):
        if not channel in self.queues:
            self.queues[channel] = GeventBroadcastQueue()
        oid, obj = self.queues[channel].get()
        return oid, obj
    
    def get_history(self, channel, last_id):
        if channel in self.historys:
            last_id = int(last_id)
            if last_id in self.historys[channel]['oids']:
                pos = self.historys[channel]['oids'].index(last_id)+1
                for i in xrange(pos, len(self.historys[channel]['oids'])):
                    oid = self.historys[channel]['oids'][i]
                    obj = self.historys[channel]['objs'][i]
                    yield (oid, obj)
