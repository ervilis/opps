# -*- coding: utf-8 -*-
from django.conf import settings
from appconf import AppConf


class ThumborConf(AppConf):
    SECURITY_KEY = ''
    ENABLED = False
    MEDIA_URL = settings.MEDIA_URL
    SERVER = ""
    ARGUMENTS = {}

    class Meta:
        prefix = 'thumbor'
