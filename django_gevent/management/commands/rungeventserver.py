from django_gevent.utils import make_django_green
make_django_green()

from gevent.pywsgi import WSGIServer
import gevent

import sys
from optparse import make_option

from django.core.management.commands.runserver import BaseRunserverCommand
from django.core.management.base import BaseCommand, CommandError

from django_gevent import get_version

# TODO: Add support for IPv6
# TODO: Benchmark, is this sutible for production?


class Command(BaseRunserverCommand):
    option_list = BaseCommand.option_list + (
        make_option('--noreload', action='store_false', dest='use_reloader', default=True,
            help='Tells Django to NOT use the auto-reloader.'),
    )
    help = "Starts the django gevent web server."

    def inner_run(self, *args, **options):
        from django.conf import settings
        from django.utils import translation
        shutdown_message = options.get('shutdown_message', '')
        quit_command = (sys.platform == 'win32') and 'CTRL-BREAK' or 'CONTROL-C'
        self.stdout.write("Validating models...\n\n")
        self.validate(display_num_errors=True)
        self.stdout.write((
            "Django version %(version)s, using settings %(settings)r\n"
            "Gevent version %(gevent_version)s, Django_gevent version %(django_gevent_version)s\n"
            "Server is running at http://%(addr)s:%(port)s/\n"
            "Quit the server with %(quit_command)s.\n"
        ) % {
            "version": self.get_version(),
            "settings": settings.SETTINGS_MODULE,
            "addr": self._raw_ipv6 and '[%s]' % self.addr or self.addr,
            "port": self.port,
            "quit_command": quit_command,
            "django_gevent_version": get_version(),
            "gevent_version": gevent.__version__,
        })
        # django.core.management.base forces the locale to en-us. We should
        # set it up correctly for the first request (particularly important
        # in the "--noreload" case).
        translation.activate(settings.LANGUAGE_CODE)
        try:
            handler = self.get_handler(*args, **options)
            run(self.addr, int(self.port), handler)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write("%s\n" % shutdown_message)
            sys.exit(0)
    
    
    
def run(addr, port, wsgi_handler):
    server_address = (addr, port)
    httpd = WSGIServer(server_address, wsgi_handler)
    httpd.serve_forever()

