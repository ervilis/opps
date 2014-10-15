# -*- coding: utf-8 -*-
from django.db import models
from .conf import settings


def model_choices():
    try:
        m = tuple(sorted([
            (u"{0}.{1}".format(app._meta.app_label, app._meta.object_name),
             u"{0} - {1}".format(app._meta.app_label, app._meta.object_name))
            for app in models.get_models()
            if 'opps.containers.type' in app.__module__]))

        return tuple(sorted(m + settings.OPPS_CONTAINER_TYPES))
    except ImportError:
        return tuple([])
