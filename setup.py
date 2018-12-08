# coding: utf-8

import os
from setuptools import setup

from django_webpackager import about

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()


def get_requirements(env):
    with open(u'requirements-{}.txt'.format(env)) as fp:
        return [x.strip() for x in fp.read().split('\n') if not x.startswith('#')]


tests_require = get_requirements('test')


setup(
    name='django-webpackager',
    version=about.__version__,
    packages=['django_webpackager'],
    zip_safe=False,
    description='Zero-config highly customisable Django Webpack integrator',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Cauê Thenório',
    author_email='caue@thenorio.com.br',
    url='https://github.com/cauethenorio/django-webpackager/',
    keywords=['django', 'webpack', 'javascript', 'assets', 'npm'],
    license='MIT',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    extras_require={
        'tests': tests_require,
    },
    install_requires=[
        'Django>=1.8',
    ],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
    ],
)
