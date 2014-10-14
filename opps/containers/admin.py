# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules

from .models import QuerySet, Container
from .forms import QuerySetAdminForm


class ContainerAdmin(admin.ModelAdmin):
    pass


@apply_opps_rules('container')
class QuerySetAdmin(admin.ModelAdmin):
    form = QuerySetAdminForm
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    raw_id_fields = ['channel']
    readonly_fields = ['data_sample']
    search_fields = ['channel__name', 'channel__long_slug', 'name', 'slug']
    exclude = ('user',)

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Rules'), {
            'fields': ('model', 'order', 'order_field',
                       'offset', 'limit', 'channel', 'recursive', 'filters',
                       'excludes')}),
        (_(u'Publication'), {
            'classes': ('extrapretty',),
            'fields': ('published', 'date_available')}),
        (_(u'Data sample'), {
            'classes': ('extrapretty',),
            'fields': ('data_sample',)}),
    )

    def data_sample(self, obj):
        html = []
        qs = obj.get_queryset()
        count = qs.count()

        if count:
            html.append(u'<strong>Items:</strong> {0}<ul>'.format(count))
            for item in qs:
                html.append(u"<li>{0}</li>".format(item))
            html.append(u'</ul>')
        else:
            html.append(u'<ul><li>No data</li></ul>')

        return u''.join(html)
    data_sample.short_description = _(u'Data sample')
    data_sample.allow_tags = True


admin.site.register(Container, ContainerAdmin)
admin.site.register(QuerySet, QuerySetAdmin)
