from django.core.management.base import NoArgsCommand, CommandError, BaseCommand
from optparse import make_option    

default_script = \
"""\"\"\"Gunicorn config\"\"\"
from django_gevent.utils import gunicorn_post_fork, gunicorn_on_starting, number_of_cpus

bind = "%(ipaddress)s:%(port)s"
workers = %(workers)s
worker_class = "gevent"
post_fork = gunicorn_post_fork
on_starting = gunicorn_on_starting
"""

default_file_name = "gunicorn.conf"
default_ip = "127.0.0.1"
default_port = 8000
default_workers = "number_of_cpus() * 2 + 1"


class Command(NoArgsCommand):
    help = 'Creates a Gunicorn config file.'
    option_list = BaseCommand.option_list + (
        make_option('--filename', '-f',
            dest='filename',
            default=default_file_name,
            help='The file name to save the Gunicorn config to. Defaults to "%s"' % default_file_name),
        make_option('--ipaddress', '-i',
            dest='ipaddress',
            default=default_ip,
            help='The IP Address that Gunicorn should run on. Defaults to "%s"' % default_ip),
        make_option('--port', '-p',
            dest='port',
            default=default_port,
            help='The port that Gunicorn should run on. Defaults to "%s"' % default_port),
        make_option('--workers', '-w',
            dest='workers',
            default=default_workers,
            help='The number of worker processes that Gunicorn should run. Defaults to "%s". You can use the "number_of_cpus()" function to set this to a multiple of the number of cpu cores avalible.' % default_workers),
    )

    
    def handle_noargs(self, **options):
        with open(options['filename'], 'w') as conf_file:
            conf_file.write(default_script % {
                'ipaddress': options['ipaddress'],
                'port': options['port'],
                'workers': options['workers'],
            })
        self.stdout.write('Successfully written Gunicorn config file to "%s"\n' % options['filename'])

