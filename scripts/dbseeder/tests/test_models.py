#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_programs
----------------------------------

Tests for `models` module.
"""

import datetime
import unittest
from dbseeder.models import SdwisResults, SdwisStations


class TestSdwisModels(unittest.TestCase):

    def test_SdwisStations_creation(self):
        db_row = [750,
                  'HANNA WATER & SEWER IMPROVEMENT DISTRICT',
                  3382,
                  'STOCKMORE WELL                          ',
                  'WL',
                  40.460074,
                  -110.826317,
                  15.0,
                  '018',
                  '003',
                  2126.71,
                  1.84,
                  '003',
                  '003',
                  0,
                  None]
        patient = SdwisStations(db_row)
        row = patient.row
        print row
        self.assertItemsEqual(['750',
                               'HANNA WATER & SEWER IMPROVEMENT DISTRICT',
                               '3382',
                               'STOCKMORE WELL',
                               'WL',
                               None,
                               None,
                               40.460074,
                               -110.826317,
                               15.0,
                               None,
                               '018',
                               '003',
                               2126.71,
                               None,
                               1.84,
                               None,
                               '003',
                               '003',
                               None,
                               None,
                               None,
                               None,
                               None,
                               None,
                               0.0,
                               None,
                               None,
                               None,
                               None,
                               None,
                               None], row)

    def test_SdwisResults_creation(self):
        db_row = [None,
                  'UT00007   ',
                  0.1,
                  'MG/L     ',
                  1748,
                  'SUMMIT CHATEAU IN BRIAN HEAD',
                  'NITRATE-NITRITE                         ',
                  0.0,
                  datetime.datetime(2014, 4, 23, 0, 0),
                  datetime.datetime(1, 1, 1, 14, 10),
                  'K201400801',
                  'WL',
                  9032,
                  '         ',
                  37.732475,
                  -112.871236,
                  None,
                  3908822]

        patient = SdwisResults(db_row)
        self.assertItemsEqual(patient.row,
                              [None,
                               None,
                               None,
                               None,
                               None, #: cas_reg
                               None,
                               None,
                               None,
                               3908822, #: idnum
                               None,
                               'UT00007', #: lab comments
                               37.732475,
                               None,
                               -112.871236,
                               0.1,
                               'MG/L',
                               None,
                               '1748', #: orgid
                               'SUMMIT CHATEAU IN BRIAN HEAD',
                               'NITRATE-NITRITE',
                               None,
                               None,
                               None,
                               None,
                               None,
                               0.0, #: result value
                               None,
                               None,
                               None,
                               None,
                               None,
                               None,
                               datetime.datetime(2014, 04, 23, 0, 0),
                               datetime.datetime(1, 1, 1, 14, 10),
                               'K201400801',
                               None,
                               None,
                               None,
                               'WL',
                               '9032',
                               '',
                               None])
