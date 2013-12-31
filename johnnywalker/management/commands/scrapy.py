from __future__ import absolute_import
from django.core.management.base import BaseCommand
from scrapy.cmdline import execute

class Command(BaseCommand):
    help = 'Run scrapy within django'
    
    def run_from_argv(self, argv):
        self._argv = argv
        self.execute()

    def handle(self, *args, **options):
        execute(self._argv[1:])
        self.stdout.write(str(args))
        self.stdout.write(str(options))

