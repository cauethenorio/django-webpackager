# coding: utf-8

import sys

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from ...discover import get_project_webapps_layout


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        configs = get_project_webapps_layout(apps)
        print(configs)



        #configs = set(wb.config for wb in webpackages)

        # try:
        #     apps['testapp'].run_bundler(watch=True)
        # except KeyboardInterrupt:
        #     sys.exit(0)  # or 1, or whatever


        #import pdb
        #pdb.set_trace()

