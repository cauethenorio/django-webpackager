# coding: utf-8

import errno
import io
import os

from django.template import Context, Engine

from .exceptions import WebconfigCreationError


def create_webconfig_dir(target_dir):
    try:
        os.makedirs(target_dir)
    except OSError as e:
        # python2 compatible
        if e.errno == errno.EEXIST:
            raise WebconfigCreationError(
                "'{}' already exists".format(target_dir)
            )
        raise WebconfigCreationError(e)

    source_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'webconfig_template'
    )

    context = Context({
        'name': os.path.basename(target_dir)
    }, autoescape=False)

    for source_file in os.listdir(source_dir):
        source_path = os.path.join(source_dir, source_file)

        with io.open(source_path, 'r', encoding='utf-8') as source_file_content:
            content = source_file_content.read()

        template = Engine().from_string(content)
        content = template.render(context)

        target_file = '.'.join(source_file.split('.')[:-1])
        target_path = os.path.join(target_dir, target_file)

        write_file_content(target_path, content)


def write_file_content(file_path, content):
    with io.open(file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(content)
