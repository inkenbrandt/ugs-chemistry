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


class Schema(object):

    """a class defining the schema for the gdb and also checks for validity"""

    station_gdoc_schema = [
        {
            'destination': 'OrgId',
            'source': 'OrganizationIdentifier',
            'alias': 'Organization Id',
            'type': 'String',
            'length': 20
        },
        {
            'destination': 'OrgName',
            'source': 'OrganizationFormalName',
            'alias': 'Organization Name',
            'type': 'String',
            'length': 100
        },
        {
            'destination': 'StationId',
            'source': 'MonitoringLocationIdentifier',
            'alias': 'Monitoring Location Id',
            'type': 'String',
            'length': 100
        },
        {
            'destination': 'StationName',
            'source': 'MonitoringLocationName',
            'alias': 'Monitoring Location Name',
            'type': 'String',
            'length': 100
        },
        {
            'destination': 'StationType',
            'source': 'MonitoringLocationTypeName',
            'alias': 'Monitoring Location Type',
            'type': 'String',
            'length': 100
        },
        {
            'destination': 'StationComment',
            'source': 'MonitoringLocationDescriptionText',
            'alias': 'Monitoring Location Description',
            'type': 'String',
            'length': 1500
        },
        {
            'destination': 'HUC8',
            'source': 'HUCEightDigitCode',
            'alias': 'HUC 8 Digit Code',
            'type': 'String',
            'length': 8
        },
        {
            'destination': 'Lon_X',
            'source': 'LongitudeMeasure',
            'alias': 'Latitude',
            'type': 'Double'
        },
        {
            'destination': 'Lat_Y',
            'source': 'LatitudeMeasure',
            'alias': 'Longitude',
            'type': 'Double'
        },
        {
            'destination': 'HorAcc',
            'source': 'HorizontalAccuracyMeasure/MeasureValue',
            'alias': 'Horizontal Accuracy',
            'type': 'Double'
        },
        {
            'destination': 'HorAccUnit',
            'source': 'HorizontalAccuracyMeasure/MeasureUnitCode',
            'alias': 'Horizontal Accuracy Unit',
            'type': 'String',
            'length': 10
        },
        {
            'destination': 'HorCollMeth',
            'source': 'HorizontalCollectionMethodName',
            'alias': 'Horizontal Collection Method',
            'type': 'String',
            'length': 100
        },
        {
            'destination': 'HorRef',
            'source': 'HorizontalCoordinateReferenceSystemDatumName',
            'alias': 'Horizontal Reference Datum',
            'type': 'String',
            'length': 10
        },
        {
            'destination': 'Elev',
            'source': 'VerticalMeasure/MeasureValue',
            'alias': 'Elevation',
            'type': 'Double'
        },
        {
            'destination': 'ElevUnit',
            'source': 'VerticalMeasure/MeasureUnitCode',
            'alias': 'Elevation Unit',
            'type': 'String',
            'length': 15
        },
        {
            'destination': 'ElevAcc',
            'source': 'VerticalAccuracyMeasure/MeasureValue',
            'alias': 'Elevation Accuracy',
            'type': 'Double'
        },
        {
            'destination': 'ElevAccUnit',
            'source': 'VerticalAccuracyMeasure/MeasureUnitCode',
            'alias': 'Elevation Accuracy Units',
            'type': 'String',
            'length': 4
        },
        {
            'destination': 'ElevMeth',
            'source': 'VerticalCollectionMethodName',
            'alias': 'Elevation Collection Method',
            'type': 'String',
            'length': 100
        },
        {
            'destination': 'ElevRef',
            'source': 'VerticalCoordinateReferenceSystemDatumName',
            'alias': 'Elevation Reference Datum',
            'type': 'String',
            'length': 12
        },
        {
            'destination': 'StateCode',
            'source': 'StateCode',
            'alias': 'State Code',
            'type': 'Short Int'
        },
        {
            'destination': 'CountyCode',
            'source': 'CountyCode',
            'alias': 'County Code',
            'type': 'Short Int'
        },
        {
            'destination': 'Aquifer',
            'source': 'AquiferName',
            'alias': 'Aquifer',
            'type': 'String',
            'length': 100
        },
        {
            'destination': 'FmType',
            'source': 'FormationTypeText',
            'alias': 'Formation Type',
            'type': 'String',
            'length': 100
        },
        {
            'destination': 'AquiferType',
            'source': 'AquiferTypeName',
            'alias': 'Aquifer Type',
            'type': 'String',
            'length': 100
        },
        {
            'destination': 'ConstDate',
            'source': 'ConstructionDateText',
            'alias': 'Construction Date',
            'type': 'Date',
            'length': 8
        },
        {
            'destination': 'Depth',
            'source': 'WellDepthMeasure/MeasureValue',
            'alias': 'Well Depth',
            'type': 'Double'
        },
        {
            'destination': 'DepthUnit',
            'source': 'WellDepthMeasure/MeasureUnitCode',
            'alias': 'Well Depth Units',
            'type': 'String',
            'length': 10
        },
        {
            'destination': 'HoleDepth',
            'source': 'WellDepthMeasure/MeasureUnitCode',
            'alias': 'Hole Depth',
            'type': 'Double'
        },
        {
            'destination': 'HoleDUnit',
            'source': 'WellHoleDepthMeasure/MeasureUnitCode',
            'alias': 'Hole Depth Units',
            'type': 'String',
            'length': 10
        },
        {
            'destination': 'demELEVm',
            'source': None,
            'alias': 'DEM Elevation m',
            'type': 'Double'
        },
        {
            'destination': 'DataSource',
            'source': None,
            'alias': 'Database Source',
            'type': 'String',
            'length': 20
        },
        {
            'destination': 'WIN',
            'source': None,
            'alias': 'WR Well Id',
            'type': 'Long Int'
        }
    ]

    result_gdoc_schema = [
        {
            'destination': 'AnalysisDate',
            'source': 'AnalysisStartDate',
            'alias': 'Analysis Start Date',
            'type': 'Date'
        },
        {
            'destination': 'AnalytMeth',
            'source': 'ResultAnalyticalMethod/MethodName',
            'alias': 'Analytical Method Name',
            'type': 'Text',
            'length': 150
        },
        {
            'destination': 'AnalytMethId',
            'source': 'ResultAnalyticalMethod/MethodIdentifier',
            'alias': 'Analytical Method Id',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'AutoQual',
            'source': None,
            'alias': 'Auto Quality Check',
            'type': 'Text'
        },
        {
            'destination': 'CAS_Reg',
            'source': None,
            'alias': 'CAS Registry',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'Chrg',
            'source': None,
            'alias': 'Charge',
            'type': 'Float'
        },
        {
            'destination': 'DataSource',
            'source': None,
            'alias': 'Database Source',
            'type': 'Text'
        },
        {
            'destination': 'DetectCond',
            'source': 'ResultDetectionConditionText',
            'alias': 'Result Detection Condition',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'IdNum',
            'source': None,
            'alias': 'Unique Id',
            'type': 'Long Int'
        },
        {
            'destination': 'LabComments',
            'source': 'ResultLaboratoryCommentText',
            'alias': 'Laboratory Comment',
            'type': 'Text',
            'length': 500
        },
        {
            'destination': 'LabName',
            'source': 'LaboratoryName',
            'alias': 'Laboratory Name',
            'type': 'Text',
            'length': 100
        },
        {
            'destination': 'Lat_Y',
            'source': None,
            'alias': 'Latitude',
            'type': 'Double'
        },
        {
            'destination': 'LimitType',
            'source': 'DetectionQuantitationLimitTypeName',
            'alias': 'Detection Limit Type',
            'type': 'Text',
            'length': 250
        },
        {
            'destination': 'Lon_X',
            'source': None,
            'alias': 'Longitude',
            'type': 'Double'
        },
        {
            'destination': 'MDL',
            'source': 'DetectionQuantitationLimitMeasure/MeasureValue',
            'alias': 'Detection Quantitation Limit',
            'type': 'Double'
        },
        {
            'destination': 'MDLUnit',
            'source': 'DetectionQuantitationLimitMeasure/MeasureUnitCode',
            'alias': 'Detection Quantitation Limit Unit',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'MethodDescript',
            'source': 'MethodDescriptionText',
            'alias': 'Method Description',
            'type': 'Text',
            'length': 100
        },
        {
            'destination': 'OrgId',
            'source': 'OrganizationIdentifier',
            'alias': 'Organization Id',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'OrgName',
            'source': 'OrganizationFormalName',
            'alias': 'Organization Name',
            'type': 'Text',
            'length': 150
        },
        {
            'destination': 'Param',
            'source': 'CharacteristicName',
            'alias': 'Parameter',
            'type': 'Text',
            'length': 500
        },
        {
            'destination': 'ParamGroup',
            'source': None,
            'alias': 'Parameter Group',
            'type': 'Text'
        },
        {
            'destination': 'ProjectId',
            'source': 'ProjectIdentifier',
            'alias': 'Project Id',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'QualCode',
            'source': 'MeasureQualifierCode',
            'alias': 'Measure Qualifier Code',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'ResultComment',
            'source': 'ResultCommentText',
            'alias': 'Result Comment',
            'type': 'Text',
            'length': 1500
        },
        {
            'destination': 'ResultStatus',
            'source': 'ResultStatusIdentifier',
            'alias': 'Result Status',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'ResultValue',
            'source': 'ResultMeasureValue',
            'alias': 'Result Measure Value',
            'type': 'Double'
        },
        {
            'destination': 'SampComment',
            'source': 'ActivityCommentText',
            'alias': 'Sample Comment',
            'type': 'Text'
        },
        {
            'destination': 'SampDepth',
            'source': 'ActivityDepthHeightMeasure/MeasureValue',
            'alias': 'Sample Depth',
            'type': 'Double'
        },
        {
            'destination': 'SampDepthRef',
            'source': 'ActivityDepthAltitudeReferencePointText',
            'alias': 'Sample Depth Reference',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'SampDepthU',
            'source': 'ActivityDepthHeightMeasure/MeasureUnitCode',
            'alias': 'Sample Depth Units',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'SampEquip',
            'source': 'SampleCollectionEquipmentName',
            'alias': 'Collection Equipment',
            'type': 'Text',
            'length': 75
        },
        {
            'destination': 'SampFrac',
            'source': 'ResultSampleFractionText',
            'alias': 'Result Sample Fraction',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'SampleDate',
            'source': 'ActivityStartDate',
            'alias': 'Sample Date',
            'type': 'Date'
        },
        {
            'destination': 'SampleTime',
            'source': 'ActivityStartTime/Time',
            'alias': 'Sample Time',
            'type': 'Time'
        },
        {
            'destination': 'SampleId',
            'source': 'ActivityIdentifier',
            'alias': 'Sample Id',
            'type': 'Text',
            'length': 100
        },
        {
            'destination': 'SampMedia',
            'source': 'ActivityMediaSubdivisionName',
            'alias': 'Sample Media',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'SampMeth',
            'source': 'SampleCollectionMethod/MethodIdentifier',
            'alias': 'Collection Method',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'SampMethName',
            'source': 'SampleCollectionMethod/MethodName',
            'alias': 'Collection Method Name',
            'type': 'Text',
            'length': 75
        },
        {
            'destination': 'SampType',
            'source': 'ActivityTypeCode',
            'alias': 'Sample Type',
            'type': 'Text',
            'length': 75
        },
        {
            'destination': 'StationId',
            'source': 'MonitoringLocationIdentifier',
            'alias': 'Station Id',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'Unit',
            'source': 'ResultMeasure/MeasureUnitCode',
            'alias': 'Result Measure Unit',
            'type': 'Text',
            'length': 50
        },
        {
            'destination': 'USGSPCode',
            'source': 'USGSPCode',
            'alias': 'USGS P Code',
            'type': 'Text',
            'length': 50
        }
    ]

    def __init__(self):
        pass

    def validate_schema(self, file_location):
        if self.get_extension(file_location) != ".shp":
            file_location = self.get_featureclass_from_fgdb(file_location)

        if file_location is None:
            return False

        properties = arcpy.Describe(file_location)

        input_schema = set([])

        for field in properties.fields:
            if field.type == 'String':
                input_schema.add((field.name, field.type, field.length))
            elif field.type == 'Date' or field.type == 'Geometry':
                input_schema.add((field.name, field.type))
            elif field.type == 'Double':
                input_schema.add((field.name, field.type))

        return self.required_schema - input_schema

        class Field(object):

            """a field model for taking the data in gdoc
            and transform it into the data for the addfield gp tool"""

            #: the field name to add to the feature class
            field_name = None

            #: the field type
            field_type = None

            #: the length of the field. Only useful for type String
            field_length = None

            #: the fields alias name
            field_alias = None

            def __init__(self, arg):
                """ args should be a set of field options
                (column, alias, type, ?length)"""

                self.field_name = arg[0]
                self.field_alias = arg[1]
                self.field_type = self.etl_type(arg[2])

                if self.field_type == 'TEXT':
                    self.field_length = arg[3]

            def etl_type(self, field_type):
                """Turn schema types into acpy fields types"""

                # arcpy wants field types upper case
                field_type = field_type.upper()

                # fields names are pretty similar if you remove int
                field_type.strip('INT')

                if field_type == 'STRING':
                    return 'TEXT'
                else:
                    return field_type

    @property
    def station(self):
        return self.station_gdoc_schema

    @property
    def result(self):
        return self.result_gdoc_schema
