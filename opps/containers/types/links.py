# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.containers.abstracts.articles import Article


class Link(Article):
    url = models.URLField(_(u"URL"), null=True, blank=True)
    container = models.ForeignKey(
        'containers.Container',
        null=True, blank=True,
        related_name='link_containers'
    )

    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def clean(self):
        if not self.url and not self.container:
            raise ValidationError(_('URL field is required.'))

        self.url = self.url
        if self.container:
            self.url = self.container.get_absolute_url()
