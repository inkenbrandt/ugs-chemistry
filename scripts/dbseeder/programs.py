import ConfigParser
import csv
import cx_Oracle
import glob
import os
from models import Results, Stations, SdwisResults, SdwisStations, Schema
from services import Project, WebQuery


class Program(object):

    def __init__(self, location, InsertCursor):
        self.location = location
        self.InsertCursor = InsertCursor

    def _get_fields(self, schema_map):
        return [schema_map[item]['destination'] for item in schema_map]


class Wqp(Program):

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

        with self.InsertCursor(location, fields) as curser:
            for row in data:
                etl = Type(row)
                insert_row = etl.row

                if feature_class == 'Stations':
                    lon = row[etl.schema_map['Lon_X']]
                    lat = row[etl.schema_map['Lat_Y']]

                    try:
                        x, y = Project().to_utm(lon, lat)
                        insert_row.append((x, y))
                    except Exception as detail:
                        print 'Handling projection error:', detail

                        insert_row.append(None)

                curser.insertRow(insert_row)

    def _csvs_on_disk(self, parent_folder, type):
        folder = os.path.join(parent_folder, type, '*.csv')
        for file in glob.glob(folder):
            yield file

    def _query(self, url):
        data = WebQuery().results(url)

        return data

    def _read_response(self, data):
        reader = csv.DictReader(data, delimiter=',')

        return reader

    def _build_field_length_structure(self, schema):
        """turns the schema doc into a structure that can count fields lengths
            dict[source column] = array[destination column, count]
        """
        results = {}

        for column in schema:
            if column['source'] is None and (
                    column['type'].lower() != 'text' or
                    column['type'].lower() != 'string'):
                continue

            results[column['source']] = [column['destination'], 0]

        return results

    def field_lengths(self, folder, type):
        schema = Schema()

        if type == 'Stations':
            maps = self._build_field_length_structure(schema.station)
        elif type == 'Results':
            maps = self._build_field_length_structure(schema.result)

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
        for type in types:
            for csv_file in self._csvs_on_disk(folder, type):
                with open(csv_file, 'r') as f:
                    print 'processing {}'.format(csv_file)
                    self._insert_rows(csv.DictReader(f), type)
                    print 'processing {}: done'.format(csv_file)

    def update(self, types):
        for type in types:
            response = self._query(type)
            csv = self._read_response(response)

            self._insert_rows(csv, type)


