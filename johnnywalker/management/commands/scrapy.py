from __future__ import absolute_import
from os import chdir

from django.core.management.base import BaseCommand
from scrapy.cmdline import execute

from . import get_scrapyroot


class Command(BaseCommand):
    help = 'Run scrapy within django\nUsage : python manage.py scrapy start=<start page> domain=<domain url>'

    def run_from_argv(self, argv):
        self._argv = argv
        self.execute()

    def handle(self, *args, **options):
        scrapydir = get_scrapyroot()
        chdir(scrapydir)
        default_args = ['scrapy']
        if len(self._argv) == 3 and self._argv[2] == 'deploy':
            default_args.append('deploy')
            default_args.append('webometrics')
        elif len(self._argv) == 4:
            default_args.extend(['crawl', 'walker'])
            default_args.extend(['-a', self._argv[2]])
            default_args.extend(['-a', self._argv[3]])
        else:
            self.stdout.write(self.help)
            return

        execute(default_args)
        self.stdout.write(str(args))
        self.stdout.write(str(options))

