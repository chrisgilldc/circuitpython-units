# Units
#### A unit conversion library for CircuitPython

This is a quick and dirty hack to get Pint like functionality in CircuitPython. I put this together because I didn't
see an official port of Pint and didn't want to take on doing a full port, which is beyond my skills.

## Supported Units

Units supports different classes of units. Operations can be performed within a class, but not across classes.
Since I hacked this together for my own needs, this is a limited set of units and doesn't claim to be exhaustive.

Currently supported units are below, with their recognized abbreviations.

* Distance
  * Millimeters (mm) 
  * Centimeters (cm)
  * Meters (m)
  * Inches (in)
  * Feet (ft)
  * Yards (y)
* Time
  * Seconds (s)
  * Minutes (min)
  * Hours (h)

## Supported Operations

Operations may be performed between two Unit objects *only*.

* Comparisons
  * Less than
  * Less than or Equal
  * Equal
  * Not Equal
  * Greater than
  * Greater than or Equal
* Operations
  * Addition
  * Subtraction

Multiplying and dividing units is not currently supported.

## Using Units

A Unit can be by passing a numeric (int or float) value and the unit to use - see abbreviations above.
````
>>> from unit import Unit
>>> u = Unit(22,"in")
>>> print(u)
22 in
````

Alternately, the library will try to interpret a string.
````


````