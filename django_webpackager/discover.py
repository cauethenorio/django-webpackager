# coding: utf-8

import fnmatch
import os

from django.conf import settings
from django.apps import apps

from .conf import wp_settings
from . import exceptions


def is_valid_webconfig_dir(path):
    if not os.path.isabs(path):
        return False

    package_json_path = os.path.join(path, 'package.json')
    if not os.path.isfile(package_json_path):
        return False

    return True


def get_app_webapps_dir(app):
    webapps_dir = getattr(
        app, 'webpackager_webapps_dir',
        wp_settings.APPS_WEBAPPS_DIR
    )
    return os.path.join(app.path, webapps_dir)


def get_app_webconfig(app):
    config_path = get_app_webapps_dir(app)

    if is_valid_webconfig_dir(config_path):
        return config_path


def get_app_webapp(app):
    webapps_path = get_app_webapps_dir(app)
    entrypoints = get_entrypoints(webapps_path)

    if entrypoints != {}:
        return {
            'app_name': app.label,
            'entrypoints': entrypoints,
            'output_path': os.path.join(app.path, 'static'),
            'config_name': getattr(app, 'webpackager_webconfig_name', None)
        }


def get_settings_webconfigs():
    webconfig_dirs = getattr(
        settings, 'WEBPACKAGER_WEBCONFIG_PATH',
        wp_settings.DEFAULT_WEBCONFIG_PATH
    )

    if isinstance(webconfig_dirs, str):
        webconfig_dirs = {'default': webconfig_dirs}

    webconfig_keys = list(webconfig_dirs.keys())

    for name, path in webconfig_dirs.items():
        if not is_valid_webconfig_dir(path):
            if len(webconfig_keys) == 1 and webconfig_keys[0] == 'default':
                raise exceptions.InvalidWebConfigPath(
                    "No valid webconfig dir was found. Tried: {}".format(path)
                )
            raise exceptions.InvalidWebConfigPath(
                "The specified '{}' webconfig directory is not "
                "valid: {}".format(name, path)
            )

    return webconfig_dirs


def get_project_webapps_layout():
    configs = get_settings_webconfigs()
    found_webapps = []

    # iterate over all apps to get their webapps and webconfigs
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

    layout = {}

    # TODO: replace all web-config text with webconfig

    # iterate again to resolve apps 'config_name's
    # and add apps to configs mapping
    # we need all apps webconfigs found to resolve that
    for app in found_webapps:
        config_name = app['config_name']

        if config_name not in configs:
            raise exceptions.InexistentWebConfig(
                "Webconfig '{}' used by app '{}' doesn't exist".format(
                    config_name, app['app_name']
                ) if config_name != 'default' else

                "App '{}' have no webconfig defined neither a default "
                "webconfig was specified".format(app['app_name'])
            )

        layout[config_name] = layout.get(config_name, {})
        layout[config_name].setdefault('apps', []).append(app)
        del app['config_name']

    return layout


def get_entrypoints(webapps_dir):
    entrypoints = {}

    if os.path.isdir(webapps_dir):
        for webapp_dir in os.listdir(webapps_dir):
            webapp_path = os.path.join(webapps_dir, webapp_dir)

            if not os.path.isdir(webapp_path):
                continue

            for file in os.listdir(webapp_path):
                if fnmatch.fnmatch(file, 'index.*'):
                    entrypoints[webapp_dir] = os.path.join(webapp_path, file)

    return entrypoints



