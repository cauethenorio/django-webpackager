# coding: utf-8

import fnmatch
import importlib
import os

from django.conf import settings

from . import exceptions


def is_valid_webconfig_dir(path, name=None, throw_error=False):
    package_json_path = os.path.join(path, 'package.json')

    if os.path.isfile(package_json_path):
        return True

    if not throw_error:
        return False

    raise exceptions.InvalidWebConfigPath(
        "The '{}' web-config directory is not valid: No package.json "
        "file found at '{}'".format(name, package_json_path)
    )


def get_app_webconfig(app):
    if hasattr(app, 'webpackager_webconfig_dir'):
        config_dir = app.webpackager_webconfig_dir
    elif hasattr(settings, 'WEBPACKAGER_APPS_WEBCONFIG_DIR'):
        config_dir = settings.WEBPACKAGER_APPS_WEBCONFIG_DIR
    else:
        config_dir = 'webapps'

    config_path = os.path.join(app.path, config_dir)

    if is_valid_webconfig_dir(config_path):
        return {'path': config_path}


def get_app_webapp(app):
    if hasattr(app, 'webpackager_webapps_dir'):
        webapps_dir = app.webpackager_webapps_dir
    elif hasattr(settings, 'WEBPACKAGER_APPS_WEBAPPS_DIR'):
        webapps_dir = settings.WEBPACKAGER_APPS_WEBAPPS_DIR
    else:
        webapps_dir = 'webapps'

    webapps_path = os.path.join(app.path, webapps_dir)
    entrypoints = get_entrypoints(webapps_path)

    if entrypoints != {}:
        return {
            'app_name': app.label,
            'entrypoints': entrypoints,
            'output_path': os.path.join(app.path, 'static'),
            'config_name': getattr(app, 'webpackager_webconfig_name', None)
        }


def get_settings_webconfigs():
    if hasattr(settings, 'WEBPACKAGER_WEBCONFIG_DIR'):
        settings_webconfig_dir = settings.WEBPACKAGER_WEBCONFIG_DIR

        if isinstance(settings_webconfig_dir, str):
            settings_webconfig_dir = {'default': settings_webconfig_dir}

        for name, path in settings_webconfig_dir.items():
            is_valid_webconfig_dir(path, name, throw_error=True)

        return {
            name: {'path': path}
            for name, path in settings_webconfig_dir.items()
        }


def get_project_webapps_layout(apps):
    configs = get_settings_webconfigs()
    found_webapps = []

    for app in apps.get_app_configs():
        app_name = app.label

        app_webconfig = get_app_webconfig(app)
        app_webapp = get_app_webapp(app)

        if app_webconfig is not None:
            if app_name in configs.keys():
                raise exceptions.DuplicatedWebConfigName()
            else:
                configs[app_name] = app_webconfig

        if app_webapp is not None:
            found_webapps.append(app_webapp)

            if app_webapp['config_name'] is None:
                if app_webconfig is not None:
                    app_webapp['config_name'] = app_name
                else:
                    app_webapp['config_name'] = 'default'

    for app in found_webapps:
        config_name = app['config_name']

        if config_name not in configs:
            raise exceptions.InexistentWebConfig(
                "Web-config '{}' used by app '{}' doesn't exist".format(
                    config_name, app['app_name']
                ) if config_name != 'default' else

                "App '{}' have no web-config defined neither a default "
                "web-config was specified".format(app['app_name'])
            )

        configs[config_name].setdefault('apps', []).append(app)
        del app['config_name']


    # filter out webconfigs which are not used by any app
    return {
        name: data for name, data in configs.items()
        if data.get('apps') is not None
    }


def get_entrypoints(webapps_dir):
    entrypoints = {}

    if os.path.isdir(webapps_dir):
        for webapp_dir in os.listdir(webapps_dir):
            webapp_path = os.path.join(webapps_dir, webapp_dir)

            for file in os.listdir(webapp_path):
                if fnmatch.fnmatch(file, 'index.*'):
                    entrypoints[webapp_dir] = os.path.join(webapp_path, file)

    return entrypoints


def get_project_rootdir():
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
    settings_path = importlib.import_module(settings_module).__file__

    project_root = os.path.dirname(settings_path)
    return project_root
