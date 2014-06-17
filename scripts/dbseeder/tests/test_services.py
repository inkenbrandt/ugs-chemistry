#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_services
----------------------------------

Tests for `services` module.
"""
import unittest
from dbseeder.services import Caster


class TestCaster(unittest.TestCase):

    def test_empty_string_returns_none(self):
        actual = Caster.cast('', 'TEXT')
        self.assertIsNotNone(actual, msg='text')

        actual = Caster.cast('', 'LONG')
        self.assertIsNone(actual, msg='long')

        actual = Caster.cast('', 'SHORT')
        self.assertIsNone(actual, msg='short')

        actual = Caster.cast('', 'DATE')
        self.assertIsNone(actual, msg='date')

        actual = Caster.cast('', 'FLOAT')
        self.assertIsNone(actual, msg='float')

        actual = Caster.cast('', 'DOUBLE')
        self.assertIsNone(actual, msg='double')

    def test_empty_string_returns_empty_for_strings(self):
        actual = Caster.cast('', 'TEXT')

        self.assertEqual(actual, '')
