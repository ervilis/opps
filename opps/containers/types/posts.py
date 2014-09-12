# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..abstracts.articles import Article


class Post(Article):
    content = models.TextField(_(u"Content"))
