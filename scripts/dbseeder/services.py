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

    def normalize_unit(self, chemical, unit, current_amount):
        """
        In the units field, make all mg/L and ug/L lowercase while preserving other uppercase letters
        convert units

        """
        inorganics_major_metals = ['Calcium', 'Magnesium', 'Potassium', 'Sodium adsorption ratio [(Na)/(sq root of 1/2 Ca + Mg)]', 'Sodium adsorption ratio', 'Sodium plus potassium', 'Sodium, percent total cations', 'Sodium']
        inorganics_major_nonmetals = ['Alkalinity, Bicarbonate as CaCO3', 'Alkalinity, Carbonate as CaCO3', 'Alkalinity, Hydroxide as CaCO3', 'Alkalinity, Phenolphthalein (total hydroxide+1/2 carbonate)', 'Alkalinity, total as CaCO3', 'Alkalinity, total', 'Alkalinity', 'Bicarbonate', 'Bromide', 'Carbon dioxide', 'Carbonate (CO3)', 'Carbonate', 'Chloride', 'Chlorine', 'Dissolved oxygen (DO)', 'Dissolved oxygen saturation', 'Fluoride', 'Fluorine', 'Hydrogen ion', 'Hydrogen', 'Hydroxide', 'Inorganic carbon', 'Oxygen', 'Silica', 'Silicon', 'Sulfate', 'Sulfide', 'Sulfur', 'Total Carbon']
        inorganics_minor_metals = ['Aluminum', 'Barium', 'Beryllium', 'Bismuth', 'Cadmium', 'Cerium', 'Cesium', 'Chromium(III)', 'Chromium(VI)', 'Chromium', 'Cobalt', 'Copper', 'Dysprosium', 'Erbium', 'Europium', 'Gadolinium', 'Gallium', 'Holmium', 'Iron, ion (Fe2+)', 'Iron', 'Lanthanum', 'Lead', 'Lithium', 'Lutetium', 'Manganese', 'Mercury', 'Molybdenum', 'Neodymium', 'Nickel', 'Niobium', 'Praseodymium', 'Rhenium', 'Rubidium', 'Samarium', 'Scandium', 'Silver', 'Strontium', 'Sulfate as S', 'Sulfate as SO4', 'Terbium', 'Thallium', 'Thulium', 'Tin', 'Titanium', 'Tungsten', 'Vanadium', 'Ytterbium', 'Yttrium', 'Zinc', 'Zirconium']
        inorganics_minor_nonmetals = ['Antimony', 'Argon', 'Arsenate (AsO43-)', 'Arsenic', 'Arsenite', 'Boron', 'Bromine', 'Cyanide', 'Cyanides amenable to chlorination (HCN & CN)', 'Germanium', 'Helium', 'Iodide', 'Krypton', 'Neon', 'Perchlorate', 'Selenium', 'Sulfur hexafluoride', 'Tellurium', 'Xenon']
        nutrient = ['Ammonia and ammonium', 'Ammonia as NH3', 'Ammonia', 'Ammonia-nitrogen as N', 'Ammonia-nitrogen', 'Ammonium as N', 'Ammonium', 'Inorganic nitrogen (nitrate and nitrite) as N', 'Inorganic nitrogen (nitrate and nitrite)', 'Kjeldahl nitrogen', 'Nitrate as N', 'Nitrate', 'Nitrate-Nitrogen', 'Nitrite as N', 'Nitrite', 'Nitrogen, ammonium/ammonia ratio', 'Nitrogen, mixed forms (NH3), (NH4), organic, (NO2) and (NO3)', 'Nitrogen', 'Organic nitrogen', 'Orthophosphate as P', 'Orthophosphate', 'Phosphate', 'Phosphate-phosphorus as P', 'Phosphate-phosphorus as PO4', 'Phosphate-phosphorus', 'Phosphorus']

        if chemical in inorganics_major_metals and unit == 'ug/l':
            return current_amount * 0.001, milli_per_liter
        elif chemical in inorganics_minor_metals and unit == milli_per_liter:
            return current_amount * 1000, 'ug/l'
        elif chemical in inorganics_major_nonmetals and unit == 'ug/l':
            return current_amount * 0.001, milli_per_liter
        elif chemical in inorganics_minor_nonmetals and unit == milli_per_liter:
            return current_amount * 1000, 'ug/l'
        elif chemical in nutrient and unit == 'ug/l':
            return current_amount * 0.001, milli_per_liter
        elif chemical == 'nitrate' and unit == 'mg/l as n':
            return current_amount * 4.426802887, milli_per_liter
        elif chemical == 'nitrite' and unit == 'mg/l as n':
            return current_amount * 3.284535258, milli_per_liter
        elif chemical == 'phosphate' and unit == 'mg/l as p':
            return current_amount * 3.131265779, milli_per_liter
        elif chemical == 'bicarbonate as caco3' and unit == milli_per_liter:
            return current_amount * 1.22, 'Bicarbonate'
        elif chemical == 'bicarbonate as caco3' and unit == 'mg/l as caco3':
            return current_amount * 1.22, milli_per_liter
            chemical = 'Bicarbonate'
        elif chemical == 'bicarbonate' and unit == 'mg/l as caco3':
            return current_amount * 1.22, milli_per_liter
        elif chemical == 'phosphate-phosphorus' and unit == 'mg/l as p':
            return current_amount * 3.131265779, milli_per_liter
            chemical = 'Phosphate'
        elif chemical == 'phosphate-phosphorus' and unit == milli_per_liter:
            return current_amount * 3.131265779, 'Phosphate'
        elif chemical == 'sulfate as s' and unit == milli_per_liter:
            return current_amount * 0.333792756, 'Sulfate'
        elif chemical == 'nitrate-nitrogen' and unit == 'mg/l as n':
            return current_amount * 4.426802887, milli_per_liter
            chemical = 'Nitrate'
        elif chemical == 'nitrate as n' and unit == 'mg/l as n':
            return current_amount * 4.426802887, milli_per_liter
            chemical = 'Nitrate'
        elif chemical == 'nitrite as n' and unit == 'mg/l as n':
            return current_amount * 3.284535258, milli_per_liter
            chemical = 'Nitrite'
        elif chemical == 'nitrate-nitrogen' and unit == milli_per_liter:
            return current_amount * 4.426802887, 'Nitrite'
        elif chemical == 'nitrate as n' and unit == milli_per_liter:
            return current_amount * 4.426802887, 'Nitrate'
        elif chemical == 'nitrite as n' and unit == milli_per_liter:
            return current_amount * 3.284535258, milli_per_liter
            chemical = 'Nitrite'
        elif chemical == 'inorganic nitrogen (nitrate and nitrite) as n' and unit == 'mg/l as n':
            return current_amount * 4.426802887, milli_per_liter
            chemical = 'Inorganic nitrogen (nitrate and nitrite) as no3'
        elif chemical == 'inorganic nitrogen (nitrate and nitrite) as n' and unit == milli_per_liter:
            return current_amount * 4.426802887, milli_per_liter
            chemical = 'Inorganic nitrogen (nitrate and nitrite) as no3'
        elif chemical == 'phosphate-phosphorus as p' and unit == 'mg/l as p':
            return current_amount * 3.131265779, 'Phosphate'
        elif chemical == 'orthophosphate as p' and unit == 'mg/l as p':
            return current_amount * 3.131265779, milli_per_liter
            chemical = 'Phosphate'
        elif chemical == 'phosphate-phosphorus as p' and unit == milli_per_liter:
            return current_amount * 3.131265779, 'Phosphate'
        elif chemical == 'orthophosphate as p' and unit == milli_per_liter:
            return current_amount * 3.131265779, 'Phosphate'
        elif chemical == 'orthophosphate' and unit == 'mg/l as p':
            return current_amount * 3.131265779, milli_per_liter
            chemical = 'Phosphate'
        elif chemical == 'ammonia and ammonium' and unit == 'mg/l nh4':
            return current_amount * 1.05918619, milli_per_liter
            chemical = 'Ammonia'
        elif chemical == 'ammonia-nitrogen as n' and unit == 'mg/l as n':
            return current_amount * 1.21587526, milli_per_liter
            chemical = 'Ammonia'
        elif chemical == 'ammonia-nitrogen' and unit == 'mg/l as n':
            return current_amount * 1.21587526, milli_per_liter
            chemical = 'Ammonia'
        elif chemical == 'ammonia-nitrogen as n' and unit == milli_per_liter:
            return current_amount * 1.21587526, 'Ammonia'
        elif chemical == 'ammonia-nitrogen' and unit == milli_per_liter:
            return current_amount * 1.21587526, 'Ammonia'
        elif chemical == 'ammonia' and unit == 'mg/l as n':
            return current_amount * 1.21587526, milli_per_liter
        elif chemical == 'specific conductance' and unit == 'ms/cm':
            return current_amount * 1000, 'uS/cm'
        elif chemical == 'specific conductance' and unit == 'umho/cm':
            converted_unit = 'uS/cm'
        elif chemical == 'calcium' and unit == 'ueq/l':
            return current_amount * 20.039, milli_per_liter
        elif chemical == 'magnesium' and unit == 'ueq/l':
            return current_amount * 12.1525, milli_per_liter
        elif chemical == 'potassium' and unit == 'ueq/l':
            return current_amount * 39.0983, milli_per_liter
        elif chemical == 'sodium' and unit == 'ueq/l':
            return current_amount * 22.9897, milli_per_liter
        elif chemical == 'nitrate' and unit == 'ueq/l':
            return current_amount * 62.0049, milli_per_liter
        elif chemical == 'chloride' and unit == 'ueq/l':
            return current_amount * 35.453, milli_per_liter
        elif chemical == 'hydroxide' and unit == 'ueq/l':
            return current_amount * 17.0073, milli_per_liter
        elif chemical == 'sulfate' and unit == 'ueq/l':
            return current_amount * 24.01565, milli_per_liter
        else:
            return current_amount, unit
