"""module containing project models"""

import os
from collections import OrderedDict
from services import Caster, Project, Normalizable


class TableInfo(object):

    def __init__(self, location, name):
        self.location = os.path.join(location, name)
        self.name = name


class WqpTable(Normalizable):

    def __init__(self, normalizer):
        """
            this base class takes a csv row
            it then pulls all of the values out via the schema map
            and creates a row object that is ordered correctly for
            inserting into the feature class
            normalizer: the service to normalize the goods
        """

        super(WqpTable, self).__init__(normalizer)

    @staticmethod
    def build_schema_map(schema):
        schema_index_items = OrderedDict()

        if isinstance(schema, basestring):
            if schema == 'Stations':
                schema = Schema().station
            elif schema == 'Results':
                schema = Schema().result

        for item in schema:
            schema_index_items.update({item['index']: Field(item)})

        return OrderedDict(schema_index_items)

    def _etl_row(self, row, schema_map, model_type):
        _row = []
        lat = lon = None

        for i, key in enumerate(schema_map):
            #: the key index maps to the column index in the feature class
            field = schema_map[key]
            source_field_name = field.field_source
            destination_field_type = field.field_type

            #: not all of the programs have the same schema
            if source_field_name not in row:
                _row.append(None)
                self.update_normalize(field.field_name, None, i)
                continue

            try:
                value = row[source_field_name].strip()
            except IndexError:
                value = None

            value = Caster.cast(value, destination_field_type)

            if field.field_name == 'Lon_X':
                lon = value
            elif field.field_name == 'Lat_Y':
                lat = value

            self.update_normalize(field.field_name, value, i)

            _row.append(value)

        _row = self.normalize(_row)

        if model_type == 'Station':
            try:
                x, y = Project().to_utm(lon, lat)

                if x and y:
                    _row.append((x, y))
            except Exception as detail:
                print 'Handling projection error:', detail

        return _row


class Table(Normalizable):

    def __init__(self, normalizer):
        super(Table, self).__init__(normalizer)

    @staticmethod
    def build_schema_map(schema):
        schema_index_items = OrderedDict()

        if isinstance(schema, basestring):
            if schema == 'Stations':
                schema = Schema().station
            elif schema == 'Results':
                schema = Schema().result

        for item in schema:
            schema_index_items.update({item['destination']: Field(item)})

        return OrderedDict(schema_index_items)

    def _etl_row(self, row, schema_map, model_type):
        _row = []

        for i, field_name in enumerate(schema_map):
            if field_name not in self.fields:
                _row.append(None)
                continue

            try:
                value = row[self.fields.index(field_name)]
            except IndexError:
                value = None

            field = schema_map[field_name]
            value = Caster.cast(value, field.field_type)

            self.update_normalize(field_name, value, i)

            _row.append(value)

        _row = self.normalize(_row)

        if model_type == 'Station':
            has_utm = False
            try:
                utmx_index = self.fields.index('UTM_X')
                utmy_index = self.fields.index('UTM_Y')
                has_utm = True
            except ValueError:
                pass

            try:
                utmx_index = self.fields.index('X_UTM')
                utmy_index = self.fields.index('Y_UTM')
                has_utm = True
            except ValueError:
                pass

            if has_utm:
                x = row[utmx_index]
                y = row[utmy_index]
            else:
                try:
                    x_index = self.fields.index('Lon_X')
                    y_index = self.fields.index('Lat_Y')

                    x, y = Project().to_utm(row[x_index], row[y_index])
                except Exception as detail:
                    print 'Handling projection error:', detail

            _row.append((x, y))

        return _row


class WqpResult(WqpTable):

    """ORM mapping to station schema to WqpResult table"""

    def __init__(self, row,  normalizer):
        super(WqpResult, self).__init__(normalizer)

        schema = Schema().result
        self.fields = range(0, len(schema))

        schema_map = WqpTable.build_schema_map(schema)
        self.row = self._etl_row(row, schema_map, 'Result')


class WqpStation(WqpTable):

    """ORM mapping from chemistry schema to WqpStation feature class"""

    def __init__(self, row, normalizer):
        super(WqpStation, self).__init__(normalizer)

        schema = Schema().station
        self.fields = range(0, len(schema))

        schema_map = WqpTable.build_schema_map(schema)
        self.row = self._etl_row(row, schema_map, 'Station')


