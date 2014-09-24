# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pkg_resources


pkg_resources.declare_namespace(__name__)

VERSION = (0, 3, 0)
__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = "Open Source Content Management Platform - CMS for the "
"magazines, newspappers websites and portals with "
"high-traffic, using the Django Framework."

__author__ = "Thiago Avelino"
__credits__ = ['Bruno Rocha']
__email__ = "thiago@avelino.xxx"
__license__ = "MIT"
__copyright__ = "Copyright 2014, Thiago Avelino"


OPPS_CORE_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',

    # Dependence
    'mptt',
    'south',

    # Opps Core
    'opps.core',
    'opps.channels',
    'opps.containers',
    'opps.types',
]
