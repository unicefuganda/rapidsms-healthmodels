from django.test import TestCase
from django.core import management
from healthmodels.models.HealthFacility import *
from django.db import IntegrityError
from mock import *
from django.conf import settings
import json
from django.template.defaultfilters import slugify

class TestHealthFacilityBase(TestCase):

  def test_storage(self):
    facility = HealthFacilityBase(name="Dummy")
    facility.save(cascade_update=False)
    self.failUnless(facility.id)

  def test_uuid_field(self):
    facility = HealthFacilityBase(name="Dummy", uuid="uuid")
    facility.save(cascade_update=False)
    self.failUnless(facility.id)

    new_facility = HealthFacilityBase(name="Dummy 1", uuid="uuid")
    self.failUnlessRaises(IntegrityError, new_facility.save, cascade_update=False)


  def test_active_field(self):
      facility = HealthFacilityBase(name="Dummy")
      facility.save(cascade_update = False)
      self.failUnless(facility.id)

      assert facility.active == True

      new_facility = HealthFacilityBase(name="Dummy", active = False)
      new_facility.save(cascade_update=False)
      self.failUnless(new_facility.id)

      assert new_facility.active == False

  def test_deleted_field(self):
        facility = HealthFacilityBase(name="Dummy")
        facility.save(cascade_update = False)
        self.failUnless(facility.id)

        assert facility.deleted == False

        new_facility = HealthFacilityBase(name="Dummy", deleted = True)
        new_facility.save(cascade_update=False)
        self.failUnless(new_facility.id)

        assert new_facility.deleted == True


  def test_storage_with_feature_turned_off(self):
      orig = settings.CASCADE_UPDATE_TO_FRED
      settings.CASCADE_UPDATE_TO_FRED = False
      facility = HealthFacility(name="Dummy 1")
      facility.save()
      self.failUnless(facility.id)
      settings.CASCADE_UPDATE_TO_FRED = orig

  def test_create_facility_without_cascading(self):
      facility = HealthFacility(name="Dummy 1")
      facility.save(cascade_update=False)
      self.failUnless(facility.id)
      self.failIf(facility.uuid)

      facility = HealthFacility(name="Dummy 2")
      facility.save()
      self.failUnless(facility.id)
      self.failIf(facility.uuid)

  def test_store_json_update(self):
      facility_json = json.loads('{  "uuid": "18a021ed-205c-4e80-ab9c-fbeb2d9c1bcf",  "name": "Some HOSPITAL",  "active": true,  "href": "http://dhis/api-fred/v1/facilities/123",  "createdAt": "2013-01-15T11:14:02.863+0000",  "updatedAt": "2013-01-15T11:14:02.863+0000",  "coordinates": [34.19622, 0.70331],  "identifiers": [{    "agency": "DHIS2",    "context": "DHIS2_UID",    "id": "123"  }],  "properties": {    "dataSets": ["123456"],    "level": 5,    "ownership": "Private Not For Profit",    "parent": "56789",    "type": "General Hospital"  }}')

      facility_json['name'] = facility_json['name'].encode('utf-8')

      facility = HealthFacility(name="Dummy", uuid=facility_json['uuid'], active = False)
      facility.save(cascade_update=False)
      self.failUnless(facility.id)

      assert facility.name == 'Dummy'
      assert facility.uuid == facility_json['uuid']
      assert facility.active == False

      HealthFacility.store_json(facility_json, comment = "Updates from FRED provider")
      facility = HealthFacility.objects.get(id=facility.id)

      assert facility.name == facility_json['name']
      assert facility.active == facility_json['active']
      assert facility.uuid == facility_json['uuid']
      assert facility.type.name == facility_json["properties"]["type"]
      assert facility.type.slug == "generalhospital"
      assert facility.owner == facility_json['properties']['ownership']


  def test_store_json_create(self):
      facility_json = json.loads('{  "uuid": "18a021ed-205c-4e80-ab9c-fbeb2d9c1bcf",  "name": "Some HOSPITAL",  "active": true,  "href": "http://dhis/api-fred/v1/facilities/123",  "createdAt": "2013-01-15T11:14:02.863+0000",  "updatedAt": "2013-01-15T11:14:02.863+0000",  "coordinates": [34.19622, 0.70331],  "identifiers": [{    "agency": "DHIS2",    "context": "DHIS2_UID",    "id": "123"  }],  "properties": {    "dataSets": ["123456"],    "level": 5,    "ownership": "Private Not For Profit",    "parent": "56789",    "type": "General Hospital"  }}')

      facility_json['name'] = facility_json['name'].encode('utf-8')

      facility = HealthFacility.store_json(facility_json, comment = "Updates from FRED provider")
      self.failUnless(facility.id)

      facility = HealthFacilityBase.objects.get(id = facility.id)

      assert facility.name == facility_json['name']
      assert facility.active == facility_json['active']
      assert facility.uuid == facility_json['uuid']
      assert facility.type.name == facility_json["properties"]["type"]
      assert facility.type.slug == "generalhospital"
      assert facility.owner == facility_json['properties']['ownership']

      fred_facility_details = FredFacilityDetail.objects.get(uuid=facility_json['uuid'])
      assert fred_facility_details.h033b == False

  def test_store_json_create_failsafe(self):
      facility_json = json.loads('{  "uuid": "18a021ed-205c-4e80-ab9c-fbeb2d9c1bcf",  "name": "Some HOSPITAL",  "active": true,  "href": "http://dhis/api-fred/v1/facilities/123",  "createdAt": "2013-01-15T11:14:02.863+0000",  "updatedAt": "2013-01-15T11:14:02.863+0000",  "coordinates": [34.19622, 0.70331],  "identifiers": [{    "agency": "DHIS2",    "context": "DHIS2_UID",    "id": "123"  }],  "properties": {    "dataSets": ["123456"],    "level": 5,    "parent": "56789"  }}')

      facility_json['name'] = facility_json['name'].encode('utf-8')

      facility = HealthFacility.store_json(facility_json, comment = "Updates from FRED provider")
      self.failUnless(facility.id)

      facility = HealthFacilityBase.objects.get(id = facility.id)

      assert facility.name == facility_json['name']
      assert facility.active == facility_json['active']
      assert facility.uuid == facility_json['uuid']
      assert facility.type == None
      assert facility.owner == ''
      fred_facility_details = FredFacilityDetail.objects.get(uuid=facility_json['uuid'])
      assert fred_facility_details.h033b == False

  def test_store_json_h033b_indicator(self):
    facility_json = json.loads('{  "uuid": "18a021ed-205c-4e80-ab9c-fbeb2d9c1bcf",  "name": "Some HOSPITAL",  "active": true,  "href": "http://dhis/api-fred/v1/facilities/123",  "createdAt": "2013-01-15T11:14:02.863+0000",  "updatedAt": "2013-01-15T11:14:02.863+0000",  "coordinates": [34.19622, 0.70331],  "identifiers": [{    "agency": "DHIS2",    "context": "DHIS2_UID",    "id": "123"  }],  "properties": {    "dataSets": ["V1kJRs8CtW4"],    "level": 5,    "parent": "56789"  }}')
    facility_json['name'] = facility_json['name'].encode('utf-8')

    facility = HealthFacility.store_json(facility_json, comment = "Updates from FRED provider")
    self.failUnless(facility.id)

    facility = HealthFacilityBase.objects.get(id = facility.id)

    fred_facility_details = FredFacilityDetail.objects.get(uuid=facility_json['uuid'])
    assert fred_facility_details.h033b == True

    facility_json['properties']['dataSets'] = []
    facility = HealthFacility.store_json(facility_json, comment = "Updates from FRED provider")
    fred_facility_details = FredFacilityDetail.objects.get(uuid=facility_json['uuid'])
    assert fred_facility_details.h033b == False


  if settings.CASCADE_UPDATE_TO_FRED:
    @patch('fred_consumer.fred_connect.FredFacilitiesFetcher.send_facility_update')
    def test_save(self, mock_send_facility_update):
        facility = HealthFacilityBase(name="Dummy")
        facility.save(cascade_update=False)
        facility.name = "changed name"
        facility.save()
        assert mock_send_facility_update.called == True

    @patch('fred_consumer.fred_connect.FredFacilitiesFetcher.send_facility_update')
    def test_save_without_cascade_update(self, mock_send_facility_update):
        facility = HealthFacilityBase(name="Dummy")
        facility.save(cascade_update=False)
        assert mock_send_facility_update.called == False

    @patch('fred_consumer.fred_connect.FredFacilitiesFetcher.send_facility_update')
    def test_unsuccesful_cascade_update_do_not_save(self, mock_send_facility_update):
        mock_send_facility_update.return_value = False
        facility = HealthFacilityBase(name="Dummy")
        facility.save(cascade_update=False)
        self.failUnless(facility.id)
        facility.name = "changed name"
        self.failUnlessRaises(ValidationError, facility.save, cascade_update=True)
        facility = HealthFacilityBase.objects.get(id=facility.id)
        assert facility.name == "Dummy"


    @patch('fred_consumer.fred_connect.FredFacilitiesFetcher.create_facility')
    def test_create_facility_without_cascading(self, mock_create_facility):
        mock_create_facility.return_value = "randomuuid"
        facility = HealthFacility(name="Dummy 1")
        facility.save()
        assert mock_create_facility.called == True
        self.failUnless(facility.id)
        assert facility.uuid == "randomuuid"

    @patch('fred_consumer.fred_connect.FredFacilitiesFetcher.create_facility')
    def test_create_facility_without_cascading_with_empty_uuid(self, mock_create_facility):
        mock_create_facility.return_value = "randomuuid"
        facility = HealthFacility(name="Dummy 1", uuid="")
        facility.save()
        assert mock_create_facility.called == True
        self.failUnless(facility.id)
        assert facility.uuid == "randomuuid"

    @patch('fred_consumer.fred_connect.FredFacilitiesFetcher.create_facility')
    def test_create_facility_without_double_cascading(self, mock_create_facility):
        facility = HealthFacility(name="Dummy 1", uuid="randomuuid")
        facility.save()
        assert mock_create_facility.called == False
        self.failUnless(facility.id)
        assert facility.uuid == "randomuuid"


    @patch('fred_consumer.fred_connect.FredFacilitiesFetcher.create_facility')
    def test_create_facility_with_cascading_and_raise_exception(self, mock_create_facility):
        mock_create_facility.return_value = None
        facility = HealthFacility(name="Dummy 1")
        self.failUnlessRaises(ValidationError, facility.save)
        assert mock_create_facility.called == True
        self.failIf(facility.id)
        self.failIf(facility.uuid)

class TestFredFacilityDetail(TestCase):

    def test_storage(self):
        facility = HealthFacility(name="Dummy 1", uuid="randomuuid")
        fred_facility_details = FredFacilityDetail(uuid=facility, h033b=True)
        fred_facility_details.save()
        self.failUnless(fred_facility_details.id)

    def test_uuid_field(self):
        facility = HealthFacility(name="Dummy 1", uuid="randomuuid")
        fred_facility_details = FredFacilityDetail(uuid=facility, h033b=True)
        fred_facility_details.save()

        new_fred_facility_details = FredFacilityDetail(uuid=facility, h033b=False)
        self.failUnlessRaises(IntegrityError, new_fred_facility_details.save)