class SdwisResult(Table):

    fields = ['AnalysisDate',
              'LabName',
              'MDL',
              'MDLUnit',
              'OrgId',
              'OrgName',
              'Param',
              'ResultValue',
              'SampleDate',
              'SampleTime',
              'SampleId',
              'SampType',
              'StationId',
              'Unit',
              'Lat_Y',
              'Lon_X',
              'CAS_Reg',
              'IdNum',
              'ParamGroup']

    def __init__(self, row, normalizer):
        super(SdwisResult, self).__init__(normalizer)

        schema = Schema().result

        schema_map = Table.build_schema_map(schema)
        self.row = self._etl_row(row, schema_map, 'Result')


class SdwisStation(Table):

    fields = ['OrgId',
              'OrgName',
              'StationId',
              'StationName',
              'StationType',
              'Lat_Y',
              'Lon_X',
              'HorAcc',
              'HorCollMeth',
              'HorRef',
              'Elev',
              'ElevAcc',
              'ElevMeth',
              'ElevRef',
              'Depth',
              'DepthUnit']

    def __init__(self, row, normalizer):
        super(SdwisStation, self).__init__(normalizer)

        schema = Schema().station

        schema_map = Table.build_schema_map(schema)
        self.row = self._etl_row(row, schema_map, 'Station')


class OgmResult(Table):

    """docstring for OgmResult"""

    fields = ['StationId',
              'Param',
              'SampleId',
              'SampleDate',
              'AnalysisDate',
              'AnalytMeth',
              'MDLUnit',
              'ResultValue',
              'SampleTime',
              'MDL',
              'Unit',
              'SampComment']

    def __init__(self, row, normalizer):
        super(OgmResult, self).__init__(normalizer)

        #: add paramgroup in ctor so `Type.fields` works for reads
        #: since paragroup does not exist in source data
        self.fields.append('ParamGroup')

        self.schema = Schema().result

        self.schema_map = Table.build_schema_map(self.schema)
        self.row = self._etl_row(row, self.schema_map, 'Result')


class OgmStation(Table):

    """docstring for OgmStation"""

    fields = ['OrgId',
              'OrgName',
              'StationId',
              'StationName',
              'Elev',
              'ElevUnit',
              'StationType',
              'StationComment',
              'Lat_Y',
              'Lon_X',
              'UTM_X',
              'UTM_Y']

    def __init__(self, row, normalizer):
        super(OgmStation, self).__init__(normalizer)

        self.schema = Schema().station

        self.schema_map = Table.build_schema_map(self.schema)
        self.row = self._etl_row(row, self.schema_map, 'Station')


class DwrResult(Table):

    fields = ['SampleDate',
              'USGSPCode',
              'ResultValue',
              'Param',
              'Unit',
              'SampFrac',
              'OrgId',
              'OrgName',
              'StationId',
              'Lat_Y',
              'Lon_X',
              'SampMedia',
              'SampleId',
              'IdNum']

    def __init__(self, row, normalizer):
        super(DwrResult, self).__init__(normalizer)

        #: add paramgroup in ctor so `Type.fields` works for reads
        #: since paragroup does not exist in source data
        self.fields.append('ParamGroup')

        self.schema = Schema().result

        self.schema_map = Table.build_schema_map(self.schema)
        self.row = self._etl_row(row, self.schema_map, 'Result')


class DwrStation(Table):

    fields = ['WIN',
              'OrgId',
              'OrgName',
              'StationId',
              'Lat_Y',
              'Lon_X',
              'StateCode',
              'CountyCode',
              'Depth',
              'HoleDepth',
              'HUC8',
              'StationName',
              'StationType',
              'X_UTM',
              'Y_UTM']

    def __init__(self, row, normalizer):
        super(DwrStation, self).__init__(normalizer)

        self.schema = Schema().station

        self.schema_map = Table.build_schema_map(self.schema)
        self.row = self._etl_row(row, self.schema_map, 'Station')


class UgsResult(Table):

    fields = ['ResultValue',
              'AnalysisDate',
              'OrgId',
              'OrgName',
              'SampleDate',
              'SampleTime',
              'DetectCond',
              'Unit',
              'MDLUnit',
              'AnalytMethId',
              'AnalytMeth',
              'SampMedia',
              'SampFrac',
              'StationId',
              'MDL',
              'IdNum',
              'LabName',
              'SampComment',
              'CAS_Reg']

    def __init__(self, row, normalizer):
        super(UgsResult, self).__init__(normalizer)

        self.schema = Schema().result

        self.schema_map = Table.build_schema_map(self.schema)
        self.row = self._etl_row(row, self.schema_map, 'Result')


