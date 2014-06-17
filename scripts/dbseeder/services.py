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
