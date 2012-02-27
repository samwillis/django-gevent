from django.http import HttpResponse
from django.shortcuts import render
import gevent

from django_gevent.ajax import event_source, streaming_response
from django_gevent.pubsub import PubSubQueue


def home(request):
    return render(request, 'home.html', {})


@streaming_response
def long_streaming_responce(request):
    def stream_response_generator():
        yield "<html><body>\n"
        for x in range(1,31):
            yield "<div>%s</div>\n" % x
            yield " " * 1024  # Encourage browser to render incrementally
            gevent.sleep(1)
        yield "</body></html>\n"
    resp = HttpResponse(stream_response_generator(), mimetype='text/html')
    return resp




@event_source
def event_source_test(request):
    if request.last_event_id:
        start = int(request.last_event_id)+1
    else:
        start = 1
    for x in range(start,start+5):
        gevent.sleep(20)
        yield {
            'event': 'update',
            'data': "Test event\ntest line 2",
        }
        yield {
            'data': None,
            'retry': 1000,
        }
        yield {
            'event': 'message',
            'id': x,
            'data': "%s" % x,
        }
        if request.long_poll:
            break    

def event_source_view(request):
    return render(request, 'event_source_test.html', {})




def chat(request):
    return render(request, 'chat.html', {})

chatqueue = PubSubQueue()

def chat_post(request):
    comment = request.POST.get('comment', '')
    name = request.POST.get('name', '')
    if comment and name:
        chatqueue.put('chat', (name, comment.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br />\n')))
    return HttpResponse()

@event_source
def chat_event_source(request):
    if request.last_event_id:
        history = chatqueue.get_history('chat', request.last_event_id)
        if history:
            for oid, obj in history:
                yield {
                    'data': "%s\n%s" % obj,
                    'id': "%s" % oid,
                    'retry': 50,
                }
            if request.long_poll:
                return
        
    while True:
        oid, obj = chatqueue.get('chat')
        yield {
            'data': "%s\n%s" % obj,
            'id': "%s" % oid,
            'retry': 50,
        }
        if request.long_poll:
            return