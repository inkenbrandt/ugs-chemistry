"""DbSeeder creates and seeds esri file geodatabases"""

import arcpy
import argparse
import os
from models import TableInfo
from programs import Wqp, Sdwis
from services import ConsolePrompt


class Seeder(object):
    parent_folder = None
    gdb_name = None
    location = None
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

    def create_relationship(self):
        origin = os.path.join(self.location, 'Stations')
        desitination = os.path.join(self.location, 'Results')
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

    def update(self):
        pass

    def field_lengths(self):
        pass

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

        wqp = Wqp(self.location, arcpy.da.InsertCursor)
        wqp.seed(folder, types)

        sdwis = Sdwis(self.location, arcpy.da.InsertCursor)
        sdwis.seed(types)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='seed a geodatabse.')

    parser.add_argument(
        '--update', action='store_true', help='update the gdb from a web service call')
    parser.add_argument(
        '--seed', nargs='*', help='seed the gdb from csv\'s on disk')
    parser.add_argument('--length', action='store_true',
                        help='get the max field sizes form files on disk')
    parser.add_argument('--relate', action='store_true',
                        help='creates the releationship class between stations and results')

    args = parser.parse_args()

    try:

        if args.update:
            pass
        elif args.length:
            seeder = Seeder('C:\\temp', 'test.gdb')
            maps = seeder.field_lengths(
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
