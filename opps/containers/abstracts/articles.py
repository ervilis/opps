# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from opps.containers.models import Container
from opps.core.tags.models import Tagged
from opps.core.models import Slugged


@python_2_unicode_compatible
class Article(Container, Slugged, Tagged):
    title = models.CharField(_("Title"), max_length=140, db_index=True)
    hat = models.CharField(_("Hat"), max_length=140, null=True, blank=True)
    headline = models.TextField(_("Headline"), blank=True, null=True)
    short_title = models.CharField(_("Short title"), max_length=140,
                                   null=True, blank=True)
    source = models.CharField(_('Source'), null=True, blank=True,
                              max_length=255)
    show_on_root_channel = models.BooleanField(_("Show on root channel?"),
                                               default=True)

    def __str__(self):
        return unicode(self.get_absolute_url())

    def get_slug(self):
        return self.slug

    class Meta:
        abstract = True