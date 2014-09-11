# -*- coding: utf-8 -*-
from .models import Channel

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .forms import ChannelAdminForm


class ChannelAdmin(MPTTModelAdmin):
    form = ChannelAdminForm
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'parent', 'site', 'homepage', 'order',
                    'show_in_menu', 'date_available', 'published']
    raw_id_fields = ['parent']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'parent', 'name', 'slug', 'layout', 'hat',
                       'description', 'order', (
                           'show_in_menu', 'include_in_main_rss', 'homepage'),
                       'group', 'paginate_by')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def save_model(self, request, obj, form, change):
        long_slug = u"{}".format(obj.slug)
        if obj.parent:
            long_slug = u"{}/{}".format(obj.parent.slug, obj.slug)
        obj.long_slug = long_slug
        super(ChannelAdmin, self).save_model(request, obj, form, change)


admin.site.register(Channel, ChannelAdmin)
