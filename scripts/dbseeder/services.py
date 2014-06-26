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
        In the units field, make all mg/L and ug/L lowercase while preserving
         other uppercase letters
        convert units
        normalize chemical

        """
        inorganics_major_metals = [
            'calcium', 'dissolved calcium', 'dissolved magnesium', 
            'dissolved potassium', 'dissolved sodium', 'magnesium', 
            'potassium', 'sodium', 'sodium adsorption ratio', 
            'sodium adsorption ratio [(na)/(sq root of 1/2 ca + mg)]', 
            'sodium plus potassium', 'sodium, percent total cations', 
            'total calcium', 'total magnesium', 'total potassium', 
            'total sodium', 'percent sodium', 'hypochlorite ion']
        inorganics_major_nonmetals = [
            'acidity as caco3', 'alkalinity', 
            'alkalinity, bicarbonate as caco3', 'alkalinity, carbonate as caco3', 
            'alkalinity, hydroxide as caco3', 
            'alkalinity, phenolphthalein (total hydroxide+1/2 carbonate)', 
            'alkalinity, total', 'alkalinity, total as caco3', 'bicarbonate', 
            'bicarbonate as caco3', 'bicarbonate as hco3', 'bromide', 
            'carbon dioxide', 'carbonate', 'carbonate (co3)', 'carbonate as caco3', 
            'carbonate as co3', 'chloride', 'chlorine', 'dissolved oxygen (do)', 
            'dissolved oxygen (field)', 'dissolved oxygen saturation', 'fluoride', 
            'fluorine', 'gran acid neutralizing capacity', 'hydrogen', 'hydrogen ion', 
            'hydroxide', 'inorganic carbon', 'oxygen', 'silica', 'silicon', 'sulfate', 
            'sulfide', 'sulfur', 'total alkalinity as caco3', 'total carbon', 
            'silica d/sio2', 't. alk/caco3', 'alkalinity as cac03', 'silica, dis. si02', 
            'carbon, total', 'chlorine dioxide', 'chlorite', 'residual chlorine', 
            'hydroxide as calcium carbonate', 'hydrogen sulfide', 'alkalinity, caco3 stability', 
            'acidity, total (caco3)', 'acidity, m.o. (caco3)', 'alkalinity, bicarbonate', 
            'alkalinity, carbonate', 'alkalinity, phenolphthalein', 'total chlorine', 
            'combined chlorine', 'perchlorate', 'free residual chlorine']
        inorganics_minor_nonmetals = [
            'antimony', 'argon', 'arsenate (aso43-)', 'arsenic', 'arsenite', 'boron', 
            'bromine', 'cyanide', 'cyanides amenable to chlorination (hcn & cn)', 
            'dissolved arsenic', 'dissolved boron', 'dissolved selenium', 'germanium', 
            'helium', 'iodide', 'krypton', 'neon', 'perchlorate', 'selenium', 
            'sulfur hexafluoride', 'tellurium', 'total arsenic', 'total boron', 
            'total selenium', 'xenon', 'chlorate', 'antimony, total', 'boron, total', 
            'asbestos']
        inorganics_minor_metals = [
            'aluminum', 'barium', 'beryllium', 'bismuth', 'cadmium', 'cerium', 
            'cesium', 'chromium', 'chromium(iii)', 'chromium(vi)', 'cobalt', 
            'copper', 'dissolved aluminum', 'dissolved barium', 
            'dissolved cadmium', 'dissolved chromium', 'dissolved copper', 
            'dissolved iron', 'dissolved lead', 'dissolved manganese', 
            'dissolved mercury', 'dissolved molybdenum', 'dissolved nickel', 
            'dissolved zinc', 'dysprosium', 'erbium', 'europium', 'gadolinium', 
            'gallium', 'holmium', 'iron', 'iron, ion (fe2+)', 'lanthanum', 'lead', 
            'lithium', 'lutetium', 'manganese', 'mercury', 'molybdenum', 
            'neodymium', 'nickel', 'niobium', 'praseodymium', 'rhenium', 'rubidium', 
            'samarium', 'scandium', 'silver', 'strontium', 
            'terbium', 'thallium', 'thulium', 'tin', 'titanium', 'total aluminum', 
            'total barium', 'total cadmium', 'total chromium', 'total copper', 
            'total iron', 'total iron-d max, dmr', 'total lead', 'total manganese', 
            'total mercury', 'total molybdenum', 'total nickel', 'total zinc', 
            'tungsten', 'vanadium', 'ytterbium', 'yttrium', 'zinc', 'zirconium', 
            'iron, dissolved', 'chromium, hex, as cr', 'copper, free', 
            'iron, suspended', 'manganese, suspended', 'beryllium, total', 
            'bismuth, total', 'chromium, hex', 'cobalt, total', 'lithium, total', 
            'molybdenum, total', 'thallium, total', 'tin, total', 'titanium, total', 
            'vanadium, total', 'lead summary', 'copper summary', 'manganese, dissolved']
        nutrient = [
            'ammonia', 'ammonia and ammonium', 'ammonia as n', 'ammonia as nh3', 
            'ammonia-nitrogen', 'ammonia-nitrogen as n', 'ammonium', 'ammonium as n', 
            'dissolved nitrate: no3', 'dissolved nitrite: no2', 
            'inorganic nitrogen (nitrate and nitrite)', 
            'inorganic nitrogen (nitrate and nitrite) as n', 'kjeldahl nitrogen', 
            'nitrate', 'nitrate as n', 'nitrate-nitrogen', 'nitrite', 'nitrite as n', 
            'nitrogen', 'nitrogen, ammonium/ammonia ratio', 
            'nitrogen, mixed forms (nh3), (nh4), organic, (no2) and (no3)', 
            'no2+no3 as n', 'organic nitrogen', 'ortho. phosphate', 'orthophosphate', 
            'orthophosphate as p', 'phosphate', 'phosphate-phosphorus', 'phosphate-phosphorus as p', 
            'phosphate-phosphorus as po4', 'phosphorus', 'total phosphorus', 'nitrate + nitrite as n', 
            'phosphate, tot. dig. (as p)', 't.k.n.', 'phosphorus 0 as p', 'nitrogen-ammonia as (n)', 
            'total kjeldahl nitrogen (in water mg/l)', 'nitrate-nitrite', 'phosphate, total', 
            'phosphorus, soluble', 'phosphate, reactive', 'phosphorus, total']


        original_chemical = chemical
        chemical = chemical.lower()
        milli_per_liter = 'mg/l'

        if chemical in inorganics_major_metals and unit == 'ug/l':
            return self.calculate_amount(current_amount, 0.001), milli_per_liter, original_chemical
        elif chemical in inorganics_minor_metals and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 1000), 'ug/l', original_chemical
        elif chemical in inorganics_major_nonmetals and unit == 'ug/l':
            return self.calculate_amount(current_amount, 0.001), milli_per_liter, original_chemical
        elif chemical in inorganics_minor_nonmetals and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 1000), 'ug/l', original_chemical
        elif chemical in nutrient and unit == 'ug/l':
            return self.calculate_amount(current_amount, 0.001), milli_per_liter, original_chemical
        elif chemical == 'nitrate' and unit == 'mg/l as n':
            return self.calculate_amount(current_amount, 4.426802887), milli_per_liter, original_chemical
        elif chemical == 'nitrite' and unit == 'mg/l as n':
            return self.calculate_amount(current_amount, 3.284535258), milli_per_liter, original_chemical
        elif chemical == 'phosphate' and unit == 'mg/l as p':
            return self.calculate_amount(current_amount, 3.131265779), milli_per_liter, original_chemical
        elif chemical == 'bicarbonate as caco3' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 1.22), milli_per_liter, 'Bicarbonate'
        elif chemical == 'carbonate as caco3' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 0.60), milli_per_liter, 'Carbonate'
        elif chemical == 'alkalinity, bicarbonate as caco3' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 1.22), milli_per_liter, 'Bicarbonate'
        elif chemical == 'bicarbonate as caco3' and unit == 'mg/l as caco3':
            return self.calculate_amount(current_amount, 1.22), milli_per_liter, 'Bicarbonate'
        elif chemical == 'alkalinity, carbonate' and unit == 'mg/l as caco3':
            return self.calculate_amount(current_amount, 0.60), milli_per_liter, 'Carbonate'        
        elif chemical == 'carbonate as co3' and unit == milli_per_liter:
            return current_amount, unit, 'Carbonate'
        elif chemical == 'carbonate (co3)' and unit == milli_per_liter:
            return current_amount, unit, 'Carbonate'
        elif chemical == 'bicarbonate as hco3' and unit == milli_per_liter:
            return current_amount, unit, 'Bicarbonate'
        elif chemical == 'alkalinity, carbonate as caco3' and unit == 'mg/l as caco3':
            return self.calculate_amount(current_amount, 0.60), milli_per_liter, 'Carbonate based on alkalinity'        
        elif chemical == 'alkalinity, bicarbonate' and unit == 'mg/l as caco3':
            return self.calculate_amount(current_amount, 1.22), milli_per_liter, 'Bicarbonate based on alkalinity'
        elif chemical == 'alkalinity' and unit == 'mg/l as caco3':
            return self.calculate_amount(current_amount, 1.22), milli_per_liter, 'Bicarbonate based on alkalinity'
        elif chemical == 't.alk/caco3' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 1.22), milli_per_liter, 'Bicarbonate based on alkalinity'        
        elif chemical == 'total alkalinity as caco3' and unit == 'mg/l':
            return self.calculate_amount(current_amount, 1.22), milli_per_liter, 'Bicarbonate based on alkalinity'
        elif chemical == 'bicarbonate' and unit == 'mg/l as caco3':
            return self.calculate_amount(current_amount, 1.22), milli_per_liter, original_chemical
        elif chemical == 'phosphate-phosphorus' and unit == 'mg/l as p':
            return self.calculate_amount(current_amount, 3.131265779), milli_per_liter, 'Phosphate'
        elif chemical == 'phosphate-phosphorus' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 3.131265779), milli_per_liter, 'Phosphate'
        elif chemical == 'sulfate as s' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 0.333792756), milli_per_liter, 'Sulfate'
        elif chemical == 'nitrate-nitrogen' and unit == 'mg/l as n':
            return self.calculate_amount(current_amount, 4.426802887), milli_per_liter, 'Nitrate'
        elif chemical == 'nitrate as n' and unit == 'mg/l as n':
            return self.calculate_amount(current_amount, 4.426802887), milli_per_liter, 'Nitrate'
        elif chemical == 'nitrite as n' and unit == 'mg/l as n':
            return self.calculate_amount(current_amount, 3.284535258), milli_per_liter, 'Nitrite'
        elif chemical == 'nitrate-nitrogen' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 4.426802887), milli_per_liter, 'Nitrite'
        elif chemical == 'nitrate as n' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 4.426802887), milli_per_liter, 'Nitrate'
        elif chemical == 'nitrite as n' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 3.284535258), milli_per_liter, 'Nitrite'
        elif (chemical == 'nitrate-nitrite' or chemical == 'inorganic nitrogen (nitrate and nitrite) as n' or chemical == 'nitrate + nitrate as n' or chemical == 'no2+no3 as n') and (unit == 'mg/l as n' or unit == milli_per):
            return self.calculate_amount(current_amount, 4.426802887), milli_per_liter, 'Nitrate and nitrite as no3'
        elif chemical == 'phosphate-phosphorus as p' and unit == 'mg/l as p':
            return self.calculate_amount(current_amount, 3.131265779), milli_per_liter, 'Phosphate'
        elif chemical == 'orthophosphate as p' and unit == 'mg/l as p':
            return self.calculate_amount(current_amount, 3.131265779), milli_per_liter, 'Phosphate'
        elif chemical == 'phosphate-phosphorus as p' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 3.131265779), milli_per_liter, 'Phosphate'
        elif chemical == 'orthophosphate as p' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 3.131265779), milli_per_liter, 'Phosphate'
        elif chemical == 'orthophosphate' and unit == 'mg/l as p':
            return self.calculate_amount(current_amount, 3.131265779), milli_per_liter, 'Phosphate'
        elif chemical == 'ammonia and ammonium' and unit == 'mg/l nh4':
            return self.calculate_amount(current_amount, 1.05918619), milli_per_liter, 'Ammonia'
        elif chemical == 'ammonia-nitrogen as n' and unit == 'mg/l as n':
            return self.calculate_amount(current_amount, 1.21587526), milli_per_liter, 'Ammonia'
        elif chemical == 'ammonia-nitrogen' and unit == 'mg/l as n':
            return self.calculate_amount(current_amount, 1.21587526), milli_per_liter, 'Ammonia'
        elif chemical == 'ammonia-nitrogen as n' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 1.21587526), milli_per_liter, 'Ammonia'
        elif chemical == 'ammonia-nitrogen' and unit == milli_per_liter:
            return self.calculate_amount(current_amount, 1.21587526), milli_per_liter, 'Ammonia'
        elif chemical == 'ammonia' and unit == 'mg/l as n':
            return self.calculate_amount(current_amount, 1.21587526), milli_per_liter, original_chemical
        elif chemical == 'specific conductance' and unit == 'ms/cm':
            return self.calculate_amount(current_amount, 1000), 'uS/cm', original_chemical
        elif chemical == 'specific conductance' and unit == 'umho/cm':
            return current_amount, 'uS/cm', original_chemical
        elif chemical == 'calcium' and unit == 'ueq/l':
            return self.calculate_amount(current_amount, 20.039), milli_per_liter, original_chemical
        elif chemical == 'magnesium' and unit == 'ueq/l':
            return self.calculate_amount(current_amount, 12.1525), milli_per_liter, original_chemical
        elif chemical == 'potassium' and unit == 'ueq/l':
            return self.calculate_amount(current_amount, 39.0983), milli_per_liter, original_chemical
        elif chemical == 'sodium' and unit == 'ueq/l':
            return self.calculate_amount(current_amount, 22.9897), milli_per_liter, original_chemical
        elif chemical == 'nitrate' and unit == 'ueq/l':
            return self.calculate_amount(current_amount, 62.0049), milli_per_liter, original_chemical
        elif chemical == 'chloride' and unit == 'ueq/l':
            return self.calculate_amount(current_amount, 35.453), milli_per_liter, original_chemical
        elif chemical == 'hydroxide' and unit == 'ueq/l':
            return self.calculate_amount(current_amount, 17.0073), milli_per_liter, original_chemical
        elif chemical == 'sulfate' and unit == 'ueq/l':
            return self.calculate_amount(current_amount, 24.01565), milli_per_liter, original_chemical
        else:
            return current_amount, unit, original_chemical

    def calculate_amount(self, amount, conversion_rate):
        if amount is None:
            return None
        elif not amount:
            return 0

        return amount * conversion_rate
