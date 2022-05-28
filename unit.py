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

    def unit_class(self):
        return self._unit_class

    @unit.setter
    def unit(self, unit):
        """Set the unit of the object. Does *not* convert values.

        :param unit: The level of the message
        """
        found = False
        for unit_class in unit_conversions.CLASSES:
            if unit in getattr(unit_conversions,unit_class):
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
        if self._unit is "ft-in" and not isinstance(value, dict):
            raise TypeError("Foot-inches unit type requires dict with 'ft' and 'in' elements.")
        if not isinstance(value, (int, float)):
            raise TypeError("Unit value must be int or float, got {} input".format(type(value)))
        self._value = value

    def convert(self, output_unit):
        # Check for issues.
        if output_unit not in getattr(unit_conversions, self._unit_class):
            raise ValueError("Requested output unit '{}' is not supported.".format(output_unit))

        try:
            conversion_factor = getattr(unit_conversions, self._unit_class)[self._unit][output_unit]
        except:
            raise ValueError("No conversion path from {} to {}".format(self._unit, output_unit))

        self_in_target = self.value * conversion_factor

        return Unit(self_in_target, output_unit)



    def _ft_in_normalize(self, value):
        pass

    def _ft_in_old(self):
        # Special handling for feet-inches.
        (val_inches, unit) = self.convert('in')
        val_feet = floor(val_inches / 12)
        val_inches = val_inches % 12
        if val_inches == 0:
            return Unit(val_feet, 'ft'), None
        else:
            return Unit(val_feet, 'ft'), Unit(val_inches, 'in')

    def __repr__(self):
        return "Unit({},{}".format(self._value,self._unit)

    def __str__(self):
        return "{} {}".format(self.value, self.unit)

    def __reduce__(self):
        return (Unit,self._value, self._unit)

    def __comparator(self, other_input, operator):
        # Check for valid inputs.
        if not isinstance(other_input, Unit):
            raise TypeError("Can only compare Units to other Units.")

        # Convert if need be.
        if self.unit != other_input.unit:
            print("Self unit: {}\tOther unit: {}".format(self.unit, other_input.unit))
            other = other_input.convert(self._unit)
            print("Unit converted: {} {}".format(other.value, other.unit))
        else:
            other = other_input

        # Do the requested operation
        if operator == 'lt':
            print("Comparing {} to {}".format(self.value, other.value))
            return self.value < other.value
        elif operator == 'le':
            print("Comparing {} to {}".format(self.value, other.value))
            return self.value <= other.value
        elif operator == 'gt':
            print("Comparing {} to {}".format(self.value, other.value))
            return self.value > other.value
        elif operator == 'ge':
            print("Comparing {} to {}".format(self.value, other.value))
            return self.value >= other.value
        elif operator == 'eq':
            print("Comparing {} to {}".format(self.value, other.value))
            return self.value == other.value
        elif operator == 'ne':
            print("Comparing {} to {}".format(self.value, other.value))
            return self.value != other.value
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

    def _arithmatic(self, other, operator):
        if not isinstance(other, Unit):
            raise TypeError("Can only compare Units to other Units.")
        elif self._unit_class is not other._unit_class:
            raise TypeError("Units are not the same class.")

        if self._unit != other._unit:
            other = other.convert(self._unit)

        if operator == 'add':
            return Unit(self._value + other._value, self.unit)
        elif operator == 'sub':
            return Unit(self._value - self._value, self._unit)

    def __add__(self, other):
        return self._arithmatic(other, 'add')

    def __sub__(self, other):
        return self._arithmatic(other, 'sub')

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
    def _int_or_float(self, x):
        if float(x) % 1 == 0:
            val = int(x)
        else:
            val = float(x)
        return val
