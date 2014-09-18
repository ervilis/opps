#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
from django.conf import settings
from django.core import management


settings.configure()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Opps CMS bin file')
    parser.add_argument('operation', help='task to be performed',
                        choices=['startproject', 'exportcontainerbox'])
    parser.add_argument("project_name", help="Project name", type=str)

    args = parser.parse_args()
    if args.operation == 'startproject':
        management.call_command(
            'startproject', args.project_name,
            template='https://github.com/opps/opps-project-template/zipball/'
            'master',
            extensions=('py', 'md', 'dev')
        )

    elif args.operation == 'exportcontainerbox':
        os.environ['DJANGO_SETTINGS_MODULE'] = args.project_name
        from django.core import serializers
        from opps.channels.models import Channel
        from opps.containers.models import ContainerBox
        from opps.boxes.models import QuerySet
        models = [Channel, ContainerBox, QuerySet]
        for m in models:
            data = serializers.serialize("json", m.objects.all())
            out = open("opps_{}.json".format(m.__class__.__name__), "w")
            out.write(data)
            out.close()
    else:
        pass
