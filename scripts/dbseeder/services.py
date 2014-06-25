"""service classes for performing specific tasks"""

import datetime
import requests
import sys
from dateutil.parser import parse
from pyproj import Proj, transform


class WebQuery(object):

    """the http query wrapper over requests for unit testing"""

    def results(self, url):
        r = requests.get(url)

        return r.text.splitlines()


class ConsolePrompt(object):

    def query_yes_no(self, question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is one of "yes" or "no".
        """
        valid = {"yes": True,   "y": True,  "ye": True,
                 "no": False,     "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = raw_input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")


class Project(object):

    input_system = Proj(init='epsg:4326')
    ouput_system = Proj(init='epsg:26912')

    def to_utm(self, x, y):
        return transform(
            self.input_system,
            self.ouput_system,
            x,
            y)


class Caster(object):

    """takes argis row input and casts it to the defined schema type"""
    @staticmethod
    def cast(destination_value, destination_field_type):
        if destination_value is None:
            return None

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
            elif destination_value == '':
                return None
            else:
                cast = parse

        try:
            value = cast(destination_value)
            return value
        except:
            return None

class Normalizer(object):
    """class for handling the normalization of fields"""
    def __init__(self):
        super(Normalizer, self).__init__()

    def normalize_unit(self, param, unit):
        """
        In the units field, make all mg/L and ug/L lowercase while preserving other uppercase letters
        Fill the ParamGroup field using the table

        """
        inorganics_major_metals = ['calcium', 'magnesium', 'potassium', 'sodium adsorption ratio [(na)/(sq root of 1/2 ca + mg)]', 'sodium adsorption ratio', 'sodium plus potassium', 'sodium, percent total cations', 'sodium']
        inorganics_major_nonmetals = []
        inorganics_minor_metals = []
        inorganics_minor_nonmetals = []
        nutrient = []

        if param in inorganics_major_metals and unit == 'ug/l':
            ResultValue = ResultValue * 0.001
            unit = 'mg/l'

        if param in inorganics_minor_metals and unit == 'mg/l':
            ResultValue = ResultValue * 1000
            unit = 'ug/l'

        if param in inorganics_major_nonmetals and unit == 'ug/l':
            ResultValue = ResultValue * 0.001
            unit = 'mg/l'

        if param in inorganics_minor_nonmetals and unit == 'mg/l':
            ResultValue = ResultValue * 1000
            unit = 'ug/l'

        if param in nutrient and unit == 'ug/l':
            ResultValue = ResultValue * 0.001
            unit = 'mg/l'

        if param == 'nitrate' and unit == 'mg/l as n':
            ResultValue = ResultValue * 4.426802887
            unit = 'mg/l'

        if param == 'nitrite' and unit == 'mg/l as n':
            ResultValue = ResultValue * 3.284535258
            unit = 'mg/l'

        if param == 'phosphate' and unit == 'mg/l as p':
            ResultValue = ResultValue * 3.131265779
            unit = 'mg/l'

        if param == 'bicarbonate as caco3' and unit == 'mg/l':
            ResultValue = ResultValue * 1.22
            param = 'Bicarbonate'

        if param == 'bicarbonate as caco3' and unit == 'mg/l as caco3':
            ResultValue = ResultValue * 1.22
            unit = 'mg/l'
            param = 'Bicarbonate'

        if param == 'bicarbonate' and unit == 'mg/l as caco3':
            ResultValue = ResultValue * 1.22
            unit = 'mg/l'

        if param == 'phosphate-phosphorus' and unit == 'mg/l as p':
            ResultValue = ResultValue * 3.131265779
            unit = 'mg/l'
            param = 'Phosphate'

        if param == 'phosphate-phosphorus' and unit == 'mg/l':
            ResultValue = ResultValue * 3.131265779
            param = 'Phosphate'

        if param == 'sulfate as s' and unit == 'mg/l':
            ResultValue = ResultValue * 0.333792756
            param = 'Sulfate'

        if param == 'nitrate-nitrogen' and unit == 'mg/l as n':
            ResultValue = ResultValue * 4.426802887
            unit = 'mg/l'
            param = 'Nitrate'

        if param == 'nitrate as n' and unit == 'mg/l as n':
            ResultValue = ResultValue * 4.426802887
            unit = 'mg/l'
            param = 'Nitrate'

        if param == 'nitrite as n' and unit == 'mg/l as n':
            ResultValue = ResultValue * 3.284535258
            unit = 'mg/l'
            param = 'Nitrite'

        if param == 'nitrate-nitrogen' and unit == 'mg/l':
            ResultValue = ResultValue * 4.426802887
            param = 'Nitrite'

        if param == 'nitrate as n' and unit == 'mg/l':
            ResultValue = ResultValue * 4.426802887
            param = 'Nitrate'

        if param == 'nitrite as n' and unit == 'mg/l':
            ResultValue = ResultValue * 3.284535258
            unit = 'mg/l'
            param = 'Nitrite'

        if param == 'inorganic nitrogen (nitrate and nitrite) as n' and unit == 'mg/l as n':
            ResultValue = ResultValue * 4.426802887
            unit = 'mg/l'
            param = 'Inorganic nitrogen (nitrate and nitrite) as no3'

        if param == 'inorganic nitrogen (nitrate and nitrite) as n' and unit == 'mg/l':
            ResultValue = ResultValue * 4.426802887
            unit = 'mg/l'
            param = 'Inorganic nitrogen (nitrate and nitrite) as no3'

        if param == 'phosphate-phosphorus as p' and unit == 'mg/l as p':
            ResultValue = ResultValue * 3.131265779
            param = 'Phosphate'

        if param == 'orthophosphate as p' and unit == 'mg/l as p':
            ResultValue = ResultValue * 3.131265779
            unit = 'mg/l'
            param = 'Phosphate'

        if param == 'phosphate-phosphorus as p' and unit == 'mg/l':
            ResultValue = ResultValue * 3.131265779
            param = 'Phosphate'

        if param == 'orthophosphate as p' and unit == 'mg/l':
            ResultValue = ResultValue * 3.131265779
            param = 'Phosphate'

        if param == 'orthophosphate' and unit == 'mg/l as p':
            ResultValue = ResultValue * 3.131265779
            unit = 'mg/l'
            param = 'Phosphate'

        if param == 'ammonia and ammonium' and unit == 'mg/l nh4':
            ResultValue = ResultValue * 1.05918619
            unit = 'mg/l'
            param = 'Ammonia'

        if param == 'ammonia-nitrogen as n' and unit == 'mg/l as n':
            ResultValue = ResultValue * 1.21587526
            unit = 'mg/l'
            param = 'Ammonia'

        if param == 'ammonia-nitrogen' and unit == 'mg/l as n':
            ResultValue = ResultValue * 1.21587526
            unit = 'mg/l'
            param = 'Ammonia'

        if param == 'ammonia-nitrogen as n' and unit == 'mg/l':
            ResultValue = ResultValue * 1.21587526
            param = 'Ammonia'

        if param == 'ammonia-nitrogen' and unit == 'mg/l':
            ResultValue = ResultValue * 1.21587526
            param = 'Ammonia'

        if param == 'ammonia' and unit == 'mg/l as n':
            ResultValue = ResultValue * 1.21587526
            unit = 'mg/l'

        if param == 'specific conductance' and unit == 'ms/cm':
            ResultValue = ResultValue * 1000
            unit = 'uS/cm'

        if param == 'specific conductance' and unit == 'umho/cm':
            unit = 'uS/cm'

        if param == 'calcium' and unit == 'ueq/l':
            ResultValue = ResultValue * 20.039
            unit = 'mg/l'

        if param == 'magnesium' and unit == 'ueq/l':
            ResultValue = ResultValue * 12.1525
            unit = 'mg/l'

        if param == 'potassium' and unit == 'ueq/l':
            ResultValue = ResultValue * 39.0983
            unit = 'mg/l'

        if param == 'sodium' and unit == 'ueq/l':
            ResultValue = ResultValue * 22.9897
            unit = 'mg/l'

        if param == 'nitrate' and unit == 'ueq/l':
            ResultValue = ResultValue * 62.0049
            unit = 'mg/l'

        if param == 'chloride' and unit == 'ueq/l':
            ResultValue = ResultValue * 35.453
            unit = 'mg/l'

        if param == 'hydroxide' and unit == 'ueq/l':
            ResultValue = ResultValue * 17.0073
            unit = 'mg/l'

        if param == 'sulfate' and unit == 'ueq/l':
            ResultValue = ResultValue * 24.01565
            unit = 'mg/l'
