# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import polymorphic.showfields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('channels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_insert', models.DateTimeField(auto_now_add=True, verbose_name='Date insert')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Date update')),
                ('site_uid', models.PositiveIntegerField(db_index=True, max_length=4, null=True, verbose_name='Site id', blank=True)),
                ('site_domain', models.CharField(db_index=True, max_length=100, null=True, verbose_name='Site domain', blank=True)),
                ('date_available', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Date available', db_index=True)),
                ('published', models.BooleanField(default=False, db_index=True, verbose_name='Published')),
                ('uid', models.CharField(db_index=True, max_length=60, null=True, verbose_name='UID', blank=True)),
                ('child_class', models.CharField(db_index=True, max_length=30, null=True, verbose_name='Child class', blank=True)),
                ('child_module', models.CharField(db_index=True, max_length=120, null=True, verbose_name='Child module', blank=True)),
                ('child_app_label', models.CharField(db_index=True, max_length=30, null=True, verbose_name='Child app label', blank=True)),
            ],
            options={
                'ordering': ['-date_available'],
                'verbose_name': 'Container',
                'verbose_name_plural': 'Containers',
            },
            bases=(polymorphic.showfields.ShowFieldContent, models.Model),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('container_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='containers.Container')),
                ('slug', models.SlugField(max_length=150, verbose_name='Slug')),
                ('tags', models.CharField(help_text='A comma-separated list of tags.', max_length=4000, null=True, verbose_name='Tags', blank=True)),
                ('title', models.CharField(max_length=140, verbose_name='Title', db_index=True)),
                ('hat', models.CharField(max_length=140, null=True, verbose_name='Hat', blank=True)),
                ('headline', models.TextField(null=True, verbose_name='Headline', blank=True)),
                ('short_title', models.CharField(max_length=140, null=True, verbose_name='Short title', blank=True)),
                ('source', models.CharField(max_length=255, null=True, verbose_name='Source', blank=True)),
                ('show_on_root_channel', models.BooleanField(default=True, verbose_name='Show on root channel?')),
                ('content', models.TextField(verbose_name='Content')),
            ],
            options={
                'abstract': False,
            },
            bases=('containers.container', models.Model),
        ),
        migrations.AddField(
            model_name='container',
            name='channel',
            field=models.ManyToManyField(related_name=b'channeling_containers_container_sets+', null=True, verbose_name='Channel', to='channels.Channel', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='container',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name=b'polymorphic_containers.container_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='container',
            name='site',
            field=models.ForeignKey(default=1, to='sites.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='container',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='container',
            unique_together=set([('site', 'uid')]),
        ),
    ]
