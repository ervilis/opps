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
                ('channel', models.ManyToManyField(related_name=b'channeling_containers_container_sets+', null=True, verbose_name='Channel', to='channels.Channel', blank=True)),
                ('polymorphic_ctype', models.ForeignKey(related_name=b'polymorphic_containers.container_set', editable=False, to='contenttypes.ContentType', null=True)),
                ('site', models.ForeignKey(default=1, to='sites.Site')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-date_available'],
                'verbose_name': 'Container',
                'verbose_name_plural': 'Containers',
            },
            bases=(polymorphic.showfields.ShowFieldContent, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='container',
            unique_together=set([('site', 'uid')]),
        ),
    ]
