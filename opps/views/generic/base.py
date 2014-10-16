# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django import template
from django.conf import settings
from django.contrib.sites.models import get_current_site

from opps.conf import settings
from opps.types.models import Album
from opps.containers.models import Container
from opps.channels.models import Channel


class View(object):

    context_object_name = "context"
    paginate_by = settings.OPPS_PAGINATE_BY
    limit = settings.OPPS_VIEWS_LIMIT
    page_kwarg = 'page'

    def __init__(self, *args, **kwargs):
        self.slug = None
        self.channel = None
        self.long_slug = None
        self.article = None
        self.child_class = u'container'
        self.channel_long_slug = []
        self.excluded_ids = set()
        super(View, self).__init__(*args, **kwargs)

    def get_paginate_by(self, queryset):
        queryset = self.get_queryset()

        setting_name = 'OPPS_{0}_{1}_PAGINATE_BY'.format(queryset.
                                                         model._meta.app_label,
                                                         queryset.model.
                                                         __name__).upper()

        by_settings = getattr(settings, setting_name, self.paginate_by)
        by_request = self.request.GET.get('paginate_by')
        by_channel = getattr(self.channel, 'paginate_by', None)

        return by_request or by_channel or by_settings

    def get_context_data(self, **kwargs):
        context = {}

        # channel is needed everywhere
        self.channel = self.channel or Channel.objects.all()[0].get_homepage(
            site=get_current_site(self.request)
        )

        if not self.channel and getattr(
                settings, 'OPPS_MULTISITE_FALLBACK', None):
            self.channel = Channel.objects.filter(
                homepage=True, published=True)[:1].get()
            context['channel'] = self.channel

        if not self.long_slug:
            return context
        context = super(View, self).get_context_data(**kwargs)

        obj_filter = {}
        obj_filter['site_domain'] = self.site.domain
        obj_filter['date_available__lte'] = timezone.now()

        obj_filter['published'] = True

        filters = obj_filter
        filters['channel__in'] = Channel.objects.filter(
            long_slug__in=self.channel_long_slug)


        is_paginated = self.page_kwarg in self.request.GET
        if self.channel and self.channel.is_root_node() and not is_paginated:
            filters['show_on_root_channel'] = True
        article = Container.objects.filter(**filters)

        context['posts'] = article.filter(
            child_class='Post'
        ).exclude(pk__in=self.excluded_ids)[:self.limit]

        context['albums'] = Album.objects.filter(
            **filters
        ).exclude(pk__in=self.excluded_ids)[:self.limit]

        context['channel'] = {}
        context['channel']['long_slug'] = self.long_slug
        if self.channel:
            context['channel'] = self.channel

        context['breadcrumb'] = self.get_breadcrumb()

        if self.slug:
            try:
                context['next'] = self.get_object()\
                    .get_next_by_date_insert(**obj_filter)
            except self.get_object().DoesNotExist:
                pass
            try:
                context['prev'] = self.get_object()\
                    .get_previous_by_date_insert(**obj_filter)
            except self.get_object().DoesNotExist:
                pass

        if self.request.META.get('HTTP_X_PJAX', False) or\
           self.request.is_ajax():
            context['extends_parent'] = 'base_ajax.html'

        return context

    def get_template_folder(self):
        domain_folder = "containers"
        if self.site.id > 1:
            domain_folder = "{0}/containers".format(self.site.domain)
        return domain_folder

    def get_long_slug(self):
        self.long_slug = self.kwargs.get('channel_long_slug', None)
        try:
            if not self.long_slug:
                self.long_slug = Channel.objects.get_homepage(
                    site=self.site).long_slug
        except AttributeError:
            pass
        return self.long_slug

    def set_channel_rules(self):
        self.fallback = getattr(settings, 'OPPS_MULTISITE_FALLBACK', False)
        filters = dict(
            site__domain=self.site.domain,
            long_slug=self.long_slug,
            date_available__lte=timezone.now(),
            published=True
        )

        try:
            self.channel = Channel.objects.get(**filters)
        except Channel.DoesNotExist:
            if not self.fallback or self.site == self.site_master:
                raise Http404('Channel not found and fallback disabled')
            filters['site__domain'] = self.site_master.domain
            self.channel = get_object_or_404(Channel, **filters)

        self.long_slug = self.channel.long_slug

        self.channel_long_slug = [self.long_slug]
        self.channel_descendants = self.channel.get_descendants(
            include_self=False)
        for children in self.channel_descendants:
            self.channel_long_slug.append(children.long_slug)

    def get_breadcrumb(self):
        try:
            if self.channel.is_root_node():
                return []
        except:
            return []

        return self.channel.get_ancestors(include_self=True)

    def check_template(self, _template):
        try:
            template.loader.get_template(_template)
            return True
        except template.TemplateDoesNotExist:
            return False
