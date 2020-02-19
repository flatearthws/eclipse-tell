#!/usr/bin/env python
'''
eclipse-tell.py

takes the latitude, longitude, and time of the observer and determine
if an eclipse is occuring.
'''

import ephem
import re
import sys
import math
from datetime import datetime, timedelta
from dateutil import parser

rad2deg = 180/math.pi
deg2rad = math.pi/180

def dms2dd(degrees, minutes, seconds, sign=1):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    dd *= sign
    return dd;

def parse_dms(dms):
    parts = re.split('[^\d]+', dms)
    sign = -1 if re.search('[swSW]', dms) else 1
    deg = dms2dd(parts[0], parts[1], parts[2], sign)

    return deg

try:
    latinput = sys.argv[1]
except IndexError:
    latinput = input("latitude: ")

try:
    loninput = sys.argv[2]
except IndexError:
    loninput = input("longitude: ")

try:
    timeinput = sys.argv[3]
except IndexError:
    timeinput = input("time: ")

latitude = parse_dms(latinput)
longitude = parse_dms(loninput)
time = parser.parse(timeinput)

print("latitude (degrees): ", latitude)
print("longitude (degrees): ", longitude)
print("time: ", time)

observer = ephem.Observer()
observer.lon = longitude * deg2rad
observer.lat = latitude * deg2rad
observer.date = time

moon = ephem.Moon(observer)
sun = ephem.Sun(observer)

moondiameter = moon.size / 3600
sundiameter = sun.size / 3600
moonradius = moondiameter / 2
sunradius = sundiameter / 2
separation = abs(ephem.separation(moon, sun)) * rad2deg

print("moon angular size (degrees): ", moondiameter)
print("sun angular size (degrees): ", sundiameter)
print("sun altitude (degrees): ", sun.alt * rad2deg )
print("sun azimuth (degrees): ", sun.az * rad2deg)
print("sun moon separation (degrees)", separation)

if sun.alt < 0:
    type = "sun is below the horizon, no solar eclipse is possible"
else:
    if separation < abs(moonradius - sunradius): # total or annular
        if sunradius > moonradius:
            type = "annular solar eclipse"
        else:
            type = "total solar eclipse"
    elif separation < moonradius + sunradius:
        type = "partial solar eclipse"

print("type of eclipse: ", type)
