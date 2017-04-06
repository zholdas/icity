# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext
from models import BusesRoutes, BusStops, BusesAndBusStops, Companies, OrangeCompanies, Rubrics, MainRubrics, OrangeRubrics
from django.shortcuts import render_to_response, redirect
from lxml import etree
from django.core.mail import send_mail
import math
import json
from minidetector import detect_mobile

#отображение заглушки главной страницы
@detect_mobile
def index(request):
    return render_to_response('index-webflow.html', context_instance=RequestContext(request))
    if request.mobile:
        return redirect('http://m.icity.kz/')
    buses = BusesRoutes.objects.order_by('route')
    rubrics = Rubrics.objects.order_by('name')
    main_rubrics = MainRubrics.objects.all()
    orange_rubrics = OrangeRubrics.objects.all()
    return render_to_response('index.html', {"buses": buses, "main_rubrics": main_rubrics, "rubrics": rubrics, "orange_rubrics": orange_rubrics}, context_instance=RequestContext(request))

#отображение работающей карты
def rip(request):
    buses = BusesRoutes.objects.order_by('route')
    rubrics = Rubrics.objects.order_by('name')
    main_rubrics = MainRubrics.objects.all()
    orange_rubrics = OrangeRubrics.objects.all()
    return render_to_response('index.html', {"buses": buses, "main_rubrics": main_rubrics, "rubrics": rubrics, "orange_rubrics": orange_rubrics}, context_instance=RequestContext(request))

#шаблон для заполнения маршрута автобуса
xml_bus = u"""<ymaps:ymaps xmlns:ymaps="http://maps.yandex.ru/ymaps/1.x"
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

#шаблон для заполнения маршрутов автобусов
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
                    <ymaps:GeoObjectCollection>
                        <gml:featureMembers>
                        </gml:featureMembers>
                    </ymaps:GeoObjectCollection>
                </ymaps:ymaps>"""
                
#шаблон для заполнения остановок
xml_bus_stops = u"""<ymaps:ymaps xmlns:ymaps="http://maps.yandex.ru/ymaps/1.x"
                    xmlns:repr="http://maps.yandex.ru/representation/1.x"
                    xmlns:gml="http://www.opengis.net/gml"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://maps.yandex.ru/schemas/ymaps/1.x/ymaps.xsd">
                    <repr:Representation>
                        <repr:Style gml:id="styleBusStop">        
                            <repr:parentStyle>default#busIcon</repr:parentStyle> 
                        </repr:Style>                        
                    </repr:Representation>
                    <ymaps:GeoObjectCollection>
                        <gml:featureMembers>
                        </gml:featureMembers>
                    </ymaps:GeoObjectCollection>
                </ymaps:ymaps>"""
                