class UgsStation(Table):

    fields = ['OrgId',
              'DataSource',
              'HUC8',
              'StateCode',
              'CountyCode',
              'OrgName',
              'Lat_Y',
              'Lon_X',
              'StationName',
              'StationComment',
              'StationId']

    def __init__(self, row, normalizer):
        super(UgsStation, self).__init__(normalizer)

        self.schema = Schema().station

        self.schema_map = Table.build_schema_map(self.schema)
        self.row = self._etl_row(row, self.schema_map, 'Station')


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
            'source': 'WellHoleDepthMeasure/MeasureValue',
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
            'index': 26,
            'length': 500
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

    #: the source of the field mapping
    field_source = None

    #: the field length default if none is set
    length_default = 50

    def __init__(self, arg):
        """ args should be a set of field options
        (column, alias, type, ?length)"""

        self.field_name = arg['destination']
        self.field_alias = arg['alias']
        self.field_type = self._etl_type(arg['type'])
        self.field_source = arg['source']

        if self.field_type == 'TEXT':
            try:
                self.field_length = arg['length']
            except KeyError:
                pass
                # print ('{} is of type text and '.format(self.field_name) +
                #        'has no limit set.' +
                #        ' Defaulting to {}'.format(self.length_default))

    def _etl_type(self, field_type):
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


class Charges(object):

    """the model holding the charge balance input values"""

    chemical_amount = None

    def __init__(self):
        super(Charges, self).__init__()

        self.chemical_amount = {'ca': None,
                                'mg': None,
                                'na': None,
                                'k': None,
                                'cl': None,
                                'hco3': None,
                                'co3': None,
                                'so4': None,
                                'no2': None,
                                'no3': None,
                                'na+k': None}

    @property
    def calcium(self):
        return self._get_summed_value('ca')

    @property
    def magnesium(self):
        return self._get_summed_value('mg')

    @property
    def chloride(self):
        return self._get_summed_value('cl')

    @property
    def bicarbonate(self):
        return self._get_summed_value('hco3')

    @property
    def sulfate(self):
        return self._get_summed_value('so4')

    @property
    def carbonate(self):
        return self._get_summed_value('co3')

    @property
    def nitrate(self):
        return self._get_summed_value('no3')

    @property
    def nitrite(self):
        return self._get_summed_value('no2')

    @property
    def sodium(self):
        k = self._get_summed_value('k')
        na = self._get_summed_value('na')
        na_k = self._get_summed_value('na+k')

        if na_k is not None and k is not None and na is None:
            return na_k - k

        return na

    @property
    def potassium(self):
        k = self._get_summed_value('k')
        na = self._get_summed_value('na')
        na_k = self._get_summed_value('na+k')

        if na_k is not None and na is not None and k is None:
            return na_k - na

        return k

    @property
    def sodium_plus_potassium(self):
        nak = self._get_summed_value('na+k')
        k = self._get_summed_value('k')
        na = self._get_summed_value('na')

        if nak is not None and na is not None or k is not None:
            return 0

        return nak

    def update(self, chemical, amount, detect_cond=None):
        #: there was a problem with the sample disregard
        if detect_cond:
            return

        #: there is more than one sample for this chemical
        if self.chemical_amount[chemical] is not None:
            try:
                self.chemical_amount[chemical].append(amount)
            except AttributeError:
                #: turn into a list for summing
                self.chemical_amount[chemical] = [
                    self.chemical_amount[chemical], amount]

            return

        self.chemical_amount[chemical] = amount

    def has_major_params(self):
        """this should only be called once everything
        is complete and you want to do the charge balance
        calculation. Otherwise your averages will be off"""

        valid_chemicals = 5
        num_of_chemicals = 0

        if self.calcium is not None:
            num_of_chemicals += 1
        if self.magnesium is not None:
            num_of_chemicals += 1
        if self.chloride is not None:
            num_of_chemicals += 1
        if self.bicarbonate is not None:
            num_of_chemicals += 1
        if self.sulfate is not None:
            num_of_chemicals += 1

        valid = num_of_chemicals == valid_chemicals

        return valid and (
            self.sodium is not None or self.sodium_plus_potassium is not None)

    def _get_summed_value(self, key):
        """turn all of the arrays into numbers"""
        value = self.chemical_amount[key]
        try:
            return sum(value) / float(len(value))
        except TypeError:
            #: value is not an array
            pass

        return value
