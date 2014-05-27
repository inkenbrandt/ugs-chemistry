#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dbseeder
----------------------------------

Tests for `dbseeder` module.
"""
import arcpy
import os
import shutil
import unittest
from dbseeder.dbseeder import Seeder


class TestDbSeeder(unittest.TestCase):

    #: thing being tested
    patient = None
    location = None
    parent_folder = None
    gdb_name = 'wqp.gdb'

    def setUp(self):
        self.parent_folder = os.path.join(os.getcwd(), 'dbseeder', 'tests')
        self.location = os.path.join(self.parent_folder, 'temp_tests')

        if not os.path.exists(self.location):
            os.makedirs(self.location)

        self.patient = Seeder(self.location, self.gdb_name)

    def test_sanity(self):
        self.assertIsNotNone(self.patient)

    def test_gdb_creation(self):
        self.patient._create_gdb()

        gdb = os.path.join(self.location, self.gdb_name)
        assert os.path.exists(gdb)

    def test_fc_creation(self):
        templates = os.path.join(
            os.getcwd(),
            'dbseeder',
            'templates',
            'Templates.gdb'
        )

        self.patient.template_location = templates
        print 'templates: {}'.format(self.patient.template_location)
        self.patient._create_gdb()
        self.patient._create_feature_classes(['Stations', 'Results'])

        arcpy.env.workspace = self.patient.location

        self.assertEqual(len(arcpy.ListFeatureClasses()), 1)
        self.assertEqual(len(arcpy.ListTables()), 1)

    def _test_update(self):
        # self.patient.chemistry_query_url = self.chemistry_url
        # self.patient.update()
        pass

    def _test_seed(self):
        folder = os.path.join(os.getcwd(), 'dbseeder', 'tests', 'data')
        templates = os.path.join(
            os.getcwd(),
            'dbseeder',
            'templates',
            'Templates.gdb'
        )

        self.patient.template_location = templates
        self.patient.seed(folder)

        arcpy.env.workspace = self.patient.location
        self.assertEqual(arcpy.GetCount_management('Stations'), 50)

    def tearDown(self):
        del self.patient
        self.patient = None

        if os.path.exists(self.location):
            shutil.rmtree(self.location)


if __name__ == '__main__':
    unittest.main()
