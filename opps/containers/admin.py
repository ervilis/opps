# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Container
from .types.posts import Post


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
