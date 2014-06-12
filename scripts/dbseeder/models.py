"""module containing project models"""

import datetime
import os
from collections import OrderedDict
from dateutil.parser import parse


class TableInfo(object):

    def __init__(self, location, name):
        self.location = os.path.join(location, name)
        self.name = name


class Table(object):

    def __init__(self, row):
        """
            this base class takes a csv row
            it then pulls all of the values out via the schema map
            and creates a row object that is ordered correctly for
            inserting into the feature class
        """

        self._row = []

        for key in self.schema_map.keys():
            #: the key index maps to the column index in the feature class
            etl_info = self.schema_map[key]
            source_field_name = etl_info['source']
            destination_field_type = Field(etl_info).field_type

            #: not all of the programs have the same schema
            if source_field_name not in row:
                self._row.append(None)
                continue

            destination_value = row[source_field_name].strip()

            if destination_field_type == 'TEXT':
                cast = str
            elif destination_field_type == 'LONG':
                cast = long
            elif destination_field_type == 'SHORT':
                cast = int
            elif (destination_field_type == 'FLOAT' or
                  destination_field_type == 'DOUBLE'):
                cast = float
            elif destination_field_type == 'DATE':
                cast = parse

            value = cast(destination_value)

            self._row.append(value)

    def _build_schema_map(self, schema):
        results_schema = schema
        schema_index_items = {}

        for item in results_schema:
            schema_index_items.update({item['index']: item})

        return OrderedDict(schema_index_items)

    @property
    def row(self):
        return self._row


class Results(Table):

    """ORM mapping to station schema to Results table"""

    def __init__(self, row):
        self.schema_map = self._build_schema_map(Schema().result)
        super(Results, self).__init__(row)

    schema_map = None


class Stations(Table):

    """ORM mapping from chemistry schema to Stations feature class"""

    def __init__(self, row):
        self.schema_map = self._build_schema_map(Schema().station)
        super(Stations, self).__init__(row)

    schema_map = None


class Sdwis(object):

    """base class for building sdwis schema map"""

    def __init__(self, row):
        """
            this base class takes a csv row
            it then pulls all of the values out via the schema map
            and creates a row object that is ordered correctly for
            inserting into the feature class
        """

        #: probably should refactor this out.
        #: it's here to get the schema map from an empty object
        if row is None or len(row) < 1:
            return

        self._row = []

        for key in self.schema_map.keys():
            #: the key index maps to the column index in the feature class
            etl_info = self.schema_map[key]
            destination_field_name = etl_info['destination']
            destination_field_type = Field(etl_info).field_type

            #: not all of the programs have the same schema
            if destination_field_name not in self.fields:
                self._row.append(None)
                continue

            destination_value = row[self.fields[destination_field_name]]
            if destination_value is None:
                self._row.append(None)
                continue

            try:
                destination_value = destination_value.strip()
            except:
                pass

            if destination_field_type == 'TEXT':
                cast = str
            elif destination_field_type == 'LONG':
                cast = long
            elif destination_field_type == 'SHORT':
                cast = int
            elif (destination_field_type == 'FLOAT' or
                  destination_field_type == 'DOUBLE'):
                cast = float
            elif destination_field_type == 'DATE':
                if isinstance(destination_value, datetime.datetime):
                    cast = lambda x: x
                else:
                    cast = parse

            value = cast(destination_value)

            self._row.append(value)

    def _build_schema_map(self, schema):
        results_schema = schema
        schema_index_items = {}

        for item in results_schema:
            schema_index_items.update({item['index']: item})

        return OrderedDict(schema_index_items)

    @property
    def row(self):
        return self._row


