#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from random import choice
from django.core.exceptions import ValidationError

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from rapidsms.models import ExtensibleModelBase
from rapidsms.contrib.locations.models import Location, Point
from django.template.defaultfilters import slugify
import reversion
from django.conf import settings
if settings.CASCADE_UPDATE_TO_FRED:
  from fred_consumer.fred_connect import FredFacilitiesFetcher

class HealthFacilityTypeBase(models.Model):

    class Meta:
        app_label = 'healthmodels'

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name


class HealthFacilityType(HealthFacilityTypeBase):
    __metaclass__ = ExtensibleModelBase

    class Meta:
        app_label = 'healthmodels'
        verbose_name = _("Health Facility Type")
        verbose_name_plural = _("Health Facility Types")

OWNERS = (
          ('GOVT', 'Government'),
          ('NGO', 'NGO'),
          ('PRIVATE', 'Private'),
          )
AUTHORITIES = (
               ('AIDS PROG', 'AIDS PROG'),
               ('COMMUNITY', 'COMMUNITY'),
               ('CSO', 'CSO'),
               ('GTZ', 'GTZ'),
               ('HOSFA', 'HOSFA'),
               ('MAP', 'MAP'),
               ('MSU', 'MSU'),
               ('OTHER NGO', 'OTHER NGO'),
               ('PRIVATE', 'PRIVATE'),
               ('RH UGANDA', 'RH UGANDA'),
               ('RHU', 'RHU'),
               ('SDA', 'SDA'),
               ('TEA FACTORY', 'TEA FACTORY'),
               ('TOURISM', 'TOURISM'),
               ('UCBM', 'UCBM'),
               ('UG. CLAYS', 'UG. CLAYS'),
               ('UMMB', 'UMMB'),
               ('UNHCR', 'UNHCR'),
               ('UPMB', 'UPMB'),
               ('WORLD VISION', 'WORLD VISION'),
               )
class HealthFacilityBase(models.Model):

    class Meta:
        app_label = 'healthmodels'

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True, null=False)
    type = models.ForeignKey(HealthFacilityType, blank=True, null=True)
    # Catchment areas should be locations that makes sense independently, i.e.
    # a city, town, village, parish, region, district, etc.
    catchment_areas = models.ManyToManyField(Location, null=True, blank=True)
    # location is the physical location of the health facility itself.
    # This location should only represent the facility's location, and
    # shouldn't be overloaded to also represent the location of a town
    # or village.  Depending on pending changes to the locations model,
    # this could eventually be a ForeignKey to the Point class instead.
    location = models.ForeignKey(Point, null=True, blank=True)
    # report_to generic relation.
    report_to_type = models.ForeignKey(ContentType, null=True, blank=True)
    report_to_id = models.PositiveIntegerField(null=True, blank=True)
    report_to = generic.GenericForeignKey('report_to_type', 'report_to_id')
    district = models.TextField(blank=True, null=True, default='')
    owner = models.TextField(null=True, blank=True, default='', choices=OWNERS)
    authority = models.TextField(null=True, blank=True, default='', choices=AUTHORITIES)
    last_reporting_date = models.DateField(null=True) #latest submission date
    uuid = models.CharField(max_length=100, blank=True, unique=True, null=True)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s" % (self.name, self.type or '')


    def clean(self, *args, **kwargs):

        if settings.CASCADE_UPDATE_TO_FRED:
            if self.id:
                cascade_update_succedded = FredFacilitiesFetcher.send_facility_update(self)
                if not cascade_update_succedded:
                    raise ValidationError('Cascade update failed')
            elif self.uuid in [None, ""]:
                self.uuid = FredFacilitiesFetcher.create_facility(self)
                if not self.uuid:
                    raise ValidationError('Cascade update failed')

    def save(self, cascade_update = True, *args,  **kwargs):

        if cascade_update:
            self.clean(*args, **kwargs)

        if not self.code:
            # generation is dumb now and not conflict-safe
            # probably suffiscient to handle human entry through django-admin
            chars = '1234567890_QWERTYUOPASDFGHJKLZXCVBNM'
            self.code = u"gen" + u"".join([choice(chars) \
                                          for i in range(10)]).lower()

        super(HealthFacilityBase, self).save(*args, **kwargs)

    @classmethod
    def store_json(self, json, comment, cascade_update = False):
        facility = HealthFacilityBase.objects.get_or_create(uuid = json['uuid'])[0]
        fred_facility_details = FredFacilityDetail.objects.get_or_create(uuid = json['uuid'])[0]
        facility.name = json['name']
        facility.active = json['active']
        if  json['properties'].has_key('type'):
            facility_type = json['properties']['type']
            facility.type = HealthFacilityType.objects.get_or_create(name=facility_type, slug=slugify(facility_type))[0]
        if  json['properties'].has_key('ownership'):
            facility.owner = json['properties']['ownership']
        if json['properties'].has_key('dataSets'):
            h033b = settings.FRED_H033B_INDICATOR in json['properties']['dataSets']
        else:
            h033b = False
        fred_facility_details.h033b = h033b
        fred_facility_details.save()
        with reversion.create_revision():
            facility.save(cascade_update = cascade_update)
            reversion.set_comment(comment)
        return facility


reversion.register(HealthFacilityBase)

class HealthFacility(HealthFacilityBase):
    __metaclass__ = ExtensibleModelBase

    class Meta:
        app_label = 'healthmodels'
        verbose_name = _("Health Facility")
        verbose_name_plural = _("Health Facilities")
    def is_root(self):
        if self.report_to == None:
            return True
        else:
            return False
    def get_children(self):

            children = HealthFacility.objects.filter(report_to_id=self.pk)
            if len(children) > 0:
                return children
            else:
                return False
    def is_child_node(self):
        children = HealthFacility.objects.filter(report_to_id=self.pk)
        if len(children > 0):
            return False
        else:
            return True

class FredFacilityDetail(models.Model):
    uuid = models.CharField(max_length=100, blank=False, unique=True, null=False)
    h033b = models.BooleanField(default=True)

    class Meta:
        app_label = 'healthmodels'