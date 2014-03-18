from __future__ import absolute_import

from django.core.management.base import BaseCommand
from scrapy.cmdline import execute


class Command(BaseCommand):
    help = """Some scrapy action shortcuts
Usage : python manage.py crawl start=<start page> domain=<domain url> [jobid=<job id>]
For other stuff use python manage.py scrapy
"""

    def run_from_argv(self, argv):
        self._argv = argv
        self.execute()

    def handle(self, *args, **options):
        default_args = ['scrapy']
        argc = len(self._argv)
        if argc >= 4:
            default_args.extend(['crawl', 'walker'])
            default_args.extend(['-a', self._argv[2]])
            default_args.extend(['-a', self._argv[3]])
        else:
            self.stdout.write(self.help)
            return
        execute(default_args)
        self.stdout.write(str(args))
        self.stdout.write(str(options))

