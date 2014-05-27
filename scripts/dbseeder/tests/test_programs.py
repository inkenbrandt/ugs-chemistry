#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_programs
----------------------------------

Tests for `programs` module.
"""
import os
import unittest
import SimpleHTTPServer
import SocketServer
import threading
from arcpy.da import InsertCursor
from dbseeder.dbseeder import Seeder
from dbseeder.programs import Wqp, Sdwis
from dbseeder.models import Results
from shutil import rmtree


class TestWqpProgram(unittest.TestCase):

    def setUp(self):
        self.parent_folder = os.path.join(os.getcwd(), 'dbseeder', 'tests')
        self.location = os.path.join(self.parent_folder, 'temp_tests')
        self.gdb_name = 'wqp.gdb'

        if not os.path.exists(self.location):
            os.makedirs(self.location)

        folder = os.path.join(self.location, self.gdb_name)

        seed = Seeder(self.location, self.gdb_name)
        templates = os.path.join(
            os.getcwd(),
            'dbseeder',
            'templates',
            'Templates.gdb'
        )

        seed.template_location = templates
        seed._create_gdb()
        seed._create_feature_classes(['Results', 'Stations'])

        self.patient = Wqp(folder, InsertCursor)

    def test_sanity(self):
        self.assertIsNotNone(self.patient)

    def test_csv_reader_with_data_from_requests(self):
        handler = SimpleHTTPServer.SimpleHTTPRequestHandler

        httpd = TestServer(('localhost', 8001), handler)

        httpd_thread = threading.Thread(target=httpd.serve_forever)
        httpd_thread.setDaemon(True)
        httpd_thread.start()

        host = 'http://localhost:8001'
        path = '/dbseeder/tests/data/Results/'

        url = '{}{}sample_chemistry.csv'.format(host, path)

        data = self.patient._query(url)
        reader = self.patient._read_response(data)
        values = reader.next()

        self.assertIsNotNone(reader)
        self.assertEqual(len(values.keys()), 62)
        self.assertEqual(values['OrganizationIdentifier'], '1119USBR_WQX')

    def test_csv_reader(self):
        test_data = 'dbseeder\\tests\\data\\Results\\sample_chemistry.csv'
        f = open(os.path.join(os.getcwd(), test_data))
        data = f.readlines(2)
        f.close()

        reader = self.patient._read_response(data)
        values = reader.next()

        self.assertIsNotNone(reader)
        self.assertEqual(len(values.keys()), 62)
        self.assertEqual(values['OrganizationIdentifier'], '1119USBR_WQX')

    def test_model_hydration(self):
        test_data = 'dbseeder\\tests\\data\\Results\\sample_chemistry.csv'
        f = open(os.path.join(os.getcwd(), test_data))
        data = f.readlines(2)
        f.close()

        reader = self.patient._read_response(data)
        values = reader.next()

        model = Results(values)

        org_index = model.schema_map.keys().index('OrgId')
        param_index = model.schema_map.keys().index('Param')

        self.assertEqual(model.row[org_index], '1119USBR_WQX')
        self.assertEqual(model.row[param_index], 'Conductivity')

    def test_csv_on_disk(self):
        data = os.path.join(os.getcwd(), 'dbseeder', 'tests', 'data')
        gen = self.patient._csvs_on_disk(data, 'Stations')
        csv = gen.next()

        self.assertIsNotNone(csv)
        self.assertRegexpMatches('Stations.csv', 'Stations.csv$')

    def test_chemistry_csv_on_disk(self):
        data = os.path.join(os.getcwd(), 'dbseeder', 'tests', 'data')
        gen = self.patient._csvs_on_disk(data, 'Results')
        count = 0

        for file in gen:
            count += 1
            self.assertIsNotNone(file)
            self.assertRegexpMatches(file, 'Result.*.csv$')

        self.assertEqual(count, 2)

    def test_get_field_lengths(self):
        data = os.path.join(os.getcwd(), 'dbseeder', 'data')
        maps = self.patient.field_lengths(data, 'Stations')

        self.assertEqual(maps['MonitoringLocationTypeName'][1], 47)
        self.assertEqual(maps['OrganizationFormalName'][1], 70)

    def tearDown(self):
        del self.patient
        self.patient = None

        if os.path.exists(self.location):
            rmtree(self.location)


class TestSdwisProgram(unittest.TestCase):

    def setUp(self):
        self.parent_folder = os.path.join(os.getcwd(), 'dbseeder', 'tests')
        self.location = os.path.join(self.parent_folder, 'temp_tests')
        self.gdb_name = 'sdwis.gdb'

        if not os.path.exists(self.location):
            os.makedirs(self.location)

        folder = os.path.join(self.location, self.gdb_name)

        seed = Seeder(self.location, self.gdb_name)
        templates = os.path.join(
            os.getcwd(),
            'dbseeder',
            'templates',
            'Templates.gdb'
        )

        seed.template_location = templates
        seed._create_gdb()
        seed._create_feature_classes(['Results', 'Stations'])

        self.patient = Sdwis(folder, InsertCursor)

    def test_sanity(self):
        self.assertIsNotNone(self.patient)

    def _test_sdwis_model_hydration(self):
        result = self.patient.sdwis_results()
        station = self.patient.sdwis_stations()

        print result
        print station

    def tearDown(self):
        del self.patient
        self.patient = None

        if os.path.exists(self.location):
            rmtree(self.location)


class TestServer(SocketServer.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    unittest.main()
