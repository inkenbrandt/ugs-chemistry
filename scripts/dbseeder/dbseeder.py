"""DbSeeder creates and seeds esri file geodatabases"""

import arcpy
import argparse
import csv
import glob
import os
from models import TableInfo, Results, Stations
from pyproj import Proj, transform
from services import WebQuery, ConsolePrompt


class Seeder(object):
    parent_folder = None
    gdb_name = None
    location = None
    chemistry_query_url = None
    template_location = os.path.join(
        os.getcwd(), 'templates', 'Templates.gdb')

    def __init__(self, parent_folder='./', gdb_name='WQP.gdb'):
        self.parent_folder = parent_folder
        self.gdb_name = gdb_name
        self.location = os.path.join(self.parent_folder, self.gdb_name)

    def _create_gdb(self):
        arcpy.CreateFileGDB_management(self.parent_folder,
                                       self.gdb_name,
                                       'CURRENT')

    def _create_feature_classes(self, types):
        results_table = TableInfo(self.template_location, 'Results')
        station_points = TableInfo(self.template_location, 'Stations')

        if 'Results' in types:
            arcpy.CreateTable_management(self.location, 
                                            results_table.name, 
                                            results_table.template)

        if 'Stations' in types:
            arcpy.CreateFeatureclass_management(self.location,
                                                    station_points.name,
                                                    "POINT",
                                                    station_points.template,
                                                    "DISABLED",
                                                    "DISABLED",
                                                    station_points.template)

    def _query(self, url):
        data = WebQuery().results(url)

        return data

    def _read_response(self, data):
        reader = csv.DictReader(data, delimiter=',')

        return reader

    def _insert_rows(self, data, feature_class):
        location = os.path.join(self.location, feature_class)

        print 'inserting into {} type {}'.format(location, feature_class)

        if feature_class == 'Results':
            Type = Results
        elif feature_class == 'Stations':
            Type = Stations

        fields = Type.schema_map.keys()
        if feature_class == 'Stations':
            fields.append('SHAPE@XY')

        input_system = Proj(init='epsg:4326')
        ouput_system = Proj(init='epsg:26912')

        with arcpy.da.InsertCursor(location, fields) as curser:
            for row in data:
                etl = Type(row)
                insert_row = etl.row
                
                if feature_class == 'Stations':
                    lon = row[etl.schema_map['Lon_X']] 
                    lat = row[etl.schema_map['Lat_Y']]

                    try:
                        x, y = transform(input_system, ouput_system, lon, lat)
                        insert_row.append((x, y))
                    except:
                        insert_row.append(None)

                curser.insertRow(insert_row)

    def _csvs_on_disk(self, parent_folder, type):
        folder = os.path.join(parent_folder, type, '*.csv')
        for file in glob.glob(folder):
            yield file

    def get_field_lengths(self, folder, type):
        results = {
            'AnalysisStartDate': ['AnalysisDate', 0],
            'ResultAnalyticalMethod/MethodIdentifierContext': ['AnalytContext', 0],
            'ResultAnalyticalMethod/MethodName': ['AnalytMeth', 0],
            'ResultAnalyticalMethod/MethodIdentifier': ['AnalytMethId', 0],
            'ResultDetectionConditionText': ['DetectCond', 0],
            'ResultLaboratoryCommentText': ['LabComments', 0],
            'LaboratoryName': ['LabName', 0],
            'DetectionQuantitationLimitTypeName': ['LimitType', 0],
            'DetectionQuantitationLimitMeasure/MeasureValue': ['MDL', 0],
            'DetectionQuantitationLimitMeasure/MeasureUnitCode': ['MDLUnit', 0],
            'MethodDescriptionText': ['MethodDescript', 0],
            'OrganizationIdentifier': ['OrgId', 0],
            'OrganizationFormalName': ['OrgName', 0],
            'CharacteristicName': ['Param', 0],
            'ProjectIdentifier': ['ProjectId', 0],
            'MeasureQualifierCode': ['QualCode', 0],
            'ResultCommentText': ['ResultComment', 0],
            'ResultStatusIdentifier': ['ResultStatus', 0],
            'ResultMeasureValue': ['ResultValue', 0],
            'ActivityCommentText': ['SampComment', 0],
            'SampleCollectionMethod/MethodIdentifierContext': ['SampContext', 0],
            'ActivityDepthHeightMeasure/MeasureValue': ['SampDepth', 0],
            'ActivityDepthAltitudeReferencePointText': ['SampDepthRef', 0],
            'ActivityDepthHeightMeasure/MeasureUnitCode': ['SampDepthU', 0],
            'SampleCollectionEquipmentName': ['SampEquip', 0],
            'ResultSampleFractionText': ['SampFrac', 0],
            'ActivityStartDate': ['SampleDate', 0],
            'ActivityStartTime/Time': ['SampleTime', 0],
            'ActivityIdentifier': ['SampleId', 0],
            'ActivityMediaName': ['SampMedia', 0],
            'ActivityMediaSubdivisionName': ['SampMediaSub', 0],
            'SampleCollectionMethod/MethodIdentifier': ['SampMeth', 0],
            'SampleCollectionMethod/MethodName': ['SampMethName', 0],
            'ActivityTypeCode': ['SampType', 0],
            'MonitoringLocationIdentifier': ['StationId', 0],
            'ResultMeasure/MeasureUnitCode': ['Unit', 0],
            'USGSPCode': ['USGSPCode', 0]
        }

        stations = {
            'OrganizationIdentifier': ['OrgID', 0],
            'OrganizationFormalName': ['OrgName', 0],
            'MonitoringLocationIdentifier': ['StationsID', 0],
            'MonitoringLocationName': ['StationName', 0],
            'MonitoringLocationTypeName': ['StationType', 0],
            'MonitoringLocationDescriptionText': ['StationComment', 0],
            'HUCEightDigitCode': ['HUC8', 0],
            'LatitudeMeasure': ['Lat_Y', 0],
            'LongitudeMeasure': ['Lon_X', 0],
            'HorizontalAccuracyMeasure/MeasureValue': ['HorAcc', 0],
            'HorizontalAccuracyMeasure/MeasureUnitCode': ['HorAccUnit', 0],
            'HorizontalCollectionMethodName': ['HorCollMeth', 0],
            'HorizontalCoordinateReferenceSystemDatumName': ['HorRef', 0],
            'VerticalMeasure/MeasureValue': ['Elev', 0],
            'VerticalMeasure/MeasureUnitCode': ['ElevUnit', 0],
            'VerticalAccuracyMeasure/MeasureValue': ['ElevAcc', 0],
            'VerticalAccuracyMeasure/MeasureUnitCode': ['ElevAccUnit', 0],
            'VerticalCollectionMethodName': ['ElevMeth', 0],
            'VerticalCoordinateReferenceSystemDatumName': ['ElevRef', 0],
            'StateCode': ['StateCode', 0],
            'CountyCode': ['CountyCode', 0],
            'AquiferName': ['Aquifer', 0],
            'FormationTypeText': ['FmType', 0],
            'AquiferTypeName': ['AquiferType', 0],
            'ConstructionDateText': ['ConstDate', 0],
            'WellDepthMeasure/MeasureValue': ['Depth', 0],
            'WellDepthMeasure/MeasureUnitCode': ['DepthUnit', 0],
            'WellHoleDepthMeasure/MeasureValue': ['HoleDepth', 0],
            'WellHoleDepthMeasure/MeasureUnitCode': ['HoleDUnit', 0]
        }

        if type == 'Stations':
            maps = stations
        elif type == 'Results':
            maps = results

        for csv_file in self._csvs_on_disk(folder, type):
            print 'processing {}'.format(csv_file)
            with open(csv_file, 'r') as f:
                data = csv.DictReader(f)
                for row in data:
                    for key in maps.keys():
                        length = len(row[key])
                        if maps[key][1] < length:
                            maps[key][1] = length

        return maps

    def seed(self, folder, types):
        """
            method to seed the database from files on disk
            expects a parent folder with two child folders
            named stations and chemistry.
            within those folders are the csv's to be imported
        """
        gdb_exists = os.path.exists(self.location)
        
        if not gdb_exists:
            print 'creating gdb'
            self._create_gdb()
            print 'creating gdb: done'

            print 'creating feature classes'
            self._create_feature_classes(types)
            print 'creating feature classes: done'
        else:
            if not ConsolePrompt().query_yes_no('gdb already exists. Seeed missing feature classes?'):
                raise SystemExit('stopping')
            else:
                print 'creating feature classes'
                self._create_feature_classes(types)
                print 'creating feature classes: done'
        
        for type in types:
            for csv_file in self._csvs_on_disk(folder, type):
                with open(csv_file, 'r') as f:
                    print 'processing {}'.format(csv_file)
                    self._insert_rows(csv.DictReader(f), type)
                    print 'processing {}: done'.format(csv_file)

    def update(self):
        """
            method to update database with queries to a url
        """
        response = self._query(self.chemistry_query_url)
        csv = self._read_response(response)

        self._insert_rows(csv, 'Results')

    def create_relationship(self):
        origin = location = os.path.join(self.location, 'Stations')
        desitination = location = os.path.join(self.location, 'Results')
        key = 'StationId'

        arcpy.CreateRelationshipClass_management(origin,
                                         desitination,
                                         'Stations_Have_Results',
                                         'COMPOSITE',
                                         'Results',
                                         'Stations',
                                         'FORWARD',
                                         'ONE_TO_MANY',
                                         'NONE',
                                         key,
                                         key)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='seed a geodatabse.')

    parser.add_argument('--update', action='store_true', help='update the gdb from a web service call')
    parser.add_argument('--seed', nargs='*', help='seed the gdb from csv\'s on disk')
    parser.add_argument('--length', action='store_true', help='get the max field sizes form files on disk')
    parser.add_argument('--relate', action='store_true', help='creates the releationship class between stations and results')

    args = parser.parse_args()

    try:

        if args.update:
            pass
        elif args.length:
            seeder = Seeder('C:\\temp', 'test.gdb')
            maps = seeder.get_field_lengths(
                'C:\\Projects\\GitHub\\ugs-chemistry\\scripts\\dbseeder\\data',
                'Stations')

            for key in maps.keys():
                print '{}'.format(maps[key])
        elif args.relate:
            seeder = Seeder('C:\\temp', 'test.gdb')
            seeder.create_relationship()
        else:
            if args.seed is None:
                args.seed = ['Stations', 'Results']

            seeder = Seeder('C:\\temp', 'test.gdb')
            seeder.seed(
                'C:\\Projects\\GitHub\\ugs-chemistry\\scripts\\dbseeder\\data',
                args.seed)

        print 'finished'
    except:
        raise
