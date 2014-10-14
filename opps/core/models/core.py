# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.redirects.models import Redirect
from django.utils import timezone
from django.utils.text import slugify

from ..managers import PublishableManager


class Date(models.Model):
    date_insert = models.DateTimeField(_(u"Date insert"), auto_now_add=True)
    date_update = models.DateTimeField(_(u"Date update"), auto_now=True)

    class Meta:
        abstract = True


class Owned(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True, null=True)

    class Meta:
        abstract = True


class Publishable(Date, Owned):
    site = models.ForeignKey(Site, default=1)
    site_uid = models.PositiveIntegerField(
        _(u"Site id"),
        max_length=4,
        null=True, blank=True,
        db_index=True)
    site_domain = models.CharField(
        _(u"Site domain"),
        max_length=100,
        null=True, blank=True,
        db_index=True)
    date_available = models.DateTimeField(
        _(u"Date available"),
        default=timezone.now,
        null=True,
        db_index=True)
    published = models.BooleanField(
        _(u"Published"),
        default=False,
        db_index=True)

    objects = PublishableManager()
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.site_domain = self.site.domain
        self.site_iid = self.site.id
        super(Publishable, self).save(*args, **kwargs)

    def is_published(self):
        return self.published and self.date_available <= timezone.now()


class Channeling(models.Model):
    channel = models.ManyToManyField(
        'channels.Channel',
        verbose_name=_(u"Channel"),
        related_name="channeling_%(app_label)s_%(class)s_sets+",
        null=True, blank=True
    )
    show_on_root_channel = models.BooleanField(
        _(u"Show on root channel?"),
        default=True
    )

    class Meta:
        abstract = True


class Slugged(models.Model):

    slug = models.SlugField(
        _(u"Slug"),
        db_index=True,
        max_length=150,
    )

    def slugfield(self):
        try:
            return slugify(self.title)
        except:
            return slugify(self.name)

    def clean(self):

        if self.slug in ("", None):
            try:
                self.slug = self.slugfield()
            except:
                pass

        self.validate_slug()

        if hasattr(self, 'get_absolute_url'):
            try:
                path = self.get_absolute_url()
            except:
                path = self.slug  # when get_absolute_url fails

            site = self.site or Site.objects.get(pk=1)
            redirect = Redirect.objects.filter(
                site=site,
                old_path=path
            )
            if redirect.exists():
                raise ValidationError(
                    _(u"The URL already exists as a redirect")
                )

        try:
            super(Slugged, self).clean()
        except AttributeError:
            pass  # does not implement the clean method

    def validate_slug(self):
        slug = getattr(self, 'slug', None)
        site = getattr(self, 'site', None)

        filters = {'slug': slug, 'site': site}

        if hasattr(self, 'channel'):
            filters['channel__in'] = [c for c in self.channel.all()]

        if hasattr(self, 'parent'):
            filters['parent'] = self.parent

        # if model does not have site
        if not getattr(self, 'site', False):
            del filters['site']

        slug_exists = self.__class__.objects.filter(**filters)

        if getattr(self, 'pk', None):
            slug_exists = slug_exists.exclude(pk=self.pk)

        if slug_exists:
            last = slug_exists.latest('slug').slug
            suffix = last.split('-')[-1]
            if suffix.isdigit():
                suffix = int(suffix) + 1
                self.slug = "{0}-{1}".format(self.slug, suffix)
            else:
                self.slug = "{0}-1".format(self.slug)

    def save(self, *args, **kwargs):
        if hasattr(self, 'get_absolute_url'):
            model = self.__class__
            if self.pk is not None:
                old_object = model.objects.get(pk=self.pk)
                if old_object.slug != self.slug:
                    redirect = Redirect(
                        site=self.site,
                        old_path=old_object.get_absolute_url(),
                        new_path=self.get_absolute_url()
                    )
                    redirect.save()

        super(Slugged, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['site', 'slug']
        abstract = True
