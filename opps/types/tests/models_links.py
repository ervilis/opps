# -*- coding: utf-8 -*-
from django.test import TestCase

from model_mommy import mommy

from ..models import Link


class ImageTest(TestCase):
    def setUp(self):
        self.link = mommy.make(Link)

    def test_exist(self):
        self.assertTrue(self.link)
