#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dbseeder
----------------------------------

Tests for `dbseeder` module.
"""
import os
import shutil
import unittest
from dbseeder.dbseeder import Seeder
from dbseeder.models import Chemistry


class TestDbSeeder(unittest.TestCase):

    patient = None
    location = None
    parent_folder = None
    gdb_name = 'wqp.gdb'
    chemistry_url = 'http://localhost/sample_chemistry.csv'

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

    def test_csv_reader_with_data_from_requests(self):
        data = self.patient._query_chemistry(self.chemistry_url)
        reader = self.patient._read_response(data)
        values = reader.next()

        self.assertIsNotNone(reader)
        self.assertEqual(len(values.keys()), 62)
        self.assertEqual(values['OrganizationIdentifier'], '1119USBR_WQX')

    def test_csv_reader(self):
        test_data = 'dbseeder\\tests\\data\\sample_chemistry.csv'
        f = open(os.path.join(os.getcwd(), test_data))
        data = f.readlines(2)
        f.close()

        reader = self.patient._read_response(data)
        values = reader.next()

        self.assertIsNotNone(reader)
        self.assertEqual(len(values.keys()), 62)
        self.assertEqual(values['OrganizationIdentifier'], '1119USBR_WQX')

    def test_model_hydration(self):
        test_data = 'dbseeder\\tests\\data\\sample_chemistry.csv'
        f = open(os.path.join(os.getcwd(), test_data))
        data = f.readlines(2)
        f.close()

        reader = self.patient._read_response(data)
        values = reader.next()

        chemistry = Chemistry(values)

        org_index = chemistry.schema_map.keys().index('OrgId')
        param_index = chemistry.schema_map.keys().index('Param')

        self.assertEqual(chemistry.row[org_index], '1119USBR_WQX')
        self.assertEqual(chemistry.row[param_index], 'Conductivity')

    def test_update(self):
        # self.patient.chemistry_query_url = self.chemistry_url
        # self.patient.update()
        pass

    def test_seed(self):
        folder = os.path.join(os.getcwd(), 'dbseeder', 'data')
        self.patient.seed(folder)

    def test_csv_on_disk(self):
        data = os.path.join(os.getcwd(), 'dbseeder', 'data')
        gen = self.patient._csvs_on_disk(data, 'Stations')
        csv = gen.next()

        self.assertIsNotNone(csv)
        self.assertRegexpMatches('Stations.csv', 'Stations.csv$')

    def test_chemistry_csv_on_disk(self):
        data = os.path.join(os.getcwd(), 'dbseeder', 'data')
        gen = self.patient._csvs_on_disk(data, 'Chemistry')
        count = 0

        for file in gen:
            count += 1
            self.assertIsNotNone(file)
            self.assertRegexpMatches(file, 'Result.*.csv$')

        self.assertEqual(count, 10)

    def tearDown(self):
        del self.patient
        self.patient = None

        while os.path.exists(self.location):
            shutil.rmtree(self.location)

if __name__ == '__main__':
    unittest.main()
