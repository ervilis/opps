# -*- coding: utf-8 -*-
from django.test import TestCase

from model_mommy import mommy

from ..models import Links


class ImageTest(TestCase):
    def setUp(self):
        self.link = mommy.make(Links)

    def test_exist(self):
        self.assertTrue(self.link)
