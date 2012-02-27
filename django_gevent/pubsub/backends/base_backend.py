class BasePubSubQueueBackend(object):

    def __init__(self, history_to_keep):
        self.history_to_keep = history_to_keep
    
    def put(self, channel, obj):
        """Publish Item"""
        raise NotImplementedError()
    
    def get(self, channel):
        """Returns tuple of (oid, obj)"""
        raise NotImplementedError()
    
    def get_history(self, channel, last_id):
        """Returns list of tuples (oid, obj)"""
        raise NotImplementedError()