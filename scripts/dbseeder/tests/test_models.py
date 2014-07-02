#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_programs
----------------------------------

Tests for `models` module.
"""

import datetime
import dbseeder.models as models
import unittest
from dbseeder.services import Normalizer


class TestWqpModels(unittest.TestCase):

    def test_model_hydration_result(self):
        mdl = 2
        resultvalue = 141
        sampdepth = 0
        analysisdate = datetime.datetime(2014, 02, 24, 0, 0)
        sampledate = datetime.datetime(2014, 02, 24, 0, 0)
        # time parsing gives current date
        sampletime = (datetime.datetime.now().
                      replace(hour=11, minute=40, second=0, microsecond=0))

        csv_data = {'ActivityIdentifier': 'SampleId',
                    'CharacteristicName': 'Param',
                    'PrecisionValue': '',
                    'ResultAnalyticalMethod/MethodIdentifierContext': '',
                    'SampleAquifer': '',
                    'StatisticalBaseCode': '',
                    'ResultWeightBasisText': '',
                    'ActivityStartTime/Time': '11:40:00',
                    'ResultDetectionConditionText': 'DetectCond',
                    'ResultSampleFractionText': 'SampFrac',
                    'ActivityStartTime/TimeZoneCode': 'MST',
                    'ActivityStartDate': '2014-02-24',
                    'ActivityEndTime/Time': '',
                    'ActivityConductingOrganizationText': '',
                    'OrganizationIdentifier': 'OrgId',
                    'ActivityBottomDepthHeightMeasure/MeasureUnitCode': '',
                    'AnalysisStartDate': '2014-02-24',
                    'DetectionQuantitationLimitTypeName': 'LimitType',
                    'MethodDescriptionText': 'MethodDescript',
                    'ResultAnalyticalMethod/MethodIdentifier': 'AnalytMethId',
                    'SampleCollectionMethod/MethodName': 'SampMethName',
                    'ResultTemperatureBasisText': '',
                    'ResultDepthHeightMeasure/MeasureValue': '',
                    'ResultStatusIdentifier': 'ResultStatus',
                    'PreparationStartDate': '',
                    'USGSPCode': 'USGSPCode',
                    'ResultMeasureValue': '141',
                    'ActivityTypeCode': 'SampType',
                    'SampleCollectionMethod/MethodIdentifierContext': '',
                    'MeasureQualifierCode': 'QualCode',
                    'ActivityDepthHeightMeasure/MeasureValue': '0',
                    'ResultParticleSizeBasisText': '',
                    'ResultAnalyticalMethod/MethodName': 'AnalytMeth',
                    'ResultDepthAltitudeReferencePointText': '',
                    'ActivityDepthAltitudeReferencePointText': 'SampDepthRef',
                    'ResultCommentText': 'ResultComment',
                    'SampleTissueAnatomyName': '',
                    'SubjectTaxonomicName': '',
                    'ActivityTopDepthHeightMeasure/MeasureUnitCode': '',
                    'ActivityMediaName': 'Water',
                    'DetectionQuantitationLimitMeasure/MeasureUnitCode': 'mdlunit',
                    'ResultValueTypeName': 'Actual',
                    'OrganizationFormalName': 'OrgName',
                    'ActivityCommentText': 'SampComment',
                    'MonitoringLocationIdentifier': 'StationId',
                    'ProjectIdentifier': 'ProjectId',
                    'ResultLaboratoryCommentText': 'LabComments',
                    'ActivityEndTime/TimeZoneCode': '',
                    'HydrologicCondition': '',
                    'ResultMeasure/MeasureUnitCode': 'unit',
                    'ActivityTopDepthHeightMeasure/MeasureValue': '',
                    'ResultDepthHeightMeasure/MeasureUnitCode': '',
                    'DetectionQuantitationLimitMeasure/MeasureValue': '2',
                    'ActivityEndDate': '',
                    'LaboratoryName': 'LabName',
                    'HydrologicEvent': '',
                    'ResultTimeBasisText': '',
                    'ActivityBottomDepthHeightMeasure/MeasureValue': '',
                    'SampleCollectionMethod/MethodIdentifier': 'SampMeth',
                    'ActivityMediaSubdivisionName': 'SampMedia',
                    'SampleCollectionEquipmentName': 'SampEquip',
                    'ActivityDepthHeightMeasure/MeasureUnitCode': 'SampDepthU'}
        actual = [analysisdate,
                  'AnalytMeth',
                  'AnalytMethId',
                  None,
                  None,
                  None,
                  None,
                  'DetectCond',
                  None,  # : idNum
                  'LabComments',
                  'LabName',
                  None,  # : lay y
                  'LimitType',
                  None,  # lon x,
                  mdl,
                  'mdlunit',
                  'MethodDescript',
                  'OrgId',
                  'OrgName',
                  'Param',
                  None,  # paramgroup
                  'ProjectId',
                  'QualCode',
                  'ResultComment',
                  'ResultStatus',
                  resultvalue,
                  'SampComment',
                  sampdepth,
                  'SampDepthRef',
                  'SampDepthU',
                  'SampEquip',
                  'SampFrac',
                  sampledate,
                  sampletime,
                  'SampleId',
                  'SampMedia',
                  'SampMeth',
                  'SampMethName',
                  'SampType',
                  'StationId',
                  'unit',
                  'USGSPCode'
                  ]

        expected = models.Results(csv_data, Normalizer()).row
        self.assertListEqual(actual, expected)

    def test_model_hydration_station(self):
        csv_data = {'DrainageAreaMeasure/MeasureUnitCode': 'ha',
                    'MonitoringLocationTypeName': 'StationType',
                    'HorizontalCoordinateReferenceSystemDatumName': 'HorRef',
                    'DrainageAreaMeasure/MeasureValue': '2774',
                    'StateCode': '16',
                    'MonitoringLocationIdentifier': 'StationId',
                    'MonitoringLocationName': 'StationName',
                    'VerticalMeasure/MeasureValue': '0',
                    'FormationTypeText': 'FmType',
                    'VerticalAccuracyMeasure/MeasureUnitCode': 'ElevAccUnit',
                    'VerticalCoordinateReferenceSystemDatumName': 'ElevRef',
                    'AquiferTypeName': 'AquiferType',
                    'HorizontalAccuracyMeasure/MeasureUnitCode': 'HorAccUnit',
                    'ContributingDrainageAreaMeasure/MeasureUnitCode': '',
                    'WellHoleDepthMeasure/MeasureValue': '0',
                    'WellDepthMeasure/MeasureValue': '0',
                    'LongitudeMeasure': '-114.323546838',
                    'AquiferName': 'Aquifer',
                    'HorizontalAccuracyMeasure/MeasureValue': '0',
                    'HUCEightDigitCode': 'HUC8',
                    'LatitudeMeasure': '42.5661737512',
                    'ContributingDrainageAreaMeasure/MeasureValue': '',
                    'OrganizationFormalName': 'OrgName',
                    'WellDepthMeasure/MeasureUnitCode': 'DepthUnit',
                    'OrganizationIdentifier': 'OrgId',
                    'HorizontalCollectionMethodName': 'HorCollMeth',
                    'VerticalAccuracyMeasure/MeasureValue': '0',
                    'VerticalCollectionMethodName': 'ElevMeth',
                    'MonitoringLocationDescriptionText': 'StationComment',
                    'CountryCode': 'US',
                    'VerticalMeasure/MeasureUnitCode': 'ElevUnit',
                    'CountyCode': '83',
                    'ConstructionDateText': '2014-06-19',
                    'WellHoleDepthMeasure/MeasureUnitCode': 'HoleDUnit',
                    'SourceMapScaleNumeric': ''}
        lon_x = -114.323546838
        lat_y = 42.5661737512
        elev = depth = holedepth = elevac = horacc = 0
        statecode = 16
        countycode = 83
        constdate = datetime.datetime(2014, 06, 19, 0, 0)
        expected = [
            'OrgId',
            'OrgName',
            'StationId',
            'StationName',
            'StationType',
            'StationComment',
            'HUC8',
            lon_x,
            lat_y,
            horacc,
            'HorAccUnit',
            'HorCollMeth',
            'HorRef',
            elev,
            'ElevUnit',
            elevac,
            'ElevAccUnit',
            'ElevMeth',
            'ElevRef',
            statecode,
            countycode,
            'Aquifer',
            'FmType',
            'AquiferType',
            constdate,
            depth,
            'DepthUnit',
            holedepth,
            'HoleDUnit',
            None,
            None,
            None
        ]
        actual = models.Stations(csv_data, Normalizer()).row

        self.assertListEqual(actual, expected)

    def test_table_normalization():
        pass


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
        patient = models.SdwisStations(db_row, Normalizer())
        row = patient.row
        self.assertListEqual(['750',
                              'HANNA WATER & SEWER IMPROVEMENT DISTRICT',
                              '3382',
                              'STOCKMORE WELL',
                              'WL',
                              None,
                              None,
                              -110.826317,
                              40.460074,
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

        patient = models.SdwisResults(db_row, Normalizer())
        self.assertListEqual(patient.row,
                             [None,
                              None,
                              None,
                              None,
                              None,  # : cas_reg
                              None,
                              None,
                              None,
                              3908822,  # : idnum
                              None,
                              'UT00007',  # : lab comments
                              37.732475,
                              None,
                              -112.871236,
                              0.1,
                              'MG/L',
                              None,
                              '1748',  # : orgid
                              'SUMMIT CHATEAU IN BRIAN HEAD',
                              'NITRATE-NITRITE',
                              None,
                              None,
                              None,
                              None,
                              None,
                              0.0,  # : result value
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

    def test_sdwis_normalization():
        pass


class TestDogmModels(unittest.TestCase):

    def test_ogm_station_model_hydration(self):
        gdb_data = ['UDOGM',
                    'Utah Division Of Oil Gas And Mining',
                    'UDOGM-0035',
                    'WILLOW CREEK; 1',
                    None,
                    'ft',
                    'MD',
                    'UPDES',
                    39.72882937000003,
                    -110.85612099299999,
                    512329.9142,
                    4397670.5318
                    ]

        model = models.OgmStation(gdb_data, models.Schema().station, Normalizer())

        expected = ['UDOGM',
                    'Utah Division Of Oil Gas And Mining',
                    'UDOGM-0035',
                    'WILLOW CREEK; 1',
                    'MD',
                    'UPDES',
                    None,
                    -110.85612099299999,
                    39.72882937000003,
                    None,
                    None,
                    None,
                    None,
                    None,
                    'ft',
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    (512329.9142,
                     4397670.5318)]

        self.assertListEqual(expected, model.row)

    def test_ogm_result_model_hydration(self):
        analysisdate = datetime.datetime(2014, 11, 17, 0, 0)
        sampledate = datetime.datetime(2008, 11, 17, 0, 0)
        sampletime = datetime.datetime(1899, 12, 30, 11, 10)
        resultvalue = 10.0

        gdb_data = ['StationId',
                    'Param',
                    'SampleId',
                    sampledate,
                    analysisdate,
                    'AnalytMeth',
                    'MDLUnit',
                    resultvalue,
                    sampletime,
                    'MDL',
                    'Unit',
                    'SampComment']
        expected = [analysisdate,
                    'AnalytMeth',
                    None,  # analythmethid
                    None,  # autoqual
                    None,  # cas reg
                    None,  # chrg
                    None,  # datasource
                    None,  # detectcond
                    None,  # idnum
                    None,  # lab comments
                    None,  # lab name
                    None,  # lat y
                    None,  # limit type
                    None,  # lon x
                    'MDL',
                    'MDLUnit',
                    None,  # method descript
                    None,  # orgid
                    None,  # orgname
                    'Param',
                    None,  # paramgroup
                    None,  # projectid
                    None,  # qualcode
                    None,  # r result comment
                    None,  # result status
                    resultvalue,
                    'SampComment',
                    None,  # sampdepth
                    None,  # sampdepthref
                    None,  # sampdepthu
                    None,  # sampequp
                    None,  # sampfrac
                    sampledate,
                    sampletime,
                    'SampleId',  # sample id
                    None,  # sampmedia
                    None,  # sampmeth
                    None,  # sampmethname
                    None,  # samptype
                    'StationId',
                    'unit',
                    None  # usgspcode
                    ]

        model = models.OgmResult(gdb_data, models.Schema().result, Normalizer())
        actual = model.row

        self.assertListEqual(expected, actual)

    def test_gdb_datasoure_normalization(self):
        gdb_data = [None,
                    '.alpha.-Endosulfan',
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None]
        expected = [None,
                    None,
                    None,  # analythmethid
                    None,  # autoqual
                    None,  # cas reg
                    None,  # chrg
                    None,  # datasource
                    None,  # detectcond
                    None,  # idnum
                    None,  # lab comments
                    None,  # lab name
                    None,  # lat y
                    None,  # limit type
                    None,  # lon x
                    None,
                    None,
                    None,  # method descript
                    None,  # orgid
                    None,  # orgname
                    '.alpha.-Endosulfan',
                    'Organics, pesticide',  # paramgroup
                    None,  # projectid
                    None,  # qualcode
                    None,  # r result comment
                    None,  # result status
                    None,
                    None,
                    None,  # sampdepth
                    None,  # sampdepthref
                    None,  # sampdepthu
                    None,  # sampequp
                    None,  # sampfrac
                    None,
                    None,
                    None,  # sample id
                    None,  # sampmedia
                    None,  # sampmeth
                    None,  # sampmethname
                    None,  # samptype
                    None,
                    None,
                    None  # usgspcode
                    ]

        model = models.OgmResult(gdb_data, models.Schema().
                                 result, Normalizer())
        actual = model.row

        self.assertListEqual(expected, actual)
