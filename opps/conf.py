# -*- coding: utf-8 -*-
from django.conf import settings
from appconf import AppConf

from opps.containers.conf import OppsContainerConf, ThumborConf


class HaystackConf(AppConf):
    CONNECTIONS = {}

    class Meta:
        prefix = 'haystack'
