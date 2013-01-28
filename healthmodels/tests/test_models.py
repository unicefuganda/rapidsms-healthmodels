from django.test import TestCase
from django.core import management
from healthmodels.models.HealthFacility import *
from django.db import IntegrityError

class TestHealthFacilityBase(TestCase):

  def test_storage(self):
    facility = HealthFacilityBase.objects.create(name="Dummy")
    self.failUnless(facility.id)

  def test_uuid_field(self):
    facility = HealthFacilityBase.objects.create(name="Dummy", uuid="uuid")
    self.failUnless(facility.id)

    new_facility = HealthFacilityBase(name="Dummy 1", uuid="uuid")
    self.failUnlessRaises(IntegrityError, new_facility.save)