#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .conf import settings

from opps.core.cache import cache_page

#from .views import ContainerList, ContainerDetail
from .views import ContainerList


urlpatterns = patterns(
    '',
    #url(r'^$', ContainerList.as_view(), name='home'),

    url(r'^(?P<channel_long_slug>[\w\b//-]+)/$',
        cache_page(settings.OPPS_CACHE_EXPIRE_LIST)(
            ContainerList.as_view()), name='channel'),
)