class SdwisResults(Sdwis):

    fields = OrderedDict([
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

    def __init__(self, row):
        self.schema_map = self._build_schema_map(Schema().result)
        super(SdwisResults, self).__init__(row)

    schema_map = None


class SdwisStations(Sdwis):

    fields = OrderedDict([
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

    def __init__(self, row):
        self.schema_map = self._build_schema_map(Schema().result)
        super(SdwisStations, self).__init__(row)

    schema_map = None


class Schema(object):

    """a class defining the schema for the gdb and also checks for validity"""

    station_gdoc_schema = [
        {
            'destination': 'OrgId',
            'source': 'OrganizationIdentifier',
            'alias': 'Organization Id',
            'type': 'String',
            'length': 20,
            'index': 0
        },
        {
            'destination': 'OrgName',
            'source': 'OrganizationFormalName',
            'alias': 'Organization Name',
            'type': 'String',
            'length': 100,
            'index': 1
        },
        {
            'destination': 'StationId',
            'source': 'MonitoringLocationIdentifier',
            'alias': 'Monitoring Location Id',
            'type': 'String',
            'length': 100,
            'index': 2
        },
        {
            'destination': 'StationName',
            'source': 'MonitoringLocationName',
            'alias': 'Monitoring Location Name',
            'type': 'String',
            'length': 100,
            'index': 3
        },
        {
            'destination': 'StationType',
            'source': 'MonitoringLocationTypeName',
            'alias': 'Monitoring Location Type',
            'type': 'String',
            'length': 100,
            'index': 4
        },
        {
            'destination': 'StationComment',
            'source': 'MonitoringLocationDescriptionText',
            'alias': 'Monitoring Location Description',
            'type': 'String',
            'length': 1500,
            'index': 5
        },
        {
            'destination': 'HUC8',
            'source': 'HUCEightDigitCode',
            'alias': 'HUC 8 Digit Code',
            'type': 'String',
            'length': 8,
            'index': 6
        },
        {
            'destination': 'Lon_X',
            'source': 'LongitudeMeasure',
            'alias': 'Latitude',
            'type': 'Double',
            'index': 7
        },
        {
            'destination': 'Lat_Y',
            'source': 'LatitudeMeasure',
            'alias': 'Longitude',
            'type': 'Double',
            'index': 8
        },
        {
            'destination': 'HorAcc',
            'source': 'HorizontalAccuracyMeasure/MeasureValue',
            'alias': 'Horizontal Accuracy',
            'type': 'Double',
            'index': 9
        },
        {
            'destination': 'HorAccUnit',
            'source': 'HorizontalAccuracyMeasure/MeasureUnitCode',
            'alias': 'Horizontal Accuracy Unit',
            'type': 'String',
            'length': 10,
            'index': 10
        },
        {
            'destination': 'HorCollMeth',
            'source': 'HorizontalCollectionMethodName',
            'alias': 'Horizontal Collection Method',
            'type': 'String',
            'length': 100,
            'index': 11
        },
        {
            'destination': 'HorRef',
            'source': 'HorizontalCoordinateReferenceSystemDatumName',
            'alias': 'Horizontal Reference Datum',
            'type': 'String',
            'length': 10,
            'index': 12
        },
        {
            'destination': 'Elev',
            'source': 'VerticalMeasure/MeasureValue',
            'alias': 'Elevation',
            'type': 'Double',
            'index': 13
        },
        {
            'destination': 'ElevUnit',
            'source': 'VerticalMeasure/MeasureUnitCode',
            'alias': 'Elevation Unit',
            'type': 'String',
            'length': 15,
            'index': 14
        },
        {
            'destination': 'ElevAcc',
            'source': 'VerticalAccuracyMeasure/MeasureValue',
            'alias': 'Elevation Accuracy',
            'type': 'Double',
            'index': 15
        },
        {
            'destination': 'ElevAccUnit',
            'source': 'VerticalAccuracyMeasure/MeasureUnitCode',
            'alias': 'Elevation Accuracy Units',
            'type': 'String',
            'length': 4,
            'index': 16
        },
        {
            'destination': 'ElevMeth',
            'source': 'VerticalCollectionMethodName',
            'alias': 'Elevation Collection Method',
            'type': 'String',
            'length': 100,
            'index': 17
        },
        {
            'destination': 'ElevRef',
            'source': 'VerticalCoordinateReferenceSystemDatumName',
            'alias': 'Elevation Reference Datum',
            'type': 'String',
            'length': 12,
            'index': 18
        },
        {
            'destination': 'StateCode',
            'source': 'StateCode',
            'alias': 'State Code',
            'type': 'Short Int',
            'index': 19
        },
        {
            'destination': 'CountyCode',
            'source': 'CountyCode',
            'alias': 'County Code',
            'type': 'Short Int',
            'index': 20
        },
        {
            'destination': 'Aquifer',
            'source': 'AquiferName',
            'alias': 'Aquifer',
            'type': 'String',
            'length': 100,
            'index': 21
        },
        {
            'destination': 'FmType',
            'source': 'FormationTypeText',
            'alias': 'Formation Type',
            'type': 'String',
            'length': 100,
            'index': 22
        },
        {
            'destination': 'AquiferType',
            'source': 'AquiferTypeName',
            'alias': 'Aquifer Type',
            'type': 'String',
            'length': 100,
            'index': 23
        },
        {
            'destination': 'ConstDate',
            'source': 'ConstructionDateText',
            'alias': 'Construction Date',
            'type': 'Date',
            'length': 8,
            'index': 24
        },
        {
            'destination': 'Depth',
            'source': 'WellDepthMeasure/MeasureValue',
            'alias': 'Well Depth',
            'type': 'Double',
            'index': 25
        },
        {
            'destination': 'DepthUnit',
            'source': 'WellDepthMeasure/MeasureUnitCode',
            'alias': 'Well Depth Units',
            'type': 'String',
            'length': 10,
            'index': 26
        },
        {
            'destination': 'HoleDepth',
            'source': 'WellDepthMeasure/MeasureUnitCode',
            'alias': 'Hole Depth',
            'type': 'Double',
            'index': 27
        },
        {
            'destination': 'HoleDUnit',
            'source': 'WellHoleDepthMeasure/MeasureUnitCode',
            'alias': 'Hole Depth Units',
            'type': 'String',
            'length': 10,
            'index': 28
        },
        {
            'destination': 'demELEVm',
            'source': None,
            'alias': 'DEM Elevation m',
            'type': 'Double',
            'index': 29
        },
        {
            'destination': 'DataSource',
            'source': None,
            'alias': 'Database Source',
            'type': 'String',
            'length': 20,
            'index': 30
        },
        {
            'destination': 'WIN',
            'source': None,
            'alias': 'WR Well Id',
            'type': 'Long Int',
            'index': 31
        }
    ]

    result_gdoc_schema = [
        {
            'destination': 'AnalysisDate',
            'source': 'AnalysisStartDate',
            'alias': 'Analysis Start Date',
            'type': 'Date',
            'index': 0
        },
        {
            'destination': 'AnalytMeth',
            'source': 'ResultAnalyticalMethod/MethodName',
            'alias': 'Analytical Method Name',
            'type': 'Text',
            'length': 150,
            'index': 1
        },
        {
            'destination': 'AnalytMethId',
            'source': 'ResultAnalyticalMethod/MethodIdentifier',
            'alias': 'Analytical Method Id',
            'type': 'Text',
            'length': 50,
            'index': 2
        },
        {
            'destination': 'AutoQual',
            'source': None,
            'alias': 'Auto Quality Check',
            'type': 'Text',
            'index': 3
        },
        {
            'destination': 'CAS_Reg',
            'source': None,
            'alias': 'CAS Registry',
            'type': 'Text',
            'length': 50,
            'index': 4
        },
        {
            'destination': 'Chrg',
            'source': None,
            'alias': 'Charge',
            'type': 'Float',
            'index': 5
        },
        {
            'destination': 'DataSource',
            'source': None,
            'alias': 'Database Source',
            'type': 'Text',
            'index': 6
        },
        {
            'destination': 'DetectCond',
            'source': 'ResultDetectionConditionText',
            'alias': 'Result Detection Condition',
            'type': 'Text',
            'length': 50,
            'index': 7
        },
        {
            'destination': 'IdNum',
            'source': None,
            'alias': 'Unique Id',
            'type': 'Long Int',
            'index': 8
        },
        {
            'destination': 'LabComments',
            'source': 'ResultLaboratoryCommentText',
            'alias': 'Laboratory Comment',
            'type': 'Text',
            'length': 500,
            'index': 9
        },
        {
            'destination': 'LabName',
            'source': 'LaboratoryName',
            'alias': 'Laboratory Name',
            'type': 'Text',
            'length': 100,
            'index': 10
        },
        {
            'destination': 'Lat_Y',
            'source': None,
            'alias': 'Latitude',
            'type': 'Double',
            'index': 11
        },
        {
            'destination': 'LimitType',
            'source': 'DetectionQuantitationLimitTypeName',
            'alias': 'Detection Limit Type',
            'type': 'Text',
            'length': 250,
            'index': 12
        },
        {
            'destination': 'Lon_X',
            'source': None,
            'alias': 'Longitude',
            'type': 'Double',
            'index': 13
        },
        {
            'destination': 'MDL',
            'source': 'DetectionQuantitationLimitMeasure/MeasureValue',
            'alias': 'Detection Quantitation Limit',
            'type': 'Double',
            'index': 14
        },
        {
            'destination': 'MDLUnit',
            'source': 'DetectionQuantitationLimitMeasure/MeasureUnitCode',
            'alias': 'Detection Quantitation Limit Unit',
            'type': 'Text',
            'length': 50,
            'index': 15
        },
        {
            'destination': 'MethodDescript',
            'source': 'MethodDescriptionText',
            'alias': 'Method Description',
            'type': 'Text',
            'length': 100,
            'index': 16
        },
        {
            'destination': 'OrgId',
            'source': 'OrganizationIdentifier',
            'alias': 'Organization Id',
            'type': 'Text',
            'length': 50,
            'index': 17
        },
        {
            'destination': 'OrgName',
            'source': 'OrganizationFormalName',
            'alias': 'Organization Name',
            'type': 'Text',
            'length': 150,
            'index': 18
        },
        {
            'destination': 'Param',
            'source': 'CharacteristicName',
            'alias': 'Parameter',
            'type': 'Text',
            'length': 500,
            'index': 19
        },
        {
            'destination': 'ParamGroup',
            'source': None,
            'alias': 'Parameter Group',
            'type': 'Text',
            'index': 20
        },
        {
            'destination': 'ProjectId',
            'source': 'ProjectIdentifier',
            'alias': 'Project Id',
            'type': 'Text',
            'length': 50,
            'index': 21
        },
        {
            'destination': 'QualCode',
            'source': 'MeasureQualifierCode',
            'alias': 'Measure Qualifier Code',
            'type': 'Text',
            'length': 50,
            'index': 22
        },
        {
            'destination': 'ResultComment',
            'source': 'ResultCommentText',
            'alias': 'Result Comment',
            'type': 'Text',
            'length': 1500,
            'index': 23
        },
        {
            'destination': 'ResultStatus',
            'source': 'ResultStatusIdentifier',
            'alias': 'Result Status',
            'type': 'Text',
            'length': 50,
            'index': 24
        },
        {
            'destination': 'ResultValue',
            'source': 'ResultMeasureValue',
            'alias': 'Result Measure Value',
            'type': 'Double',
            'index': 25
        },
        {
            'destination': 'SampComment',
            'source': 'ActivityCommentText',
            'alias': 'Sample Comment',
            'type': 'Text',
            'index': 26
        },
        {
            'destination': 'SampDepth',
            'source': 'ActivityDepthHeightMeasure/MeasureValue',
            'alias': 'Sample Depth',
            'type': 'Double',
            'index': 27
        },
        {
            'destination': 'SampDepthRef',
            'source': 'ActivityDepthAltitudeReferencePointText',
            'alias': 'Sample Depth Reference',
            'type': 'Text',
            'length': 50,
            'index': 28
        },
        {
            'destination': 'SampDepthU',
            'source': 'ActivityDepthHeightMeasure/MeasureUnitCode',
            'alias': 'Sample Depth Units',
            'type': 'Text',
            'length': 50,
            'index': 29
        },
        {
            'destination': 'SampEquip',
            'source': 'SampleCollectionEquipmentName',
            'alias': 'Collection Equipment',
            'type': 'Text',
            'length': 75,
            'index': 30
        },
        {
            'destination': 'SampFrac',
            'source': 'ResultSampleFractionText',
            'alias': 'Result Sample Fraction',
            'type': 'Text',
            'length': 50,
            'index': 31
        },
        {
            'destination': 'SampleDate',
            'source': 'ActivityStartDate',
            'alias': 'Sample Date',
            'type': 'Date',
            'index': 32
        },
        {
            'destination': 'SampleTime',
            'source': 'ActivityStartTime/Time',
            'alias': 'Sample Time',
            'type': 'Time',
            'index': 33
        },
        {
            'destination': 'SampleId',
            'source': 'ActivityIdentifier',
            'alias': 'Sample Id',
            'type': 'Text',
            'length': 100,
            'index': 34
        },
        {
            'destination': 'SampMedia',
            'source': 'ActivityMediaSubdivisionName',
            'alias': 'Sample Media',
            'type': 'Text',
            'length': 50,
            'index': 35
        },
        {
            'destination': 'SampMeth',
            'source': 'SampleCollectionMethod/MethodIdentifier',
            'alias': 'Collection Method',
            'type': 'Text',
            'length': 50,
            'index': 36
        },
        {
            'destination': 'SampMethName',
            'source': 'SampleCollectionMethod/MethodName',
            'alias': 'Collection Method Name',
            'type': 'Text',
            'length': 75,
            'index': 37
        },
        {
            'destination': 'SampType',
            'source': 'ActivityTypeCode',
            'alias': 'Sample Type',
            'type': 'Text',
            'length': 75,
            'index': 38
        },
        {
            'destination': 'StationId',
            'source': 'MonitoringLocationIdentifier',
            'alias': 'Station Id',
            'type': 'Text',
            'length': 50,
            'index': 39
        },
        {
            'destination': 'Unit',
            'source': 'ResultMeasure/MeasureUnitCode',
            'alias': 'Result Measure Unit',
            'type': 'Text',
            'length': 50,
            'index': 40
        },
        {
            'destination': 'USGSPCode',
            'source': 'USGSPCode',
            'alias': 'USGS P Code',
            'type': 'Text',
            'length': 50,
            'index': 41
        }
    ]

    def __init__(self):
        pass

    # def validate_schema(self, file_location):
    #     if self.get_extension(file_location) != ".shp":
    #         file_location = self.get_featureclass_from_fgdb(file_location)

    #     if file_location is None:
    #         return False

    #     properties = arcpy.Describe(file_location)

    #     input_schema = set([])

    #     for field in properties.fields:
    #         if field.type == 'String':
    #             input_schema.add((field.name, field.type, field.length))
    #         elif field.type == 'Date' or field.type == 'Geometry':
    #             input_schema.add((field.name, field.type))
    #         elif field.type == 'Double':
    #             input_schema.add((field.name, field.type))

    #     return self.required_schema - input_schema

    @property
    def station(self):
        return self.station_gdoc_schema

    @property
    def result(self):
        return self.result_gdoc_schema


class Field(object):

    """a field model for taking the data in gdoc
    and transform it into the data for the addfield gp tool"""

    #: the field name to add to the feature class
    field_name = None

    #: the fields alias name
    field_alias = None

    #: the field type
    field_type = None

    #: the length of the field. Only useful for type String
    field_length = None

    #: the field length default if none is set
    length_default = 50

    def __init__(self, arg):
        """ args should be a set of field options
        (column, alias, type, ?length)"""

        self.field_name = arg['destination']
        self.field_alias = arg['alias']
        self.field_type = self.etl_type(arg['type'])

        if self.field_type == 'TEXT':
            try:
                self.field_length = arg['length']
            except KeyError:
                print ('{} is of type text and '.format(self.field_name) +
                       'has no limit set.' +
                       ' Defaulting to {}'.format(self.length_default))

    def etl_type(self, field_type):
        """Turn schema types into acpy fields types"""

        # arcpy wants field types upper case
        field_type = field_type.upper()

        # fields names are pretty similar if you remove int
        field_type = field_type.replace('INT', '').strip()

        if field_type == 'STRING':
            return 'TEXT'
        elif field_type == 'TIME':
            return 'DATE'
        else:
            return field_type
