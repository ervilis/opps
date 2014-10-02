# -*- coding: utf-8 -*-
from django.test import TestCase

from model_mommy import mommy

from ..models import Album


class AlbumTest(TestCase):
    def setUp(self):
        self.album = mommy.make(Album)

    def test_exist(self):
        self.assertTrue(self.album)
