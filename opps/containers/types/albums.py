# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from opps.containers.abstracts.articles import Article


class Album(Article):
    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
