# -*- coding: utf-8 -*-
from django.test import TestCase

from model_mommy import mommy

from ..models import Image


class ImageTest(TestCase):
    def setUp(self):
        self.image = mommy.make(Image)

    def test_exist(self):
        self.assertTrue(self.image)
