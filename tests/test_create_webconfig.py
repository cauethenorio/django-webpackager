import functools
import os

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management import call_command
from django.test import TestCase

from django_webpackager.exceptions import WebconfigCreationError
from django_webpackager.webconfig import create_webconfig_dir

from .utils import override_settings_and_update_wp_conf, mock


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def patch_create_webconfig_dir(test_func):
    @functools.wraps(test_func)
    @mock.patch(
        'django_webpackager.management.commands.'
        'webpackager-create-webconfig.webconfig.create_webconfig_dir'
    )
    def patch_wrapper(*args, **kwargs):
        return test_func(*args, **kwargs)
    return patch_wrapper


class CreateWebconfigTest(TestCase):

    @patch_create_webconfig_dir
    def test_non_existent_app_should_raise(self, patch):
        with self.assertRaisesMessage(CommandError, 'No installed app'):
            call_command('webpackager-create-webconfig', app='non-existent')

    @override_settings_and_update_wp_conf(
        WEBPACKAGER_APPS_WEBAPPS_DIR='custom_webapps_dir',
        INSTALLED_APPS=settings.INSTALLED_APPS + ('tests.app_with_webapps',)
    )
    @patch_create_webconfig_dir
    def test_valid_app_should_create_inside_app_dir(self, patch):
        app = 'app_with_webapps'
        call_command('webpackager-create-webconfig', app=app)
        patch.assert_called_once_with(
            os.path.join(BASE_DIR, app, 'custom_webapps_dir')
        )

    @patch_create_webconfig_dir
    def test_absolute_dir_should_be_accepted(self, patch):
        abs_path = '/some/absolute/path'
        call_command('webpackager-create-webconfig', dir=abs_path)
        patch.assert_called_once_with(abs_path)

    @patch_create_webconfig_dir
    def test_relative_path_should_be_resolved(self, patch):
        rel_path = 'random-dir-name'
        call_command('webpackager-create-webconfig', dir=rel_path)
        patch.assert_called_once_with(os.path.join(os.getcwd(), rel_path))

    @override_settings_and_update_wp_conf(
        WEBPACKAGER_DEFAULT_WEBCONFIG_DIRNAME='thats-default-webconfig'
    )
    @patch_create_webconfig_dir
    def test_no_argument_should_use_create_dir_on_project_root(self, patch):
        call_command('webpackager-create-webconfig')
        patch.assert_called_once_with(
            os.path.join(BASE_DIR, 'thats-default-webconfig')
        )

    def test_existing_target_should_raise(self):
        with self.assertRaisesMessage(WebconfigCreationError, 'already exists'):
            create_webconfig_dir(BASE_DIR)

    @mock.patch('django_webpackager.webconfig.os.makedirs')
    @mock.patch('django_webpackager.webconfig.write_file_content')
    def test_ok_target_should_create_files(self, write_file_stub, makedirs_stub):
        create_webconfig_dir('/dest')
        makedirs_stub.assert_called_once_with('/dest')

        file_path, file_content = write_file_stub.call_args[0]
        self.assertEqual(file_path, '/dest/package.json')
        self.assertNotIn('{{', file_content)
        self.assertNotIn('{%', file_content)
        self.assertIn('devDependencies', file_content)
