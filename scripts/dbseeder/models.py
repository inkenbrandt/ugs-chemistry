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

class Stations(Table):

    """ORM mapping from chemistry schema to Stations feature class"""

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

class Results(Table):

    """ORM mapping to station schema to Results table"""

    schema_map = OrderedDict([
        ('OrgID', 'OrganizationIdentifier'),
        ('OrgName', 'OrganizationFormalName'),
        ('StationID', 'MonitoringLocationIdentifier'),
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
