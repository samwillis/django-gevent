from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_gevent_dev.views.home', name='home'),
    # url(r'^django_gevent_dev/', include('django_gevent_dev.foo.urls')),
    
    url(r'^$', 'testapp.views.home'),
    
    url(r'^long-streaming-responce/$', 'testapp.views.long_streaming_responce'),
    
    url(r'^long-polling/$', 'testapp.views.long_polling_view'),
    url(r'^long-polling-test/$', 'testapp.views.long_polling_test'),
    
    url(r'^event-source/$', 'testapp.views.event_source_view'),
    url(r'^event-source-test/$', 'testapp.views.event_source_test'),
    
    url(r'^chat/$', 'testapp.views.chat'),
    url(r'^chat/post/$', 'testapp.views.chat_post'),
    url(r'^chat/event_source/$', 'testapp.views.chat_event_source'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += staticfiles_urlpatterns()