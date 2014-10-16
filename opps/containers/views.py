# -*- coding: utf-8 -*-

from opps.containers.models import Container
from opps.views.generic.list import ListView


class ContainerList(ListView):
    model = Container
