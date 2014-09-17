# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import hmac
import json

from hashlib import sha1

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from django.utils.encoding import python_2_unicode_compatible

from polymorphic import PolymorphicModel
from polymorphic.showfields import ShowFieldContent

from opps.core.cache import _cache_key
from opps.core.models import Publishable, Slugged, Channeling
from opps.core.managers import PublishableManager


@python_2_unicode_compatible
class Container(PolymorphicModel, ShowFieldContent, Publishable, Channeling):
    uid = models.CharField(
        _('UID'),
        max_length=60,
        null=True, blank=True,
        db_index=True
    )
    child_class = models.CharField(
        _('Child class'),
        max_length=30,
        null=True, blank=True,
        db_index=True
    )
    child_module = models.CharField(
        _('Child module'),
        max_length=120,
        null=True, blank=True,
        db_index=True
    )
    child_app_label = models.CharField(
        _('Child app label'),
        max_length=30,
        null=True, blank=True,
        db_index=True
    )

    objects = PublishableManager()

    def __str__(self):
        return unicode(self.get_absolute_url())

    def __repr__(self):
        val = self.__unicode__()
        if isinstance(val, str):
            return val
        elif not isinstance(val, unicode):
            val = unicode(val)
        return val.encode('utf8')

    class Meta:
        ordering = ['-date_available']
        verbose_name = _('Container')
        verbose_name_plural = _('Containers')
        unique_together = ("site", "uid")

    def save(self, *args, **kwargs):
        self.child_class = self.__class__.__name__
        self.child_module = self.__class__.__module__
        self.child_app_label = self._meta.app_label

        if not self.id:
            new_uuid = uuid.uuid4()
            self.uid = hmac.new(new_uuid.bytes, digestmod=sha1).hexdigest()

        super(Container, self).save(*args, **kwargs)

    def get_slug(self):
        return self.uid

    def get_absolute_url(self):
        if not self.channel.exists():
            return "/{}.html".format(self.get_slug())
        return "/{}/{}.html".format(self.channel.all()[0].long_slug,
                                    self.get_slug())

    def get_http_absolute_url(self):
        return "http://{}{}".format(self.site_domain, self.get_absolute_url())
    get_http_absolute_url.short_description = _('Get HTTP Absolute URL')

    @classmethod
    def get_children_models(cls):
        children = models.get_models()
        return [model for model in children
                if (model is not None and
                    issubclass(model, cls) and
                    model is not cls)]

    def custom_fields(self):
        if not self.json:
            return
        return json.loads(self.json)
