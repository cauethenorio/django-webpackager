# coding: utf-8

from django.test.utils import TestContextDecorator, override_settings

from django_webpackager.conf import wp_settings, WebpackagerSettings

try:
    import mock
except ImportError:
    import unittest.mock as mock


class override_settings_and_update_wp_conf(TestContextDecorator):
    def __init__(self, **kwargs):
        self.OverrideSettings = override_settings(**kwargs)
        super(override_settings_and_update_wp_conf, self).__init__()

    def enable(self):
        self.original = wp_settings._wrapped
        self.OverrideSettings.enable()
        wp_settings._wrapped = WebpackagerSettings()


    def disable(self):
        wp_settings._wrapped = self.original
        self.OverrideSettings.disable()
