#!/usr/bin/env python

import yaml, urllib, lxml
from lxml import etree

with open("../../MyMagicMirrorPy.config", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

### config
lat = str(cfg['openweathermap']['openweathermapLAT'])
lon = str(cfg['openweathermap']['openweathermapLON'])
api = cfg['openweathermap']['openweathermapAPI']
url = "http://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon + "&appid=" + api + "&mode=xml&units=metric"
city = cfg['openweathermap']['openweathermapCityname']

#print(url)

### call API
xmlsource = urllib.urlopen(url)
context = etree.iterparse(xmlsource)

for action, elem in context:
	if elem.getparent() is None: break #fix for bug 1185701
	if elem.tag == "sun":
		sun_rise = elem.attrib['rise']
		sun_set = elem.attrib['set']
	if elem.tag == "temperature":
		temp_max = elem.attrib['max']
		temp_min = elem.attrib['min']
		temp_value = elem.attrib['value']
	if elem.tag == "humidity":
		humidity = elem.attrib['value']
	if elem.tag == "pressure":
		pressure = elem.attrib['value']
	if elem.tag == "speed":
		wind_speed = elem.attrib['value']
		wind_desc = elem.attrib['name']
	if elem.tag == "direction":
		wind_dir = elem.attrib['value']
	if elem.tag == "clouds":
		clouds_id = elem.attrib['value']
		clouds_desc = elem.attrib['name']
	if elem.tag == "weather":
		icon = elem.attrib['icon']

xmlsource.close()

### write it into html code
print("<div id=\"currentweather\">")
print("<div id=\"city\"\>" + city + "</div>") 
print("<div id=\"sunrise\">" + sun_rise + "</div> <div id=\"sunset\">" + sun_set + "</div>")
print("<div id=\"weathericon\"> <img src=\"http://openweathermap.org/img/w/" + icon + ".png\"></div> <div id=\"weatherdesc\">" + clouds_desc + "</dv>")
print("<div id=\"tempvalue\">" + temp_value + "</div> <div id=\"tempmax\">" + temp_max + "</div> <div id=\"tempmin\">" + temp_min + "</div>")
print("<div id=\"windspeed\">" + wind_speed + "km/h </div>")
print("</div)")


#print(humidity, pressure, sun_rise, sun_set, clouds_id, wind_desc, wind_dir)

