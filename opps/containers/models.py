# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import hmac
import json

from hashlib import sha1

from django.db import models
from django.db.models import Q
from django.db.models import Manager
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

    def __str__(self):
        return self.get_absolute_url()

    def __repr__(self):
        return self.__str__()

    class Meta:
        ordering = ['-date_available']
        verbose_name = _('Container')
        verbose_name_plural = _('Containers')
        unique_together = ("site", "uid")

    def save(self, *args, **kwargs):
        self.child_class = self.__class__.__name__
        self.child_module = self.__class__.__module__
        self.child_app_label = self._meta.app_label
        import pdb; pdb.set_trace()

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


@python_2_unicode_compatible
class QuerySet(Publishable, Channeling, Slugged):
    name = models.CharField(_(u"Dynamic queryset name"), max_length=140)

    model = models.CharField(_(u'Model'), max_length=150)
    limit = models.PositiveIntegerField(_(u'Limit'), default=7)
    offset = models.PositiveIntegerField(_(u'Offset'), default=0)
    order_field = models.CharField(
        _(u"Order Field"),
        max_length=100,
        default='id',
        help_text=_(u"Take care, should be an existing field or lookup")
    )
    order = models.CharField(_('Order'), max_length=1, choices=(
        ('-', 'DESC'), ('+', 'ASC')))

    recursive = models.BooleanField(
        _("Recursive"),
        help_text=_("Bring the content channels and subchannels (tree)"),
        default=False
    )

    filters = models.TextField(
        _(u'Filters'),
        help_text=_(u'Json format extra filters for queryset'),
        blank=True,
        null=True
    )

    excludes = models.TextField(
        _(u'Excludes'),
        help_text=_(u'Json format for queryset excludes'),
        blank=True,
        null=True
    )
    objects = Manager()

    def __init__(self, *args, **kwargs):
        """
        to avoid re-execution of methods
        its results are cached in a local storage
        per instance cache
        """
        super(QuerySet, self).__init__(*args, **kwargs)
        if not hasattr(self, 'local_cache'):
            self.local_cache = {}

    def __str__(self):
        return u"{0} {1} {2}".format(self.name, self.slug, self.model)

    def clean(self):

        if self.filters:
            try:
                json.loads(self.filters)
            except:
                raise ValidationError(_(u'Invalid JSON for filters'))

        if self.excludes:
            try:
                json.loads(self.excludes)
            except:
                raise ValidationError(_(u'Invalid JSON for excludes'))

        try:
            self.get_queryset().all()
        except Exception as e:
            raise ValidationError(
                u'Invalid Queryset: {0}'.format(str(e))
            )

        if self.offset >= self.limit:
            raise ValidationError(_(u'Offset can\'t be equal or higher than'
                                    u'limit'))

        if self.recursive:
            if not self.channel:
                raise ValidationError(_(u"To use recursion (channel) is "
                                        u"necessary to select a channel"))

    def get_queryset(self, content_group='default',
                     exclude_ids=None, use_local_cache=True):
        cached = self.local_cache.get('get_queryset')
        if use_local_cache and cached:
            return cached

        exclude_ids = exclude_ids or []

        import pdb; pdb.set_trace()
        _app, _model = self.model.split('.')
        model = models.get_model(_app, _model)

        queryset = model.objects.filter(
            published=True,
            date_available__lte=timezone.now(),
            site=self.site
        )

        try:
            if model._meta.get_field_by_name('show_on_root_channel'):
                queryset = queryset.filter(show_on_root_channel=True)
        except:
            pass  # silently pass when FieldDoesNotExists

        try:
            if self.channel and not self.channel.homepage:
                if self.recursive:
                    channel_long_slug = [self.channel.long_slug]
                    channel_descendants = self.channel.get_descendants(
                        include_self=False)
                    for children in channel_descendants:
                        channel_long_slug.append(children.long_slug)

                    queryset = queryset.filter(
                        channel_long_slug__in=channel_long_slug)
                else:
                    queryset = queryset.filter(
                        channel_long_slug=self.channel.long_slug)
        except:
            pass

        if self.filters:
            filters = json.loads(self.filters)

            for key, value in filters.iteritems():
                if value == "datetime.now()":
                    filters[key] = datetime.now()

            queryset = queryset.filter(**filters)

        if self.excludes:
            excludes = json.loads(self.excludes)

            for key, value in excludes.iteritems():
                if value == "datetime.now()":
                    excludes[key] = datetime.now()

            queryset = queryset.exclude(**excludes)

        # importing here to avoid circular imports
        from opps.containers.models import Container
        if issubclass(model, Container):
            queryset = queryset.exclude(
                id__in=exclude_ids
            )

        order_term = self.order_field or 'id'
        if self.order == '-':
            order_term = "-{0}".format(self.order_field or 'id')

        queryset = queryset.order_by(order_term)

        result = queryset[self.offset:self.limit]
        if use_local_cache:
            self.local_cache['get_queryset'] = result
        return result


class BaseBox(Publishable, Channeling, Slugged):
    name = models.CharField(_(u"Box name"), max_length=140)

    class Meta:
        abstract = True
        unique_together = ['site', 'channel_long_slug', 'slug']

    def __unicode__(self):
        return u"{0}-{1}".format(self.slug, self.site.name)
