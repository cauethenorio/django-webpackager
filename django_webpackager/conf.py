# coding: utf-8

from django.utils.functional import LazyObject
from django.conf import settings


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

        self.DEFAULT_WEBCONFIG_DIRNAME = self.get_with_prefix(
            'DEFAULT_WEBCONFIG_DIRNAME', 'webconfig'
        )


class LazyWebPackagerSettings(LazyObject):
    """Lazy-load the app settings, so they can be easily replaced in tests"""

    def _setup(self, name=None):
        self._wrapped = WebpackagerSettings()


wp_settings = LazyWebPackagerSettings()
