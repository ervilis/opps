# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from opps.containers.models import Container
from opps.core.models import Publishable, Slugged


<<<<<<< HEAD
class ChannelManager(TreeManager):
    def get_homepage(self, site):
        try:
            return super(ChannelManager, self).get_query_set().filter(
                site__domain=site, homepage=True, published=True).get()
        except Channel.DoesNotExist:
            return None


class Channel(MPTTModel, Publishable, Slugged):

    name = models.CharField(_(u"Name"), max_length=60)
    long_slug = models.CharField(_(u"Long slug"), max_length=250,
                                 db_index=True, null=True, blank=True)
    layout = models.CharField(_(u'Layout'), max_length=250, db_index=True,
=======
@python_2_unicode_compatible
class Channel(Publishable, Slugged, MP_Node):

    name = models.CharField(_("Name"), max_length=60)
    long_slug = models.SlugField(_("Long Slug"), max_length=250,
                                 db_index=True)
    layout = models.CharField(_('Layout'), max_length=250, db_index=True,
>>>>>>> a4ecc7c1165f8e7dbf0dda2b04fad3a3efdb7e65
                              default="default")
    description = models.CharField(_("Description"),
                                   max_length=255, null=True, blank=True)
    hat = models.CharField(_("Hat"),
                           max_length=255, null=True, blank=True)

    show_in_menu = models.BooleanField(_("Show in menu?"), default=False)
    include_in_main_rss = models.BooleanField(
        _("Show in main RSS?"),
        default=True
    )
    homepage = models.BooleanField(
        _("Is home page?"),
        default=False,
        help_text=_('Check only if this channel is the homepage.'
                    ' Should have only one homepage per site')
    )
<<<<<<< HEAD
    group = models.BooleanField(_(u"Group sub-channel?"), default=False)
    order = models.PositiveIntegerField(_(u"Order"), default=0)
    parent = TreeForeignKey('self', related_name='subchannel',
                            null=True, blank=True,
                            verbose_name=_(u'Parent'))
=======
    group = models.BooleanField(_("Group sub-channel?"), default=False)
    order = models.IntegerField(_("Order"), default=0)
>>>>>>> a4ecc7c1165f8e7dbf0dda2b04fad3a3efdb7e65
    paginate_by = models.IntegerField(_("Paginate by"), null=True, blank=True)
    objects = ChannelManager()


    class Meta:
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')

    def __str__(self):
        """ Uniform resource identifier
        http://en.wikipedia.org/wiki/Uniform_resource_identifier
        """
        return "/{}/".format(self._set_long_slug())

    def get_absolute_url(self):
        return "{}".format(self.__unicode__())

    def get_http_absolute_url(self):
        return "http://{}{}".format(self.site_domain, self.get_absolute_url())
    get_http_absolute_url.short_description = _('Get HTTP Absolute URL')

    @property
    def title(self):
        return self.name

    def clean(self):
        channel_is_home = Channel.objects.filter(
            site__id=settings.SITE_ID,
            homepage=True, published=True)
        if self.pk:
            channel_is_home = channel_is_home.exclude(pk=self.pk)

        if self.homepage and channel_is_home.exists():
            raise ValidationError('Exist home page!')

        super(Channel, self).clean()

    def _set_long_slug(self):
        if self.parent:
            return "{}/{}".format(self.parent.long_slug, self.slug)
        return "{}".format(self.slug)

    def save(self, *args, **kwargs):
        self.long_slug = self._set_long_slug()
        super(Channel, self).save(*args, **kwargs)
