# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Companies(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    address = models.TextField()
    coordinates = models.TextField()
    phone1 = models.TextField()
    description1 = models.TextField()
    phone2 = models.TextField()
    description2 = models.TextField()
    phone3 = models.TextField()
    description3 = models.TextField()
    phone4 = models.TextField()
    description4 = models.TextField()
    phone5 = models.TextField()
    description5 = models.TextField()
    work_hours = models.TextField()
    site = models.TextField()
    email = models.TextField()
    additional_info = models.TextField()
    photo1 = models.TextField()
    photo2 = models.TextField()
    photo3 = models.TextField()
    photo4 = models.TextField()
    photo5 = models.TextField()
    photo6 = models.TextField()
    photo7 = models.TextField()
    photo8 = models.TextField()
    video = models.TextField()
    icon = models.TextField()
    highlight = models.IntegerField()
    rubric = models.IntegerField()
    city = models.TextField()
    class Meta:
        db_table = u'companies'
        ordering = ('name',)

class BusesRoutes(models.Model):
    city = models.TextField()
    route = models.IntegerField(primary_key=True)
    coordinates = models.TextField()
    color = models.TextField()
    width = models.IntegerField()
    carrier = models.TextField()
    interval = models.TextField()
    start_time = models.TextField()
    end_time = models.TextField()
    first_and_last_stops = models.TextField()
    class Meta:
        db_table = u'buses_routes'

class BusStops(models.Model):
    bus_stop_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    coordinates = models.TextField()
    icon = models.TextField()
    buses = models.TextField()
    lon = models.DecimalField(max_digits=8, decimal_places=6)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    class Meta:
        db_table = u'bus_stops'

class Rubrics(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.TextField()
    class Meta:
        db_table = u'rubrics'

class BusesAndBusStops(models.Model):
    route = models.ForeignKey(BusesRoutes, db_column='route')
    bus_stop = models.ForeignKey(BusStops)
    id = models.IntegerField()
    class Meta:
        db_table = u'buses_and_bus_stops'

class OrangeCompanies(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    address = models.TextField()
    coordinates = models.TextField()
    phone1 = models.TextField()
    description1 = models.TextField()
    phone2 = models.TextField()
    description2 = models.TextField()
    phone3 = models.TextField()
    description3 = models.TextField()
    phone4 = models.TextField()
    description4 = models.TextField()
    phone5 = models.TextField()
    description5 = models.TextField()
    work_hours = models.TextField()
    site = models.TextField()
    email = models.TextField()
    additional_info = models.TextField()
    photo1 = models.TextField()
    photo2 = models.TextField()
    photo3 = models.TextField()
    photo4 = models.TextField()
    photo5 = models.TextField()
    photo6 = models.TextField()
    photo7 = models.TextField()
    photo8 = models.TextField()
    video = models.TextField()
    icon = models.TextField()
    highlight = models.IntegerField()
    rubric = models.IntegerField()
    city = models.TextField()
    discount = models.TextField()
    discount_terms = models.TextField()
    class Meta:
        db_table = u'orange_companies'

class OrangeRubrics(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.TextField()
    class Meta:
        db_table = u'orange_rubrics'

class MainRubrics(models.Model):
    rubric_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    class Meta:
        db_table = u'main_rubrics'
        ordering = ('rubric_id',)

