# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Container


class ContainerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Container, ContainerAdmin)
