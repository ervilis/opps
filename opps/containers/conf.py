# -*- coding: utf-8 -*-
from django.conf import settings
from appconf import AppConf

from .types.images.conf import ThumborConf


class OppsContainerConf(AppConf):

    CACHE_EXPIRE_LIST = 5
    PAGINATE_BY = 10
    VIEWS_LIMIT = 10
    CONTAINER_TYPES = ()

    class Meta:
        prefix = 'opps'
