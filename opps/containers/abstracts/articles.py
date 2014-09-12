# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.containers.models import Container
from opps.core.tags.models import Tagged


class Article(Container, Tagged):
    title = models.CharField(_(u"Title"), max_length=140, db_index=True)
    hat = models.CharField(_(u"Hat"), max_length=140, null=True, blank=True)
    headline = models.TextField(_(u"Headline"), blank=True, null=True)
    short_title = models.CharField(_(u"Short title"), max_length=140,
                                   null=True, blank=True)
    source = models.CharField(_('Source'), null=True, blank=True,
                              max_length=255)
    show_on_root_channel = models.BooleanField(_(u"Show on root channel?"),
                                               default=True)

    class Meta:
        abstract = True
