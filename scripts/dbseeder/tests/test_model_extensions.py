#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_model_extensions
----------------------------------

Tests for the `modelextensions` module.
"""

import dbseeder.modelextensions as modelextensions
import unittest


class TestBalanceableBaseClass(unittest.TestCase):
    """tests the balanceable baseclass"""

    def setUp(self):
        self.patient = modelextensions.Balanceable()

    def test_row_access(self):
        row = [None, 'detectcond', None, 'resultvalue', None, 'param']

        self.patient.set_row_index('detectcond', 1)
        self.patient.set_row_index('resultvalue', 3)
        self.patient.set_row_index('param', 5)
        self.patient.set_row_index('nothing', 5)
        self.patient.set_row_index(None, 5)

        expected = {
            'detectcond': 1,
            'resultvalue': 3,
            'param': 5
        }

        self.assertDictEqual(expected, self.patient.field_index)

        self.patient.balance(row)

        self.assertEqual('detectcond', self.patient.detect_cond)
        self.assertEqual('resultvalue', self.patient.amount)
        self.assertEqual('param', self.patient.chemical)

    def test_row_access_with_nones(self):
        row = []

        self.patient.balance(row)

        self.assertEqual(None, self.patient.detect_cond)
        self.assertEqual(None, self.patient.amount)
        self.assertEqual(None, self.patient.chemical)
