# -*- coding: utf-8 -*-

from .models import Channel

from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


class ChannelAdmin(TreeAdmin):
    form = movenodeform_factory(Channel)


admin.site.register(Channel, ChannelAdmin)