#метод для формирования xml документа всех остановки
def all_bus_stops(request):
    root = etree.fromstring(xml_bus_stops)
    bus_stops = BusStops.objects.all()
    for item in bus_stops:
        bus_stop_buses = BusesAndBusStops.objects.filter(bus_stop=item.bus_stop_id)
        elem_PointGeoObject = etree.SubElement(root[1][0], "{http://maps.yandex.ru/ymaps/1.x}GeoObject")
        etree.SubElement(etree.SubElement(etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}metaDataProperty"), "{http://maps.yandex.ru/ymaps/1.x}AnyMetaData"), "bus_stop_id").text = str(item.bus_stop_id)
        etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}name").text = u"Остановка: «" + item.name + u"»"            
        etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}description").text = u"Автобусы: " + ", ".join("%s" % item2.route.route for item2 in bus_stop_buses)
        etree.SubElement(etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}Point"), "{http://www.opengis.net/gml}pos").text = item.coordinates
        etree.SubElement(elem_PointGeoObject, "{http://maps.yandex.ru/ymaps/1.x}style").text = "#styleBusStop"
    return HttpResponse(etree.tostring(root), mimetype='application/xml')

def description(carrier, interval, start_time, end_time, first_and_last_stops):
    info = u"""<div>{0}</div>
                <div>Перевозчик: {1}</div>
                <div>Интервал движения: {2}</div>
                <div>Начало работы: {3}</div>
                <div>Последнее отправление: {4}</div>""".format(first_and_last_stops, carrier, interval, start_time, end_time)
    return info

#метод для формирования xml для одного маршрута              
def routes(request, aRoute):
    root = etree.fromstring(xml_bus)
    get_route = BusesRoutes.objects.get(route=aRoute)
    get_bus_stops = BusesAndBusStops.objects.filter(route=aRoute)
    
    elem_style = etree.SubElement(root[0], "{http://maps.yandex.ru/representation/1.x}Style")
    elem_style.set("{http://www.opengis.net/gml}id", "styleRoute_{0}".format(get_route.route))
    etree.SubElement(elem_style, "{http://maps.yandex.ru/representation/1.x}parentStyle").text = "#styleRouteParent"
    elem_line_style = etree.SubElement(elem_style, "{http://maps.yandex.ru/representation/1.x}lineStyle")
    etree.SubElement(elem_line_style, "{http://maps.yandex.ru/representation/1.x}strokeColor").text = get_route.color
    
    elem_geoCollection = etree.SubElement(root, "{http://maps.yandex.ru/ymaps/1.x}GeoObjectCollection")
    etree.SubElement(etree.SubElement(etree.SubElement(elem_geoCollection, "{http://www.opengis.net/gml}metaDataProperty"), "{http://maps.yandex.ru/ymaps/1.x}AnyMetaData"), "route").text = str(get_route.route)
    elem_featureMembers = etree.SubElement(elem_geoCollection, "{http://www.opengis.net/gml}featureMembers")
    elem_routeLineGeoObject = etree.SubElement(elem_featureMembers, "{http://maps.yandex.ru/ymaps/1.x}GeoObject")
    etree.SubElement(elem_routeLineGeoObject, "{http://www.opengis.net/gml}name").text = u"Автобус: {0}".format(get_route.route)
    etree.SubElement(elem_routeLineGeoObject, "{http://www.opengis.net/gml}description").text = description(get_route.carrier,
                                                                                                            get_route.interval,
                                                                                                            get_route.start_time,
                                                                                                            get_route.end_time,
                                                                                                            get_route.first_and_last_stops)
    etree.SubElement(etree.SubElement(elem_routeLineGeoObject, "{http://www.opengis.net/gml}LineString"), "{http://www.opengis.net/gml}posList").text = get_route.coordinates
    etree.SubElement(elem_routeLineGeoObject, "{http://maps.yandex.ru/ymaps/1.x}style").text = "#styleRoute_" + str(get_route.route)
    
    for item2 in get_bus_stops:
        bus_stops = BusStops.objects.filter(bus_stop_id=item2.bus_stop_id)
        bus_stop_buses = BusesAndBusStops.objects.filter(bus_stop=item2.bus_stop_id)
        elem_PointGeoObject = etree.SubElement(elem_featureMembers, "{http://maps.yandex.ru/ymaps/1.x}GeoObject")
        etree.SubElement(etree.SubElement(etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}metaDataProperty"), "{http://maps.yandex.ru/ymaps/1.x}AnyMetaData"), "bus_stop_id").text = str(bus_stops[0].bus_stop_id)
        etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}name").text = u"Остановка: «" + bus_stops[0].name + u"»"            
        etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}description").text = u"Автобусы: " + ", ".join("%s" % item.route.route for item in bus_stop_buses)
        etree.SubElement(etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}Point"), "{http://www.opengis.net/gml}pos").text = bus_stops[0].coordinates
        etree.SubElement(elem_PointGeoObject, "{http://maps.yandex.ru/ymaps/1.x}style").text = "#styleBusStop"
    return HttpResponse(etree.tostring(root), mimetype='application/xml')    

#метод для формирования xml документа содержащего все маршруты автобусов и остановки
def all_routes(request):    
    root = etree.fromstring(xml_buses)
    routes = BusesRoutes.objects.order_by('route')
    
    for item in routes:
        elem_style = etree.SubElement(root[0], "{http://maps.yandex.ru/representation/1.x}Style")
        elem_style.set("{http://www.opengis.net/gml}id", "styleRoute_{0}".format(item.route))
        etree.SubElement(elem_style, "{http://maps.yandex.ru/representation/1.x}parentStyle").text = "#styleRouteParent"
        elem_line_style = etree.SubElement(elem_style, "{http://maps.yandex.ru/representation/1.x}lineStyle")
        etree.SubElement(elem_line_style, "{http://maps.yandex.ru/representation/1.x}strokeColor").text = item.color
        
        #elem_geoCollectionRoot = etree.SubElement(root, "{http://maps.yandex.ru/ymaps/1.x}GeoObjectCollection")
        #elem_featureMembersRoot = etree.SubElement(elem_geoCollectionRoot, "{http://www.opengis.net/gml}featureMembers")
        elem_geoCollection = etree.SubElement(root[1][0], "{http://maps.yandex.ru/ymaps/1.x}GeoObjectCollection")
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
            etree.SubElement(etree.SubElement(etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}metaDataProperty"), "{http://maps.yandex.ru/ymaps/1.x}AnyMetaData"), "bus_stop_id").text = str(bus_stops[0].bus_stop_id)
            etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}name").text = u"Остановка: «" + bus_stops[0].name + u"»"            
            etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}description").text = u"Автобусы: " + bus_stops[0].buses
            etree.SubElement(etree.SubElement(elem_PointGeoObject, "{http://www.opengis.net/gml}Point"), "{http://www.opengis.net/gml}pos").text = bus_stops[0].coordinates
            etree.SubElement(elem_PointGeoObject, "{http://maps.yandex.ru/ymaps/1.x}style").text = "#styleBusStop"
    return HttpResponse(etree.tostring(root), mimetype='application/xml')

#метод для определения расстояния между точками
def distance(llat1, llong1, llat2, llong2):
    rad = 6372795
    #в радианах
    lat1 = llat1*math.pi/180.
    lat2 = llat2*math.pi/180.
    long1 = llong1*math.pi/180.
    long2 = llong2*math.pi/180.
    
    #косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)
    
    #вычисления длины большого круга
    y = math.sqrt(math.pow(cl2*sdelta,2)+math.pow(cl1*sl2-sl1*cl2*cdelta,2))
    x = sl1*sl2+cl1*cl2*cdelta
    ad = math.atan2(y,x)
    dist = ad*rad
    return dist #возвращает расстояние в метрах

#метод для поиска ближайжих объектов (500 метров)
def nearest(request):
    if request.method == 'POST':
        if request.POST['object'] == 'busstop':
            p = BusStops.objects.all()
            bus_stops_list = []
            for item in p:
                if distance(float(request.POST['lat']), float(request.POST['lon']), float(item.lat), float(item.lon)) < 500:
                    bus_stops_list.append(item.bus_stop_id)
        bus_stops_string = ""
        for i in bus_stops_list:
            bus_stops_string += str(i) + " "
        return HttpResponse(bus_stops_string)

#метод для отправки письма с сообщением об ошибке
def feedback(request):
    if request.method == 'POST':
        #return HttpResponse(request.GET['email'] + " " + request.GET['message'])
        send_mail(
                  request.POST['email'],
                  request.POST['message'],
                  request.POST['email'],
                  ['feedback@icity.kz'],
                  )
        return HttpResponse('Спасибо')

def Phones(aCompanyObject):
    phone_list = []    
    if aCompanyObject.phone1:
        phone_dict = {"phone":"", "description":""}
        phone_dict["phone"] = aCompanyObject.phone1
        phone_dict["description"] = aCompanyObject.description1
        phone_list.append(phone_dict)
    else:
        return phone_list
    if aCompanyObject.phone2:
        phone_dict = {"phone":"", "description":""}
        phone_dict["phone"] = aCompanyObject.phone2
        phone_dict["description"] = aCompanyObject.description2
        phone_list.append(phone_dict)
    else:
        return phone_list
    if aCompanyObject.phone3:
        phone_dict = {"phone":"", "description":""}
        phone_dict["phone"] = aCompanyObject.phone3
        phone_dict["description"] = aCompanyObject.description3
        phone_list.append(phone_dict)
    if aCompanyObject.phone4:
        phone_dict = {"phone":"", "description":""}
        phone_dict["phone"] = aCompanyObject.phone4
        phone_dict["description"] = aCompanyObject.description4
        phone_list.append(phone_dict)
    else:
        return phone_list
    if aCompanyObject.phone5:
        phone_dict = {"phone":"", "description":""}
        phone_dict["phone"] = aCompanyObject.phone5
        phone_dict["description"] = aCompanyObject.description5
        phone_list.append(phone_dict)
    return phone_list

def Photos(aCompanyObject):
    photos_list = []    
    if aCompanyObject.photo1:
        photo_dict = {"href":""}
        photo_dict["href"] = aCompanyObject.photo1
        photos_list.append(photo_dict)
    else:
        return photos_list
    if aCompanyObject.photo2:
        photo_dict = {"href":""}
        photo_dict["href"] = aCompanyObject.photo2
        photos_list.append(photo_dict)
    else:
        return photos_list
    if aCompanyObject.photo3:
        photo_dict = {"href":""}
        photo_dict["href"] = aCompanyObject.photo3
        photos_list.append(photo_dict)
    else:
        return photos_list
    if aCompanyObject.photo4:
        photo_dict = {"href":""}
        photo_dict["href"] = aCompanyObject.photo4
        photos_list.append(photo_dict)
    else:
        return photos_list
    if aCompanyObject.photo5:
        photo_dict = {"href":""}
        photo_dict["href"] = aCompanyObject.photo5
        photos_list.append(photo_dict)
    else:
        return photos_list
    if aCompanyObject.photo6:
        photo_dict = {"href":""}
        photo_dict["href"] = aCompanyObject.photo6
        photos_list.append(photo_dict)
    else:
        return photos_list
    if aCompanyObject.photo7:
        photo_dict = {"href":""}
        photo_dict["href"] = aCompanyObject.photo7
        photos_list.append(photo_dict)
    else:
        return photos_list
    if aCompanyObject.photo8:
        photo_dict = {"href":""}
        photo_dict["href"] = aCompanyObject.photo8
        photos_list.append(photo_dict)
    return photos_list
    
def companies(request, rubric_id):
    p = Companies.objects.filter(rubric=rubric_id)
    json_dict = {"items":[]}
    json_list = []
    for item in p:        
        general_dict = {"name":"",
                         "address":"",
                         "coordinates":"",
                         "phones":[],
                         "work_hours":"",
                         "site":"",
                         "email":"",
                         "additional_info":"",
                         "photos":[],
                         "video":"",
                         "icon":"",
                         "highlight":"" }
        general_dict["name"] = item.name
        general_dict["address"] = item.address
        general_dict["coordinates"] = item.coordinates
        general_dict["phones"] = Phones(item)
        general_dict["work_hours"] = item.work_hours
        general_dict["site"] = item.site
        general_dict["email"] = item.email
        general_dict["additional_info"] = item.additional_info
        general_dict["photos"] = Photos(item)
        general_dict["video"] = item.video
        general_dict["icon"] = item.icon
        general_dict["highlight"] = item.highlight
        json_list.append(general_dict)
    json_dict["items"] = json_list
    return HttpResponse(json.dumps(json_dict), mimetype="application/json")

def orangeCompanies(request, rubric_id):
    p = OrangeCompanies.objects.filter(rubric=rubric_id)
    json_dict = {"items":[]}
    json_list = []
    for item in p:        
        general_dict = {"name":"",
                         "address":"",
                         "coordinates":"",
                         "phones":[],
                         "work_hours":"",
                         "site":"",
                         "email":"",
                         "additional_info":"",
                         "photos":[],
                         "video":"",
                         "discount":"",
                         "discount_terms":"",
                         "icon":"",
                         "highlight":"" }
        general_dict["name"] = item.name
        general_dict["address"] = item.address
        general_dict["coordinates"] = item.coordinates
        general_dict["phones"] = Phones(item)
        general_dict["work_hours"] = item.work_hours
        general_dict["site"] = item.site
        general_dict["email"] = item.email
        general_dict["additional_info"] = item.additional_info
        general_dict["photos"] = Photos(item)
        general_dict["video"] = item.video
        general_dict["discount"] = item.discount
        general_dict["discount_terms"] = item.discount_terms
        general_dict["icon"] = item.icon
        general_dict["highlight"] = item.highlight
        json_list.append(general_dict)
    json_dict["items"] = json_list
    return HttpResponse(json.dumps(json_dict), mimetype="application/json")

def test(request):
    p = BusesRoutes.objects.filter(route=1)
    p1 = BusesAndBusStops.objects.filter(route=1)
    #p2 = BusStops.objects.
    def description(carrier, interval, start_time, end_time, first_and_last_stops):
            info = u"""<div>%s</div>
                        <div>Перевозчик: %s</div>
                        <div>Интервал движения: %s</div>
                        <div>Начало работы: %s</div>
                        <div>Последнее отправление: %s</div>""" % (first_and_last_stops, carrier, interval, start_time, end_time)
            return info
    xml1 = u"""<?xml version="1.0" encoding="UTF-8"?>
<ymaps:ymaps xmlns:ymaps="http://maps.yandex.ru/ymaps/1.x"
   xmlns:repr="http://maps.yandex.ru/representation/1.x"
   xmlns:gml="http://www.opengis.net/gml"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://maps.yandex.ru/schemas/ymaps/1.x/ymaps.xsd">
    <repr:Representation>"""
    xml1 += u"""<repr:Style gml:id="bus_stop"> 
          <repr:parentStyle>default#busIcon</repr:parentStyle>
        </repr:Style>
                        <repr:Style gml:id="bus_astana_%s">                           
                            <repr:lineStyle> 
                                <repr:strokeColor>%s</repr:strokeColor> 
                                <repr:strokeWidth>%s</repr:strokeWidth>
                            </repr:lineStyle>                            
                        </repr:Style>""" % (p[0].route, p[0].color, p[0].width if p[0].width != None else '1')
    xml1 += u"</repr:Representation>"
    xml1 += u"""<ymaps:GeoObjectCollection>
                        <gml:name>Маршруты автобусов</gml:name>
                        <gml:featureMembers>"""
    xml1 += u"""<ymaps:GeoObject> 
                            <gml:metaDataProperty><route>%s</route></gml:metaDataProperty>
                            <gml:name>Маршрут %s</gml:name> 
                            <gml:description>%s</gml:description> 
                            <gml:LineString> 
                                <gml:posList>%s</gml:posList> 
                            </gml:LineString> 
                            <ymaps:style>#bus_astana_%s</ymaps:style> 
                        </ymaps:GeoObject>""" % (p[0].route,
                                                 p[0].route,
                                                 description(p[0].carrier, p[0].interval, p[0].start_time, p[0].end_time, p[0].first_and_last_stops),
                                                 p[0].coordinates,
                                                 p[0].route)
    xml1 += u"""<ymaps:GeoObject> 
                <ymaps:style>#bus_stop</ymaps:style> 
                <gml:name>%s</gml:name> 
                <gml:description>%s</gml:description> 
                <gml:Point> 
                    <gml:pos>%s</gml:pos> 
                </gml:Point> 
            </ymaps:GeoObject> """ % ()
    xml1 += u"""</gml:featureMembers> 
                </ymaps:GeoObjectCollection> 
            </ymaps:ymaps>"""
    return HttpResponse(xml1, mimetype='application/xml')
    