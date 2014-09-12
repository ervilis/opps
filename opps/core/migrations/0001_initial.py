# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_insert', models.DateTimeField(auto_now_add=True, verbose_name='Date insert')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Date update')),
                ('slug', models.SlugField(max_length=150, verbose_name='Slug')),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('slug', 'name')]),
        ),
    ]
