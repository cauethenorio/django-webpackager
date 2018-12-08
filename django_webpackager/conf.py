# coding: utf-8

import os
import importlib

from django.utils.functional import LazyObject
from django.conf import settings


def get_project_rootdir():
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
    settings_path = importlib.import_module(settings_module).__file__

    project_root = os.path.dirname(settings_path)
    return project_root


class WebpackagerSettings(object):

    def get_with_prefix(self, setting_name, fallback):
        return getattr(
            settings,
            'WEBPACKAGER_{}'.format(setting_name),
            fallback
        )

    def __init__(self):

        self.APPS_WEBAPPS_DIR = self.get_with_prefix(
            'APPS_WEBAPPS_DIR', 'webapps'
        )

        self.DEFAULT_WEBCONFIG_PATH = os.path.join(
            get_project_rootdir(), 'webconfig'
        )


class LazyWebPackagerSettings(LazyObject):
    """Lazy-load the app settings, so they can be easily replaced in tests"""

    def _setup(self, name=None):
        self._wrapped = WebpackagerSettings()


wp_settings = LazyWebPackagerSettings()
