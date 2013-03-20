from django.test import TestCase
from django.core import management
from healthmodels.models.HealthFacility import *
from django.db import IntegrityError
from mock import *
from django.conf import settings
import json

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


  def test_storage_with_feature_turned_off(self):
      orig = settings.CASCADE_UPDATE_TO_DHIS2
      settings.CASCADE_UPDATE_TO_DHIS2 = False
      facility = HealthFacility(name="Dummy 1")
      facility.save()
      self.failUnless(facility.id)
      settings.CASCADE_UPDATE_TO_DHIS2 = orig

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
      facility_json = json.loads('{"facilities":[{"uuid":"6VeE8JrylXn","name":" BATMAN HC II","active":true,"href":"http:/example/6VeE8JrylXn","createdAt":"2012-08-14T10:00:07.701+0000","updatedAt":"2013-01-22T15:09:55.543+0000","coordinates":[2.2222,0.1111]}]}')['facilities'][0]

      facility = HealthFacility(name="Dummy", uuid=facility_json['uuid'], active = False)
      facility.save(cascade_update=False)
      self.failUnless(facility.id)

      assert facility.name == 'Dummy'
      assert facility.uuid == facility_json['uuid']
      assert facility.active == False

      HealthFacility.store_json(facility_json)
      facility = HealthFacility.objects.get(id=facility.id)

      assert facility.name == facility_json['name']
      assert facility.active == facility_json['active']
      assert facility.uuid == facility_json['uuid']


  def test_store_json_create(self):
      facility_json = json.loads('{"facilities":[{"uuid":"6VeE8JrylXn","name":" BATMAN HC II","active":true,"href":"http:/example/6VeE8JrylXn","createdAt":"2012-08-14T10:00:07.701+0000","updatedAt":"2013-01-22T15:09:55.543+0000","coordinates":[2.2222,0.1111]}]}')['facilities'][0]

      facility = HealthFacility.store_json(facility_json)
      self.failUnless(facility.id)

      facility = HealthFacilityBase.objects.get(id = facility.id)

      assert facility.name == facility_json['name']
      assert facility.active == facility_json['active']
      assert facility.uuid == facility_json['uuid']


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
