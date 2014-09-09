# -*- coding: utf-8 -*-
import uuid
import hmac

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

from polymorphic import PolymorphicModel
from polymorphic.showfields import ShowFieldContent

from opps.core.cache import _cache_key
from opps.core.models import Publishable, Slugged, Channeling


class Container(PolymorphicModel, ShowFieldContent, Channeling, Publishable):
    uid = models.CharField(
        _(u'UID'),
        max_length=60,
        null=True, blank=True,
        db_index=True
    )
    child_class = models.CharField(
        _(u'Child class'),
        max_length=30,
        null=True, blank=True,
        db_index=True
    )
    child_module = models.CharField(
        _(u'Child module'),
        max_length=120,
        null=True, blank=True,
        db_index=True
    )
    child_app_label = models.CharField(
        _(u'Child app label'),
        max_length=30,
        null=True, blank=True,
        db_index=True
    )

    def __unicode__(self):
        return u"{}".format(self.get_absolute_url())

    def __repr__(self):
        val = self.__unicode__()
        if isinstance(val, str):
            return val
        elif not isinstance(val, unicode):
            val = unicode(val)
        return val.encode('utf8')

    class Meta:
        ordering = ['-date_available']
        verbose_name = _(u'Container')
        verbose_name_plural = _(u'Containers')
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
        if self.slug:
            return self.slug
        if self.title:
            return slugify(self.title)
        if self.name:
            return slugify(self.name)
        return self.uid

    def get_absolute_url(self):
        if not self.channel:
            return u"/{}.html".format(self.get_slug())
        return u"/{}/{}.html".format(self.channel_long_slug, self.get_slug())

    def get_http_absolute_url(self):
        return u"http://{}{}".format(self.site_domain, self.get_absolute_url())
    get_http_absolute_url.short_description = _(u'Get HTTP Absolute URL')

    @classmethod
    def get_children_models(cls):
        children = models.get_models()
        return [model for model in children
                if (model is not None and
                    issubclass(model, cls) and
                    model is not cls)]

    def inbox(self, containerbox=None):
        obj = ContainerBoxContainers.objects
        if containerbox:
            return obj.get(container=self.id,
                           containerbox__slug=containerbox)
        return obj.filter(container=self.id)

    def custom_fields(self):
        import json
        if not self.json:
            return
        return json.loads(self.json)
