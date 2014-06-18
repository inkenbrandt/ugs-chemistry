#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_programs
----------------------------------

Tests for `programs` module.
"""
import arcpy
import datetime
import os
import unittest
import SimpleHTTPServer
import SocketServer
import threading
from arcpy.da import InsertCursor
from dbseeder.dbseeder import Seeder
from dbseeder.programs import Wqp, Sdwis
from dbseeder.models import Results, Stations, SdwisResults
from shutil import rmtree


class TestWqpProgram(unittest.TestCase):

    def setUp(self):
        self.parent_folder = os.path.join(os.getcwd(), 'dbseeder', 'tests')
        self.location = os.path.join(self.parent_folder, 'temp_tests')
        self.gdb_name = 'wqp.gdb'

        self.tearDown()

        if not os.path.exists(self.location):
            os.makedirs(self.location)

        self.folder = os.path.join(self.location, self.gdb_name)

        seed = Seeder(self.location, self.gdb_name)

        seed._create_gdb()
        seed._create_feature_classes(['Results', 'Stations'])

        self.patient = Wqp(self.folder, InsertCursor)

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

    def test_model_hydration_result(self):
        test_data = 'dbseeder\\tests\\data\\Results\\sample_chemistry.csv'
        f = open(os.path.join(os.getcwd(), test_data))
        data = f.readlines(2)
        f.close()

        reader = self.patient._read_response(data)
        values = reader.next()

        model = Results(values)

        org_index = model.schema_map[17]['index']
        param_index = model.schema_map[19]['index']

        self.assertEqual(model.row[org_index], '1119USBR_WQX')
        self.assertEqual(model.row[param_index], 'Conductivity')

    def test_model_hydration_station(self):
        test_data = 'dbseeder\\tests\\data\\Stations\\sample_stations.csv'
        f = open(os.path.join(os.getcwd(), test_data))
        data = f.readlines(2)
        f.close()

        reader = self.patient._read_response(data)
        values = reader.next()

        model = Stations(values)

        org_index = model.schema_map[17]['index']
        param_index = model.schema_map[19]['index']

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

    def test_field_lengths(self):
        data = os.path.join(os.getcwd(), 'dbseeder', 'data')
        maps = self.patient.field_lengths(data, 'Stations')

        self.assertEqual(maps['MonitoringLocationTypeName'][1], 47)
        self.assertEqual(maps['OrganizationFormalName'][1], 70)

    def test_insert_rows_result(self):
        one_row_from_csv = [{'ActivityIdentifier': '1119USBR_WQX-14-A317',
                             'CharacteristicName': 'Conductivity',
                             'PrecisionValue': '',
                             'ResultAnalyticalMethod/MethodIdentifierContext': 'APHA',
                             'SampleAquifer': '',
                             'StatisticalBaseCode': '',
                             'ResultWeightBasisText': '',
                             'ActivityStartTime/Time': '11:40:00',
                             'ResultDetectionConditionText': '',
                             'ResultSampleFractionText': 'Dissolved',
                             'ActivityStartTime/TimeZoneCode': 'MST',
                             'ActivityStartDate': '2014-02-24',
                             'ActivityEndTime/Time': '',
                             'ActivityConductingOrganizationText': '',
                             'OrganizationIdentifier': '1119USBR_WQX',
                             'ActivityBottomDepthHeightMeasure/MeasureUnitCode': '',
                             'AnalysisStartDate': '2014-02-24',
                             'DetectionQuantitationLimitTypeName': 'Method Detection Level',
                             'MethodDescriptionText': '',
                             'ResultAnalyticalMethod/MethodIdentifier': '2510',
                             'SampleCollectionMethod/MethodName': '1119USBR_WQX~GRAB',
                             'ResultTemperatureBasisText': '',
                             'ResultDepthHeightMeasure/MeasureValue': '',
                             'ResultStatusIdentifier': 'Final',
                             'PreparationStartDate': '',
                             'USGSPCode': '',
                             'ResultMeasureValue': '141',
                             'ActivityTypeCode': 'Sample-Routine',
                             'SampleCollectionMethod/MethodIdentifierContext': '1119USBR_WQX~GRAB',
                             'MeasureQualifierCode': '',
                             'ActivityDepthHeightMeasure/MeasureValue': '',
                             'ResultParticleSizeBasisText': '',
                             'ResultAnalyticalMethod/MethodName': '',
                             'ResultDepthAltitudeReferencePointText': '',
                             'ActivityDepthAltitudeReferencePointText': '',
                             'ResultCommentText': '',
                             'SampleTissueAnatomyName': '',
                             'SubjectTaxonomicName': '',
                             'ActivityTopDepthHeightMeasure/MeasureUnitCode': '',
                             'ActivityMediaName': 'Water',
                             'DetectionQuantitationLimitMeasure/MeasureUnitCode': 'uS/cm     ',
                             'ResultValueTypeName': 'Actual',
                             'OrganizationFormalName': 'Bureau of Reclamation',
                             'ActivityCommentText': '',
                             'MonitoringLocationIdentifier': '1119USBR_WQX-RCK101',
                             'ProjectIdentifier': 'WQDATA',
                             'ResultLaboratoryCommentText': '',
                             'ActivityEndTime/TimeZoneCode': '',
                             'HydrologicCondition': '',
                             'ResultMeasure/MeasureUnitCode': 'uS/cm',
                             'ActivityTopDepthHeightMeasure/MeasureValue': '',
                             'ResultDepthHeightMeasure/MeasureUnitCode': '',
                             'DetectionQuantitationLimitMeasure/MeasureValue': '2',
                             'ActivityEndDate': '',
                             'LaboratoryName': '',
                             'HydrologicEvent': '',
                             'ResultTimeBasisText': '',
                             'ActivityBottomDepthHeightMeasure/MeasureValue': '',
                             'SampleCollectionMethod/MethodIdentifier': '1119USBR_WQX~GRAB',
                             'ActivityMediaSubdivisionName': '',
                             'SampleCollectionEquipmentName': 'Water Bottle',
                             'ActivityDepthHeightMeasure/MeasureUnitCode': ''}]

        self.patient._insert_rows(one_row_from_csv, 'Results')

        table = os.path.join(self.folder, 'Results')
        self.assertEqual('1', arcpy.GetCount_management(table).getOutput(0))

    def test_insert_rows_station(self):
        one_row_from_csv = [{
            'DrainageAreaMeasure/MeasureUnitCode': 'ha',
            'MonitoringLocationTypeName': '',
            'HorizontalCoordinateReferenceSystemDatumName': 'NAD83',
            'DrainageAreaMeasure/MeasureValue': '2774',
            'StateCode': '16',
            'MonitoringLocationIdentifier': 'ARS-IDUSR-IDUSRA10',
            'MonitoringLocationName': 'IDUSRA10',
            'VerticalMeasure/MeasureValue': '',
            'FormationTypeText': '',
            'VerticalAccuracyMeasure/MeasureUnitCode': '',
            'VerticalCoordinateReferenceSystemDatumName': '',
            'AquiferTypeName': '',
            'HorizontalAccuracyMeasure/MeasureUnitCode': '',
            'ContributingDrainageAreaMeasure/MeasureUnitCode': '',
            'WellHoleDepthMeasure/MeasureValue': '',
            'WellDepthMeasure/MeasureValue': '',
            'LongitudeMeasure': '-114.323546838',
            'AquiferName': '',
            'HorizontalAccuracyMeasure/MeasureValue': '',
            'HUCEightDigitCode': '17040212',
            'LatitudeMeasure': '42.5661737512',
            'ContributingDrainageAreaMeasure/MeasureValue': '',
            'OrganizationFormalName': 'USDA Agricultural Research Service',
            'WellDepthMeasure/MeasureUnitCode': '',
            'OrganizationIdentifier': 'ARS',
            'HorizontalCollectionMethodName': '',
            'VerticalAccuracyMeasure/MeasureValue': '',
            'VerticalCollectionMethodName': '',
            'MonitoringLocationDescriptionText': 'IDUSRA10 is an irrigation return',
            'CountryCode': 'US',
            'VerticalMeasure/MeasureUnitCode': '',
            'CountyCode': '83',
            'ConstructionDateText': '',
            'WellHoleDepthMeasure/MeasureUnitCode': '',
            'SourceMapScaleNumeric': ''}]

        self.patient._insert_rows(one_row_from_csv, 'Stations')

        table = os.path.join(self.folder, 'Stations')
        self.assertEqual('1', arcpy.GetCount_management(table).getOutput(0))

    def tearDown(self):
        self.patient = None
        del self.patient

        limit = 5000
        i = 0

        while os.path.exists(self.location) and i < limit:
            try:
                rmtree(self.location)
            except:
                i += 1


class TestSdwisProgram(unittest.TestCase):

    def setUp(self):
        self.parent_folder = os.path.join(os.getcwd(), 'dbseeder', 'tests')
        self.location = os.path.join(self.parent_folder, 'temp_tests')
        self.gdb_name = 'sdwis.gdb'

        self.tearDown()

        if not os.path.exists(self.location):
            os.makedirs(self.location)

        self.folder = os.path.join(self.location, self.gdb_name)

        seed = Seeder(self.location, self.gdb_name)

        seed._create_gdb()
        seed._create_feature_classes(['Results', 'Stations'])

        self.patient = Sdwis(self.folder, InsertCursor)

    def test_sanity(self):
        self.assertIsNotNone(self.patient)

    def test_query(self):
        data = self.patient._query(self.patient._result_query, 2)
        for item in data:
            etl = SdwisResults(item)

            self.assertIsNotNone(etl.row)

    def test_insert_rows_result(self):
        one_row_from_query = [(None,
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
                               3908822)]

        self.patient._insert_rows(one_row_from_query, 'Results')

        table = os.path.join(self.folder, 'Results')
        self.assertEqual('1', arcpy.GetCount_management(table).getOutput(0))

    def test_insert_rows_station(self):
        one_row_from_query = [(750,
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
                               None)]

        self.patient._insert_rows(one_row_from_query, 'Stations')

        table = os.path.join(self.folder, 'Stations')
        self.assertEqual('1', arcpy.GetCount_management(table).getOutput(0))

    def tearDown(self):
        self.patient = None
        del self.patient

        limit = 5000
        i = 0

        while os.path.exists(self.location) and i < limit:
            try:
                rmtree(self.location)
            except:
                i += 1


class TestServer(SocketServer.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    unittest.main()
