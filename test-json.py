# -*- coding: utf-8 -*-
# set up the environment using the settings module
from django.core.management import setup_environ
from lxml import etree

import settings
import json
setup_environ(settings)
from django.db import models
from map.models import BusesRoutes, BusStops, BusesAndBusStops, Companies

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

p = Companies.objects.filter(rubric=105101)
json_dict = {"items":[]}
json_list = []
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
phones = {"phones":[]}
phones_1 = []
phones_1.append({"phone":"", "description":""})
phones_1[0]["phone"] = p[0].phone1
phones_1[0]["description"] = p[0].description1
phones["phones"] = Phones(p[0])
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
print "\n" + json.dumps(json_dict) + "\n"
#test = {"phones":[{"phone":"", "description":""}, {"phone":"", "description":""}]}