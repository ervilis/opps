# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms

from mptt.forms import MoveNodeForm

from .models import Channel


class ChannelAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChannelAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['slug'].widget.attrs['readonly'] = True

    class Meta:
        model = Channel
