# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Post, Album, Link


class PostAdmin(admin.ModelAdmin):
    pass


class AlbumAdmin(admin.ModelAdmin):
    pass


class LinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Album, AlbumAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Post, PostAdmin)
