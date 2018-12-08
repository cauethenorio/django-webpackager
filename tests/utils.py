# coding: utf-8

import os

from django.test.utils import (
    TestCase,
    TestContextDecorator,
    override_settings
)

from django_webpackager.conf import wp_settings, WebpackagerSettings

try:
    import mock
except ImportError:
    import unittest.mock as mock


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def make_rel(path):
    return os.path.relpath(path, BASE_DIR)


def join_basedir(*args):
    return os.path.join(BASE_DIR, *args)


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


class BaseWebpackagerTestCase(TestCase):

    BASE_DIR = BASE_DIR

    @classmethod
    def make_rel(cls, path):
        return make_rel(path)

    @classmethod
    def join_basedir(cls, *args):
        return join_basedir(*args)
