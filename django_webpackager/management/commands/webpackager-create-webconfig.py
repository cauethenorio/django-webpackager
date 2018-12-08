# coding: utf-8

import os

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from django_webpackager import discover, webconfig, exceptions
from django_webpackager.conf import wp_settings


class Command(BaseCommand):
    help = 'Create a webconfig directory'

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--app',
            help='App label of an application where to create the webconfig',
        )
        group.add_argument(
            '--dir',
            help='Webconfig destination directory',
        )

    def handle(self, app=None, dir=None, *args, **options):
        if app:
            try:
                app_config = apps.get_app_config(app)
            except LookupError as err:
                raise CommandError(str(err))

            target_dir = os.path.join(app_config.path, wp_settings.APPS_WEBAPPS_DIR)

        elif dir:
            if os.path.isabs(dir):
                target_dir = dir
            else:
                target_dir = os.path.join(os.getcwd(), dir)

        else:
            target_dir = wp_settings.DEFAULT_WEBCONFIG_PATH

        try:
            webconfig.create_webconfig_dir(target_dir)
        except exceptions.WebconfigCreationError as e:
            raise CommandError(e)
