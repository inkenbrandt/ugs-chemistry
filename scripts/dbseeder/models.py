"""module containing project models"""

import os
from collections import OrderedDict


class TableInfo(object):

    def __init__(self, template, name):
        self.template = os.path.join(template, name)
        self.name = name


class Table(object):

    def __init__(self, row):

        self._row = []

        for key in self.schema_map:
            value = str(row[self.schema_map[key]]).strip()
            self._row.append(value)

    @property
    def row(self):
        return self._row


class Results(Table):

    """ORM mapping to station schema to Results table"""

    schema_map = OrderedDict([
        ('AnalysisDate', 'AnalysisStartDate'),
        ('AnalytContext', 'ResultAnalyticalMethod/MethodIdentifierContext'),
        ('AnalytMeth', 'ResultAnalyticalMethod/MethodName'),
        ('AnalytMethId', 'ResultAnalyticalMethod/MethodIdentifier'),
        ('DetectCond', 'ResultDetectionConditionText'),
        ('LabComments', 'ResultLaboratoryCommentText'),
        ('LabName', 'LaboratoryName'),
        ('LimitType', 'DetectionQuantitationLimitTypeName'),
        ('MDL', 'DetectionQuantitationLimitMeasure/MeasureValue'),
        ('MDLUnit', 'DetectionQuantitationLimitMeasure/MeasureUnitCode'),
        ('MethodDescript', 'MethodDescriptionText'),
        ('OrgId', 'OrganizationIdentifier'),
        ('OrgName', 'OrganizationFormalName'),
        ('Param', 'CharacteristicName'),
        ('ProjectId', 'ProjectIdentifier'),
        ('QualCode', 'MeasureQualifierCode'),
        ('ResultComment', 'ResultCommentText'),
        ('ResultStatus', 'ResultStatusIdentifier'),
        ('ResultValue', 'ResultMeasureValue'),
        ('SampComment', 'ActivityCommentText'),
        ('SampContext', 'SampleCollectionMethod/MethodIdentifierContext'),
        ('SampDepth', 'ActivityDepthHeightMeasure/MeasureValue'),
        ('SampDepthRef', 'ActivityDepthAltitudeReferencePointText'),
        ('SampDepthU', 'ActivityDepthHeightMeasure/MeasureUnitCode'),
        ('SampEquip', 'SampleCollectionEquipmentName'),
        ('SampFrac', 'ResultSampleFractionText'),
        ('SampleDate', 'ActivityStartDate'),
        ('SampleTime', 'ActivityStartTime/Time'),
        ('SampleId', 'ActivityIdentifier'),
        ('SampMedia', 'ActivityMediaName'),
        ('SampMediaSub', 'ActivityMediaSubdivisionName'),
        ('SampMeth', 'SampleCollectionMethod/MethodIdentifier'),
        ('SampMethName', 'SampleCollectionMethod/MethodName'),
        ('SampType', 'ActivityTypeCode'),
        ('StationId', 'MonitoringLocationIdentifier'),
        ('Unit', 'ResultMeasure/MeasureUnitCode'),
        ('USGSPCode', 'USGSPCode')
    ])


class Stations(Table):

    """ORM mapping from chemistry schema to Stations feature class"""

    schema_map = OrderedDict([
        ('OrgId', 'OrganizationIdentifier'),
        ('OrgName', 'OrganizationFormalName'),
        ('StationId', 'MonitoringLocationIdentifier'),
        ('StationName', 'MonitoringLocationName'),
        ('StationType', 'MonitoringLocationTypeName'),
        ('StationComment', 'MonitoringLocationDescriptionText'),
        ('HUC8', 'HUCEightDigitCode'),
        ('Lat_Y', 'LatitudeMeasure'),
        ('Lon_X', 'LongitudeMeasure'),
        ('HorAcc', 'HorizontalAccuracyMeasure/MeasureValue'),
        ('HorAccUnit', 'HorizontalAccuracyMeasure/MeasureUnitCode'),
        ('HorCollMeth', 'HorizontalCollectionMethodName'),
        ('HorRef', 'HorizontalCoordinateReferenceSystemDatumName'),
        ('Elev', 'VerticalMeasure/MeasureValue'),
        ('ElevUnit', 'VerticalMeasure/MeasureUnitCode'),
        ('ElevAcc', 'VerticalAccuracyMeasure/MeasureValue'),
        ('ElevAccUnit', 'VerticalAccuracyMeasure/MeasureUnitCode'),
        ('ElevMeth', 'VerticalCollectionMethodName'),
        ('ElevRef', 'VerticalCoordinateReferenceSystemDatumName'),
        ('StateCode', 'StateCode'),
        ('CountyCode', 'CountyCode'),
        ('Aquifer', 'AquiferName'),
        ('FmType', 'FormationTypeText'),
        ('AquiferType', 'AquiferTypeName'),
        ('ConstDate', 'ConstructionDateText'),
        ('Depth', 'WellDepthMeasure/MeasureValue'),
        ('DepthUnit', 'WellDepthMeasure/MeasureUnitCode'),
        ('HoleDepth', 'WellHoleDepthMeasure/MeasureValue'),
        ('HoleDUnit', 'WellHoleDepthMeasure/MeasureUnitCode')
    ])


class SdwisResults(object):
    def __init__(self, row):

        self.row = []

        for item in row:
            value = str(item).strip()
            self.row.append(value)

    schema_index_map = OrderedDict([
        ('AnalysisDate', 0),
        ('LabName', 1),
        ('MDL', 2),
        ('MDLUnit', 3),
        ('OrgId', 4),
        ('OrgName', 5),
        ('Param', 6),
        ('ResultValue', 7),
        ('SampleDate', 8),
        ('SampleTime', 9),
        ('SampleId', 10),
        ('SampType', 11),
        ('StationId', 12),
        ('Unit', 13),
        ('Lat_Y', 14),
        ('Lon_X', 15),
        ('CAS_Reg', 16),
        ('Id_Num', 17)
    ])


class SdwisStations(object):
    def __init__(self, row):

        self.row = []

        for item in row:
            value = str(item).strip()
            self.row.append(value)

    schema_index_map = OrderedDict([
        ('OrgId', 0),
        ('OrgName', 1),
        ('StationId', 2),
        ('StationName', 3),
        ('StationType', 4),
        ('Lat_Y', 5),
        ('Lon_X', 6),
        ('HorAcc', 7),
        ('HorCollMeth', 8),
        ('HorRef', 9),
        ('Elev', 10),
        ('ElevAcc', 11),
        ('ElevMeth', 12),
        ('ElevRef', 13),
        ('Depth', 14),
        ('DepthUnit', 15)
    ])
