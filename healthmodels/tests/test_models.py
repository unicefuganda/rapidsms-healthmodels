from django.test import TestCase
from django.core import management
from healthmodels.models.HealthFacility import *
from django.db import IntegrityError
from mock import *
from django.db import models

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

  @patch('fred_consumer.fred_connect.FredFacilitiesFetcher.send_facility_update')
  def test_save(self, mock_send_facility_update):
      facility = HealthFacilityBase(name="Dummy")
      facility.save()
      assert mock_send_facility_update.called == True

  @patch('fred_consumer.fred_connect.FredFacilitiesFetcher.send_facility_update')
  def test_save_without_cascade_update(self, mock_send_facility_update):
      facility = HealthFacilityBase(name="Dummy")
      facility.save(cascade_update=False)
      assert mock_send_facility_update.called == False

  @patch('django.db.models.Model.save')
  def test_unsuccesful_cascade_update_do_not_save(self, mock_save):
      facility = HealthFacilityBase(name="Dummy")
      FredFacilitiesFetcher.send_facility_update = MagicMock(return_value = False)
      facility.save(cascade_update=True)
      assert mock_save.called == False
