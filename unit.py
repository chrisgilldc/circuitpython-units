####
# Unit Processor for CircuitPython
# 2022 - Christopher Gill
# https://github.com/chrisgilldc/circuitpython-units
####

# Helper class for unit conversion
from math import floor

# Import the constants.
import unit_conversions


class Unit:
    def __init__(self, first, second=None):

        # Check inputs and determine mode.
        # If only one parameter is passed and it's a string, send it to string parsing.
        if isinstance(first, str) and second is None:
            self._unit_string_parse(first)
        else:
            if first is None:
                raise ValueError("Value is required when creating a Unit")
            if type(first) not in (int, float):
                raise TypeError("Value type must be float or int")
            if second is None:
                raise ValueError("Unit is required when creating a Unit through parameters")
            # Get conversion table for this unit

            try:
                self.unit = second
            except:
                raise

            self._value = first

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value

    @property
    def unit_class(self):
        return self._unit_class

    @unit.setter
    def unit(self, unit):
        """Set the unit of the object. Does *not* convert values.

        :param unit: The level of the message
        """
        found = False
        for unit_class in unit_conversions.CLASSES:
            if unit in getattr(unit_conversions, unit_class):
                found = True
                self._unit_class = unit_class
                break
        if not found:
            raise ValueError("Provided unit {} is not supported.".format(unit))
        self._unit = unit

    # When value is set, convert it.
    @value.setter
    def value(self, value):
        """Set the scalar value of the unit.

        :param value: The scalar value the unit. Must be an integer or float.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Unit value must be int or float, got {} input".format(type(value)))
        self._value = value

    # Method to convert and return a *new* Unit value.
    def convert(self, output_unit):
        # Check for issues.
        if output_unit not in getattr(unit_conversions, self._unit_class):
            raise ValueError("Requested output unit '{}' is not supported.".format(output_unit))

        try:
            conversion_factor = getattr(unit_conversions, self._unit_class)[self._unit][output_unit]
        except:
            raise ValueError("No conversion path from {} to {}".format(self._unit, output_unit))

        self_in_target = self.value / conversion_factor
        return Unit(self_in_target, output_unit)

    # Method to convert and make the new values this object's *new* values.
    def convert_inplace(self,output_unit):
        try:
            new_obj = self.convert(output_unit)
        except:
            raise
        # If successful, merge in the unit.
        self._unit = new_obj._unit
        self._value = new_obj._value

    def asftin(self,format='iso',include_zero=True):
        # If no format provided, return 'ISO' format, ie: 'X ft Y in'
        if format not in ('iso','prime'):
            format = 'iso'
        # This must be a distance class.
        if self._unit_class != "DISTANCE":
            raise TypeError("Cannot return feet and inches for non-distance unit!")
        # If not inches, convert to inches.
        if self.unit != "in":
            working_value = self.convert("in").value
        else:
            working_value = self.value

        working_value = self.value
        # Find out how many feet there are
        working_value_feet = int(working_value // 12)
        working_value_inches = floor(working_value % 12)

        # Now we can stringify it.
        if format == 'prime':
            ftin_string = str(working_value_feet) + "'"
            if include_zero:
                ftin_string = ftin_string + str(working_value_inches) + '"'
        else:
            ftin_string = str(working_value_feet) + " ft"
            if include_zero:
                ftin_string = ftin_string + " " + str(working_value_inches) + " in"
        return ftin_string

    # Parse a unit string out
    def _unit_string_parse(self, unit_string):
        # Try to split on whitespace.
        elements = unit_string.split()
        if len(elements) == 2:
            # If there's two elements, it should be "<value> <unit>"
            try:
                self.unit = elements[1]
            except:
                raise
            self.value = self._str_to_numeric(elements[0])

        # Four elements means 'X ft Y in'.
        # To be implemented later.
        # elif len(elements) == 4:
        #     pass
        else:
            raise ValueError("Incorrect number of elements, could not interpret.")

    def _str_to_numeric(self, value_string):
        if not isinstance(value_string, str):
            raise TypeError("Can only convert strings, not {}".format(type(value_string)))
        try:
            return self._int_or_float(value_string)
        except:
            raise ValueError("Could not convert {} to numeric (int or float)".format(value_string))

    # Simple helper to keep from returning floats where not required.
    @staticmethod
    def _int_or_float(x):
        if float(x) % 1 == 0:
            val = int(x)
        else:
            val = float(x)
        return val

    # Output methods
    def __repr__(self):
        return "Unit({},{}".format(self._value, self._unit)

    def __str__(self):
        return "{} {}".format(self.value, self.unit)

    def __reduce__(self):
        return (Unit, self._value, self._unit)

    # Comparison operations
    def __comparator(self, other_input, operator):
        # Check for valid inputs.
        if type(other_input) not in (Unit, int, float):
            raise TypeError("Can only compare Units to other Units, integers or floats.")

        # Convert if need be.
        if isinstance(other_input,Unit):
            if self.unit != other_input.unit:
                other = other_input.convert(self._unit).value
            else:
                other = other_input.value
        else:
                other = other_input

        # Do the requested operation
        if operator == 'lt':
            return self.value < other
        elif operator == 'le':
            return self.value <= other
        elif operator == 'gt':
            return self.value > other
        elif operator == 'ge':
            return self.value >= other
        elif operator == 'eq':
            return self.value == other
        elif operator == 'ne':
            return self.value != other
        else:
            raise ValueError("Not a valid operator")

    def __lt__(self, other):
        return self.__comparator(other, 'lt')

    def __le__(self, other):
        return self.__comparator(other, 'le')

    def __gt__(self, other):
        return self.__comparator(other, 'gt')

    def __ge__(self, other):
        return self.__comparator(other, 'ge')

    def __eq__(self, other):
        return self.__comparator(other, 'eq')

    def __ne__(self, other):
        return self.__comparator(other, 'ne')

    # Mathematical operators
    def _arithmetic(self, other, operator):
        if isinstance(other, Unit):
            if self.unit_class is not other.unit_class:
                raise TypeError("Units are not the same class.")
            elif self._unit != other._unit:
                other_value = other.convert(self._unit)._value
            else:
                other_value = other._value
        elif isinstance(other,int) or isinstance(other,float):
            other_value = other
        elif isinstance(other,str):
            try:
                other_value = int(other)
            except:
                try:
                    other_value = float(other)
                except:
                    raise TypeError("Other string '{}' could not be cast to int or float.".format(other))
        else:
            raise TypeError("Type {} not supported with Unit.".format(type(other)))

        if operator == 'add':
            return Unit(self._value + other_value, self.unit)
        elif operator == 'sub':
            return Unit(self._value - other_value, self.unit)
        elif operator == 'mul':
            return Unit(self._value * other_value, self.unit)
        elif operator == 'truediv':
            # This will return a float, ie, a percentage
            return self._int_or_float(self._value / other._value)

    def __add__(self, other):
        return self._arithmetic(other, 'add')

    def __sub__(self, other):
        return self._arithmetic(other, 'sub')

    def __mul__(self,other):
        if not (isinstance(other,int) or isinstance(other,float)):
            raise TypeError("Can only multiply unit by a scalar value (int or float)")
        return self._arithmetic(other, 'mul')

    def __truediv__(self, other):
        return self._arithmetic(other, 'truediv')

    def __abs__(self):
        return Unit(abs(self._value), self.unit)

# This is a dummy class so there can be a type to return when something isn't a number.
class NaN:
    def __init__(self, reason=None):
        self._reason = reason

    @property
    def reason(self):
        return self._reason
