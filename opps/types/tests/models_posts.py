# -*- coding: utf-8 -*-
from django.test import TestCase

from model_mommy import mommy

from ..models import Post


class PostTest(TestCase):
    def setUp(self):
        self.post = mommy.make(Post)

    def test_exist_post(self):
        self.assertTrue(self.post)
