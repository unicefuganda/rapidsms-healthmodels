# -*- coding: utf-8 -*-
import json
from lettuce import *
from lxml import html
from random import randint
from nose.tools import assert_equals
from splinter import Browser
from lettuce.django import django_url
from healthmodels.models.HealthFacility import *
import reversion
from fred_consumer.models import FredConfig, HealthFacilityIdMap,Failure
from django.db import transaction

FRED_CONFIG = {"url": "http://dhis/api-fred/v1///", "username": "api", "password": "P@ssw0rd"}

NO_OF_EXISTING_FAILURE = len(Failure.objects.all())
CONFIG = {
    'test_facility_url'      : FRED_CONFIG['url'] + 'facilities/6VeE8JrylXn',
    'uuid'  :                  "234567"
}
RANDOM_FACILTY_NAME = "TW"+ str(randint(1,9999))

@transaction.commit_on_success
def create_facility(f):
    f.save(False)
    return f

@before.each_scenario
def set_browser(scenario):
  world.browser = Browser()
  FredConfig.store_fred_configs(FRED_CONFIG)

@after.each_scenario
def close_browser_and_clean_data(scenario):
  visit("/admin/logout/")
  world.browser.quit()
  if(scenario.name == "Changes to HealthFacility should be logged"):
      HealthFacilityIdMap.objects.get(uuid=CONFIG['uuid']).delete()
  HealthFacility.objects.get(uuid=CONFIG['uuid']).delete()

def visit(url):
  world.browser.visit(django_url(url))

@step(u'Given I am logged in as admin')
def log_in(step):
  visit("/account/login/")
  world.browser.fill("username", "smoke")
  world.browser.fill("password", "password")
  world.browser.find_by_css('input[type=submit]').first.click()
  visit("/admin/")

@step(u'And I have an existing facility with UID')
def have_existing_facility_with_uid(step):
    facility = HealthFacility(name="ThoughtWorks facility", uuid=CONFIG['uuid'])
    create_facility(facility)
    HealthFacilityIdMap.objects.create(url= CONFIG['test_facility_url'], uuid=CONFIG['uuid'])

@step(u'And I dont have an existing facility with UID')
def dont_have_existing_facility_with_uid(step):
    facility = HealthFacility(name="ThoughtWorks facility", uuid=CONFIG['uuid'])
    create_facility(facility)

@step(u'When I edit a HealthFacility')
def edit_a_healthfacility(step):
    visit("/admin/healthmodels/healthfacility")
    world.browser.click_link_by_text("ThoughtWorks facility ")
    world.browser.fill("name", RANDOM_FACILTY_NAME)
    world.browser.click_link_by_text("Today")


@step(u'And I attempt to save')
def edit_a_healthfacility(step):
    world.browser.find_by_css('input[name=_save]').first.click()

@step(u'Then I should see my facility changes are made')
def edit_a_healthfacility(step):
    world.browser.click_link_by_text(RANDOM_FACILTY_NAME + " ")
    assert world.browser.find_by_css('input[name=name]').first.value == RANDOM_FACILTY_NAME

@step(u'Then I should see an error')
def should_see_an_error(step):
    assert world.browser.find_by_css('.errorlist').text == 'Cascade update failed'

@step(u'And I should have a failure object created to report it')
def should_have_a_failure(step):
    assert len(Failure.objects.all()) == NO_OF_EXISTING_FAILURE + 1
    failure = Failure.objects.latest('time')

    assert failure.exception == "DoesNotExist:HealthFacilityIdMap matching query does not exist."
    assert failure.json == json.dumps({"name": RANDOM_FACILTY_NAME, "uuid": CONFIG['uuid']})

@step(u'And I should see my changes are logged')
def then_i_should_see_my_changes_are_logged(step):
  facility = HealthFacility.objects.filter(uuid=CONFIG['uuid'])[0]
  version_list = reversion.get_for_object(facility)
  assert len(version_list) > 0
  version = version_list[0]
  assert version.revision.comment == "Changed name and last_reporting_date."