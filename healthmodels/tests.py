from django.test import TestCase
from django.core import management
from healthmodels.models.HealthFacility import *
from django.db import IntegrityError
from mock import *
from django.conf import settings

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

  if settings.CASCADE_UPDATE_TO_DHIS2:
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
