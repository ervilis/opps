# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_insert', models.DateTimeField(auto_now_add=True, verbose_name='Date insert')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Date update')),
                ('site_uid', models.PositiveIntegerField(db_index=True, max_length=4, null=True, verbose_name='Site id', blank=True)),
                ('site_domain', models.CharField(db_index=True, max_length=100, null=True, verbose_name='Site domain', blank=True)),
                ('date_available', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Date available', db_index=True)),
                ('published', models.BooleanField(default=False, db_index=True, verbose_name='Published')),
                ('slug', models.SlugField(max_length=150, verbose_name='Slug')),
                ('name', models.CharField(max_length=60, verbose_name='Name')),
<<<<<<< HEAD
                ('long_slug', models.CharField(db_index=True, max_length=250, null=True, verbose_name='Long slug', blank=True)),
=======
                ('long_slug', models.SlugField(max_length=250, verbose_name='Long Slug')),
>>>>>>> a4ecc7c1165f8e7dbf0dda2b04fad3a3efdb7e65
                ('layout', models.CharField(default=b'default', max_length=250, verbose_name='Layout', db_index=True)),
                ('description', models.CharField(max_length=255, null=True, verbose_name='Description', blank=True)),
                ('hat', models.CharField(max_length=255, null=True, verbose_name='Hat', blank=True)),
                ('show_in_menu', models.BooleanField(default=False, verbose_name='Show in menu?')),
                ('include_in_main_rss', models.BooleanField(default=True, verbose_name='Show in main RSS?')),
                ('homepage', models.BooleanField(default=False, help_text='Check only if this channel is the homepage. Should have only one homepage per site', verbose_name='Is home page?')),
                ('group', models.BooleanField(default=False, verbose_name='Group sub-channel?')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
                ('paginate_by', models.IntegerField(null=True, verbose_name='Paginate by', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name=b'subchannel', verbose_name='Parent', blank=True, to='channels.Channel', null=True)),
                ('site', models.ForeignKey(default=1, to='sites.Site')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Channel',
                'verbose_name_plural': 'Channels',
            },
            bases=(models.Model,),
        ),
    ]
