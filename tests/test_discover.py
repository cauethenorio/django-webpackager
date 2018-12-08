import os

from django.apps import apps
from django.conf import settings

from django_webpackager import discover
from django_webpackager import exceptions
from django_webpackager.conf import wp_settings

from .utils import (
    BaseWebpackagerTestCase,
    join_basedir,
    mock,
    override_settings_and_update_wp_conf
)


class GetSettingsWebconfigsTestCase(BaseWebpackagerTestCase):

    def test_default_webconfig_path_should_be_correct(self):
        dir = self.make_rel(wp_settings.DEFAULT_WEBCONFIG_PATH)
        self.assertEqual(dir, 'webconfig')

    @mock.patch('django_webpackager.discover.is_valid_webconfig_dir')
    def test_get_default_webconfig_path_from_root(self, is_valid_stub):
        discover.get_settings_webconfigs()
        is_valid_stub.assert_called_once_with(self.join_basedir('webconfig'))

    @mock.patch('django_webpackager.discover.is_valid_webconfig_dir')
    @override_settings_and_update_wp_conf(
        WEBPACKAGER_WEBCONFIG_PATH='/invalid-path'
    )
    def test_inexistent_webconfig_path_should_raise(self, is_valid_stub):
        discover.get_settings_webconfigs()
        is_valid_stub.assert_called_once_with('/invalid-path')

    @override_settings_and_update_wp_conf(
        WEBPACKAGER_WEBCONFIG_PATH='valid_webconfig_path'
    )
    def test_relative_webconfig_path_should_raise(self):
        with self.assertRaises(exceptions.InvalidWebConfigPath):
            discover.get_settings_webconfigs()

    @override_settings_and_update_wp_conf(
        WEBPACKAGER_WEBCONFIG_PATH=join_basedir('valid_webconfig_dir')
    )
    def test_relative_webconfig_path_should_raise(self):
        dir = self.make_rel(discover.get_settings_webconfigs()['default'])
        self.assertEqual(dir, 'valid_webconfig_dir')

    @override_settings_and_update_wp_conf(
        WEBPACKAGER_WEBCONFIG_PATH={
            'valid_webconfig': join_basedir('valid_webconfig_dir'),
            'other_webconfig': join_basedir('other_webconfig'),
        }
    )
    def test_multiple_named_webconfig_paths_should_work(self):
        webconfigs = discover.get_settings_webconfigs()

        self.assertEqual(
            self.make_rel(webconfigs['valid_webconfig']),
            'valid_webconfig_dir'
        )
        self.assertEqual(
            self.make_rel(webconfigs['other_webconfig']),
            'other_webconfig'
        )


class GetAppWebappsDirTestCase(BaseWebpackagerTestCase):

    @override_settings_and_update_wp_conf(
        INSTALLED_APPS=settings.INSTALLED_APPS + ('tests.sample_app',)
    )
    def test_get_app_webapps_dir_from_default_settings(self):
        app = apps.get_app_config('sample_app')

        webapps_settings = discover.get_app_webapp(app)
        self.assertEqual(
            self.make_rel(webapps_settings['entrypoints']['abc']),
            'sample_app/webapps/abc/index.js'
        )
        app_webconfig = discover.get_app_webconfig(app)
        self.assertIs(app_webconfig, None)

    @override_settings_and_update_wp_conf(
        INSTALLED_APPS=settings.INSTALLED_APPS + (
            'tests.sample_app.apps.AppWithCustomWebconfigConfig',
        ),
        WEBPACKAGER_APPS_WEBAPPS_DIR='custom_project_webapps'
    )
    def test_get_app_webapps_dir_from_app_config(self):
        app = apps.get_app_config('sample_app')

        webapps_settings = discover.get_app_webapp(app)
        self.assertEqual(
            self.make_rel(webapps_settings['entrypoints']['cde']),
            'sample_app/custom_app_webapps/cde/index.js'
        )

        app_webconfig = discover.get_app_webconfig(app)
        self.assertEqual(
            self.make_rel(app_webconfig), 'sample_app/custom_app_webapps'
        )

    @override_settings_and_update_wp_conf(
        INSTALLED_APPS=settings.INSTALLED_APPS + ('tests.sample_app',),
        WEBPACKAGER_APPS_WEBAPPS_DIR='custom_project_webapps'
    )
    def test_get_app_webapps_dir_from_project_settings(self):
        app = apps.get_app_config('sample_app')
        webapps_settings = discover.get_app_webapp(app)

        self.assertEqual(
            self.make_rel(webapps_settings['entrypoints']['bcd']),
            'sample_app/custom_project_webapps/bcd/index.ts'
        )

        app_webconfig = discover.get_app_webconfig(app)
        self.assertIs(app_webconfig, None)
