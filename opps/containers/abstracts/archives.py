# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from opps.core.models import Slugged
from opps.core.tags.models import Tagged
from opps.containers.models import Container


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = u"{0}-{1}.{2}".format(random.getrandbits(32),
                                     instance.slug[:100], ext)
    d = datetime.now()
    folder = u"archives/{0}".format(d.strftime("%Y/%m/%d/"))
    return os.path.join(folder, filename)


@python_2_unicode_compatible
class Archive(Container, Slugged, Tagged):
    title = models.CharField(_("Title"), max_length=140, db_index=True)
    archive = models.FileField(upload_to=get_file_path,
                               max_length=255,
                               verbose_name=_('Archive'),
                               null=True,
                               blank=True)
    archive_link = models.URLField(_("Archive URL"),
                                   max_length=255,
                                   null=True,
                                   blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)

    source = models.CharField(
        _('Source'),
        null=True, blank=True,
        max_length=255
    )

    class Meta:
        verbose_name = _('Archive')
        verbose_name_plural = _('Archives')
        unique_together = ['site', 'slug']
        abstract = True

    def __str__(self):
        return "{0}-{1}".format(self.site, self.slug)

    def clean(self):
        items = [self.archive, self.archive_link]
        if not any(items):
            raise ValidationError(_("You must fill archive or archive URL"))
        if all(items):
            raise ValidationError(_("Cannot set archive and archive URL"))

    def get_absolute_url(self):
        if self.date_available <= timezone.now() and self.published:
            return self.archive_link or self.archive.url
        return ""
