# -*- coding: utf-8 -*-

from .models import Container

from django.contrib import admin


class ContainerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Container, ContainerAdmin)
