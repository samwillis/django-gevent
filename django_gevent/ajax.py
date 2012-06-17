from django.http import HttpResponse
from django.views.decorators.http import condition


def streaming_response(view):
    # TODO: Transactions? Gzip? others?
    return condition(etag_func=None, last_modified_func=None)(view)


def event_source(view):
    def event_view(request, *args, **kwargs):
        mimetype = 'text/event-stream'
        
        if 'HTTP_LAST_EVENT_ID' in request.META:
            request.last_event_id = request.META['HTTP_LAST_EVENT_ID']
        else:
            request.last_event_id = None
        
        request.long_poll = False
        if 'HTTP_X_REQUESTED_WITH' in request.META:
            if request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
                request.long_poll = True
        
        def event_gen():
            for message in view(request, *args, **kwargs):
                for key, value in message.items():
                    if value == None:
                        yield "%s\n" % key
                    else:
                        for line in str(value).split('\n'):
                            yield "%s: %s\n" % (key, line)
                yield "\n"
            
        resp = HttpResponse(event_gen(), mimetype=mimetype)
        return resp
    return streaming_response(event_view)
