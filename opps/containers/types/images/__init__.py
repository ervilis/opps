# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from opps.containers.abstracts.archives import Archive

from .generate import image_url as url


HALIGN_CHOICES = (
    ('left', _('Left')),
    ('center', _('Center')),
    ('right', _('Right'))
)
VALIGN_CHOICES = (
    ('top', _('Top')),
    ('middle', _('Middle')),
    ('bottom', _('Bottom'))
)


class Cropping(models.Model):
    crop_example = models.CharField(_("Crop Example"), max_length=255,
                                    null=True, blank=True)
    crop_x1 = models.PositiveSmallIntegerField(default=0, null=True,
                                               blank=True)
    crop_x2 = models.PositiveSmallIntegerField(default=0, null=True,
                                               blank=True)
    crop_y1 = models.PositiveSmallIntegerField(default=0, null=True,
                                               blank=True)
    crop_y2 = models.PositiveSmallIntegerField(default=0, null=True,
                                               blank=True)
    flip = models.BooleanField(_('Flip'), default=False,
                               help_text=_('Flag that indicates that '
                                           'thumbor should flip '
                                           'horizontally (on the vertical '
                                           'axis) the image'))
    flop = models.BooleanField(_('Flop'), default=False,
                               help_text=_('Flag that indicates that '
                                           'thumbor should flip '
                                           'vertically (on the horizontal '
                                           'axis) the image'))
    halign = models.CharField(_('Horizontal Align'), default=False,
                              max_length=6,
                              null=True, blank=True,
                              choices=HALIGN_CHOICES,
                              help_text=_('Horizontal alignment that '
                                          'thumbor should use for cropping'))
    valign = models.CharField(_('Vertical Align'), default=False,
                              max_length=6,
                              null=True, blank=True,
                              choices=VALIGN_CHOICES,
                              help_text=_('Vertical alignment that '
                                          'thumbor should use for cropping'))

    fit_in = models.BooleanField(_('Fit in'), default=False,
                                 help_text=_('Flag that indicates that '
                                             'thumbor should fit the image '
                                             'in the box defined by width x '
                                             'height'))

    smart = models.BooleanField(_('Smart'), default=False,
                                help_text=_('Flag that indicates that'
                                            ' thumbor should use smart '
                                            'cropping'))

    class Meta:
        abstract = True

    def clean(self):
        super(Cropping, self).clean()

    def save(self, *args, **kwargs):
        if self.archive and settings.THUMBOR_ENABLED:
            self.crop_example = self.archive.url
        else:
            self.crop_example = self.image_url()

        super(Cropping, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Image(Archive, Cropping):

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return "{0}-{1}".format(self.site, self.slug)

    def clean(self):
        items = ['x1', 'x2', 'y1', 'y2']
        for item in items:
            prop = getattr(self, 'crop_' + item, None)
            if not prop or prop is None or prop in ['', ' ']:
                setattr(self, 'crop_' + item, 0)

        if self.archive and settings.THUMBOR_ENABLED:
            self.crop_example = self.archive.url
        else:
            self.crop_example = self.image_url()

        super(Image, self).clean()

    def image_url(self, *args, **kwargs):
        if self.archive:
            return url(self.archive.url, *args, **kwargs)
        elif self.archive_link:
            return self.archive_link
        return ''
