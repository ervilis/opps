# -*- coding: utf-8 -*-
from django import forms
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _

from opps.core.forms import model_choices
from .models import QuerySet


class QuerySetAdminForm(forms.ModelForm):
    model = forms.ChoiceField(label=_(u'Model'),
                              choices=lazy(model_choices, tuple)())

    class Meta:
        model = QuerySet