class Sdwis(Program):

    _result_query = """SELECT
        UTV80.TSASAR.ANALYSIS_START_DT AS "AnalysisDate",
        UTV80.TSALAB.LAB_ID_NUMBER AS "LabName",
        UTV80.TSASAR.DETECTN_LIMIT_NUM AS "MDL",
        UTV80.TSASAR.DETECTN_LIM_UOM_CD AS "MDLUnit",
        UTV80.TINWSYS.TINWSYS_IS_NUMBER AS "OrgId",
        UTV80.TINWSYS.NAME AS "OrgName",
        UTV80.TSAANLYT.NAME AS "Param",
        UTV80.TSASAR.CONCENTRATION_MSR AS "ResultValue",
        UTV80.TSASAMPL.COLLLECTION_END_DT AS "SampleDate",
        UTV80.TSASAMPL.COLLCTN_END_TIME AS "SampleTime",
        UTV80.TSASAMPL.LAB_ASGND_ID_NUM AS "SampleId",
        UTV80.TINWSF.TYPE_CODE AS "SampType",
        UTV80.TINWSF.TINWSF_IS_NUMBER AS "StationId",
        UTV80.TSASAR.UOM_CODE AS "Unit",
        UTV80.TINLOC.LATITUDE_MEASURE AS "Lat_Y",
        UTV80.TINLOC.LONGITUDE_MEASURE AS "Lon_X",
        UTV80.TSAANLYT.CAS_REGISTRY_NUM AS "CAS_Reg",
        UTV80.TSASAR.TSASAR_IS_NUMBER AS "Id_Num"

        FROM UTV80.TINWSF
        JOIN UTV80.TINWSYS ON
        UTV80.TINWSF.TINWSYS_IS_NUMBER = UTV80.TINWSYS.TINWSYS_IS_NUMBER
        JOIN UTV80.TINLOC ON
        UTV80.TINWSF.TINWSF_IS_NUMBER = UTV80.TINLOC.TINWSF_IS_NUMBER
        JOIN UTV80.TSASMPPT ON
        UTV80.TINWSF.TINWSF_IS_NUMBER = UTV80.TSASMPPT.TINWSF0IS_NUMBER
        JOIN UTV80.TSASAMPL ON
        UTV80.TSASMPPT.TSASMPPT_IS_NUMBER = UTV80.TSASAMPL.TSASMPPT_IS_NUMBER
        JOIN UTV80.TSASAR ON
        UTV80.TSASAMPL.TSASAMPL_IS_NUMBER = UTV80.TSASAR.TSASAMPL_IS_NUMBER
        JOIN UTV80.TSAANLYT ON
        UTV80.TSASAR.TSAANLYT_IS_NUMBER = UTV80.TSAANLYT.TSAANLYT_IS_NUMBER
        JOIN UTV80.TSALAB ON
        UTV80.TSASAMPL.TSALAB_IS_NUMBER = UTV80.TSALAB.TSALAB_IS_NUMBER

        WHERE (UTV80.TINWSF.TYPE_CODE = 'SP' Or
                UTV80.TINWSF.TYPE_CODE = 'WL') AND
                UTV80.TSASAR.CONCENTRATION_MSR IS NOT NULL

        ORDER BY UTV80.TINWSF.ST_ASGN_IDENT_CD"""

    _station_query = """SELECT
        UTV80.TINWSYS.TINWSYS_IS_NUMBER AS "OrgId",
        UTV80.TINWSYS.NAME AS "OrgName",
        UTV80.TINWSF.TINWSF_IS_NUMBER AS "StationId",
        UTV80.TINWSF.NAME AS "StationName",
        UTV80.TINWSF.TYPE_CODE AS "StationType",
        UTV80.TINLOC.LATITUDE_MEASURE AS "Lat_Y",
        UTV80.TINLOC.LONGITUDE_MEASURE AS "Lon_X",
        UTV80.TINLOC.HORIZ_ACCURACY_MSR AS "HorAcc",
        UTV80.TINLOC.HZ_COLLECT_METH_CD AS "HorCollMeth",
        UTV80.TINLOC.HORIZ_REF_DATUM_CD AS "HorRef",
        UTV80.TINLOC.VERTICAL_MEASURE AS "Elev",
        UTV80.TINLOC.VERT_ACCURACY_MSR AS "ElevAcc",
        UTV80.TINLOC.VER_COL_METH_CD AS "ElevMeth",
        UTV80.TINLOC.VERT_REF_DATUM_CD AS "ElevRef",
        MAX(UTV80.TINWLCAS.BOTTOM_DEPTH_MSR) AS "Depth",
        UTV80.TINWLCAS.BOTTOM_DP_MSR_UOM AS "DepthUnit"

        FROM UTV80.TINWSF
        JOIN UTV80.TINWSYS ON
            UTV80.TINWSF.TINWSYS_IS_NUMBER = UTV80.TINWSYS.TINWSYS_IS_NUMBER
        JOIN UTV80.TINLOC ON
            UTV80.TINWSF.TINWSF_IS_NUMBER = UTV80.TINLOC.TINWSF_IS_NUMBER
        LEFT JOIN UTV80.TINWLCAS ON
            UTV80.TINWSF.TINWSF_IS_NUMBER = UTV80.TINWLCAS.TINWSF_IS_NUMBER

        WHERE (UTV80.TINWSF.TYPE_CODE = 'SP' OR
            UTV80.TINWSF.TYPE_CODE = 'WL') AND
            UTV80.TINLOC.LATITUDE_MEASURE != 0
        GROUP BY UTV80.TINWSF.TINWSF_IS_NUMBER,
                UTV80.TINWSF.NAME,
                UTV80.TINWSF.TYPE_CODE,
                UTV80.TINWSYS.TINWSYS_IS_NUMBER,
                UTV80.TINWSYS.NAME,
                UTV80.TINLOC.LATITUDE_MEASURE,
                UTV80.TINLOC.LONGITUDE_MEASURE,
                UTV80.TINLOC.SRC_MAP_SCALE_NUM,
                UTV80.TINLOC.HORIZ_ACCURACY_MSR,
                UTV80.TINLOC.HZ_COLLECT_METH_CD,
                UTV80.TINLOC.HORIZ_REF_DATUM_CD,
                UTV80.TINLOC.VERTICAL_MEASURE,
                UTV80.TINLOC.VERT_ACCURACY_MSR,
                UTV80.TINLOC.VER_COL_METH_CD,
                UTV80.TINLOC.VERT_REF_DATUM_CD,
                UTV80.TINWLCAS.BOTTOM_DEPTH_MSR,
                UTV80.TINWLCAS.BOTTOM_DP_MSR_UOM"""

    def __init__(self, location, InsertCursor):
        super(Sdwis, self).__init__(location, InsertCursor)

        config = ConfigParser.RawConfigParser()

        file = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'secrets.cfg')

        config.read(file)

        user = config.get('sdwis', 'username')
        password = config.get('sdwis', 'password')
        server = config.get('sdwis', 'server')
        instance = config.get('sdwis', 'instance')

        self._connection_string = '{}/{}@{}/{}'.format(
            user, password, server, instance)

    def _query(self, query, count=None):
        print 'querying SDWIS database'

        conn = cx_Oracle.connect(self._connection_string)
        cursor = conn.cursor()

        results = cursor.execute(query)

        if count is not None:
            some = results.fetchmany(count)

            cursor.close()
            conn.close()

            return some

        return results

    def _insert_rows(self, data, feature_class):
        location = os.path.join(self.location, feature_class)

        print 'inserting into {} type {}'.format(location, feature_class)

        if feature_class == 'Results':
            Type = SdwisResults
        elif feature_class == 'Stations':
            Type = SdwisStations

        fields = self._get_fields(Type(None).schema_map)

        if feature_class == 'Stations':
            fields.append('SHAPE@XY')

        with self.InsertCursor(location, fields) as curser:
            for row in data:
                etl = Type(row)
                insert_row = etl.row

                if feature_class == 'Stations':
                    lat = row[etl.schema_map['Lat_Y']]
                    lon = row[etl.schema_map['Lon_X']]

                    try:
                        x, y = Project().to_utm(lon, lat)
                        insert_row.append((x, y))
                    except Exception as detail:
                        print 'Handling projection error:', detail

                        insert_row.append(None)

                curser.insertRow(insert_row)

    def seed(self, types):
        query_string = None

        for type in types:
            if type == 'Stations':
                query_string = self._station_query
            elif type == 'Results':
                query_string = self._result_query

            records = self._query(query_string)
            self._insert_rows(records, type)
