# -*- coding: utf-8 -*-
# set up the environment using the settings module
from django.core.management import setup_environ
from lxml import etree

import settings
setup_environ(settings)
from django.db import models
from map.models import BusesRoutes, BusStops, BusesAndBusStops

xml_buses = u"""<ymaps:ymaps xmlns:ymaps="http://maps.yandex.ru/ymaps/1.x"
                    xmlns:repr="http://maps.yandex.ru/representation/1.x"
                    xmlns:gml="http://www.opengis.net/gml"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://maps.yandex.ru/schemas/ymaps/1.x/ymaps.xsd">
                    <repr:Representation>
                        <repr:Style gml:id="styleBusStop">        
                            <repr:parentStyle>default#busIcon</repr:parentStyle> 
                        </repr:Style>
                        <repr:Style gml:id="styleRouteParent"> 
                            <repr:lineStyle>
                                <repr:strokeWidth>4</repr:strokeWidth> 
                            </repr:lineStyle> 
                        </repr:Style> 
                    </repr:Representation>
                </ymaps:ymaps>"""

p = BusStops.objects.filter(bus_stop_id=4)
root = etree.fromstring(xml_buses)
routes = BusesRoutes.objects.order_by('route')

def description(carrier, interval, start_time, end_time, first_and_last_stops):
    info = u"""<div>{0}</div>
                <div>Перевозчик: {1}</div>
                <div>Интервал движения: {2}</div>
                <div>Начало работы: {3}</div>
                <div>Последнее отправление: {4}</div>""".format(first_and_last_stops, carrier, interval, start_time, end_time)
    return info

for item in routes:
    elem_style = etree.SubElement(root[0], "{http://maps.yandex.ru/representation/1.x}Style")
    elem_style.set("{http://www.opengis.net/gml}id", "styleRoute_{0}".format(item.route))
    etree.SubElement(elem_style, "{http://maps.yandex.ru/representation/1.x}parentStyle").text = "#styleRouteParent"
    elem_line_style = etree.SubElement(elem_style, "{http://maps.yandex.ru/representation/1.x}lineStyle")
    etree.SubElement(elem_line_style, "{http://maps.yandex.ru/representation/1.x}strokeColor").text = item.color
    
    elem_geoCollection = etree.SubElement(root, "{http://maps.yandex.ru/ymaps/1.x}GeoObjectCollection")
    etree.SubElement(etree.SubElement(etree.SubElement(elem_geoCollection, "{http://www.opengis.net/gml}metaDataProperty"), "{http://maps.yandex.ru/ymaps/1.x}AnyMetaData"), "route").text = str(item.route)
    elem_featureMembers = etree.SubElement(elem_geoCollection, "{http://www.opengis.net/gml}featureMembers")
    elem_routeLineGeoObject = etree.SubElement(elem_featureMembers, "{http://maps.yandex.ru/ymaps/1.x}GeoObject")
    etree.SubElement(elem_routeLineGeoObject, "{http://www.opengis.net/gml}name").text = u"Автобус: {0}".format(item.route)
    etree.SubElement(elem_routeLineGeoObject, "{http://www.opengis.net/gml}description").text = description(item.carrier,
                                                                                                            item.interval,
                                                                                                            item.start_time,
                                                                                                            item.end_time,
                                                                                                            item.first_and_last_stops)
    etree.SubElement(etree.SubElement(elem_routeLineGeoObject, "{http://www.opengis.net/gml}LineString"), "{http://www.opengis.net/gml}posList").text = item.coordinates
    etree.SubElement(elem_routeLineGeoObject, "{http://maps.yandex.ru/ymaps/1.x}style").text = "#styleRoute_" + str(item.route)
    
    bus_stops_and_routes = BusesAndBusStops.objects.filter(route=item)
    for item2 in bus_stops_and_routes:
        bus_stops = BusStops.objects.filter(bus_stop_id=item2.bus_stop_id)
        elem_PointGeoObject = etree.SubElement(elem_featureMembers, "{http://maps.yandex.ru/ymaps/1.x}GeoObject")
        etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}name").text = u"Остановка: «" + bus_stops[0].name + u"»"
        etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}description").text = bus_stops[0].buses
        etree.SubElement(etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}Point"), "{http://www.opengis.net/gml}pos").text = bus_stops[0].coordinates
        etree.SubElement(elem_PointGeoObject, "{http://maps.yandex.ru/ymaps/1.x}style").text = "#styleBusStop"

#print routes[0].route
print(etree.tostring(root, pretty_print=True, encoding="utf-8"))
#print bus_stops_and_routes[0].bus_stop_id
#bus_stops = BusStops.objects.filter(bus_stop_id=bus_stops_and_routes[0].bus_stop_id)
#print len(bus_stops)