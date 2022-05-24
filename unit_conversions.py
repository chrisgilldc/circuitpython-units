# Unit classes and conversions.
# When the module gets loaded, these are built into the master CONVERSION_LOOKUP dict, which defines conversion from
# each unit into each other unit in the class.
# You can't convert across classes, that's silly.

# Within a class, each unit has a dict for all other units, converting one of that unit into the base unit.
# For example, the Meter value in Distance would define mm as 0.001 meters, inches as 0.0254 meters, and so on.
# It also should include itself, with a conversion factor of '1'.

DISTANCE = {
    'mm': {'mm': 1, 'cm': 10, 'm': 1000, 'in': 25.4, 'ft': 304.8, 'yd': 914.4},
    'cm': {'mm': 0.1, 'cm': 1, 'm': 100, 'in': 2.54, 'ft': 30.48, 'yd': 91.44},
    'm': {'mm': 0.001, 'cm': 0.01, 'm': 1, 'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144},
    'in': {'mm': 0.0393701, 'cm': 0.393701, 'm': 39.3701, 'in': 1, 'ft': 12, 'yd': 36},
    'ft': {'mm': 0.00328084, 'cm': 0.0328084, 'm': 3.28084, 'in': 12, 'ft': 1, 'yd': 3},
    'yd': {'mm': 0.00109361, 'cm': 0.0109361, 'm': 1.09361, 'in': 1/36, 'ft': 3, 'yd': 1}
}

SPEED = {
    'kph': {'kph': 1, 'mph': 1.60934},
    'mph': {'kph': 0.621371, 'mph': 1}
}

TIME = {
    's': {'s': 1, 'min': 60, 'h': 3600, 'd': 86400},
    'min': {'s': 1/60, 'min': 1, 'h': 60, 'd': 1440},
    'h': {'s': 1/3600, 'min': 1/60, 'h': 1, 'd': 24},
    'd': {'s': 1/86400, 'min': 1/1440, 'd': 1, 'h': 1/24}
}

# enumerate the classes, so they can be iterated.
CLASSES = [DISTANCE, SPEED, TIME]
