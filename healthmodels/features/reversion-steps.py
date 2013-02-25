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
from fred_consumer.fred_connect import FredFacilitiesFetcher

FRED_CONFIG = {"url": "http://dhis/api-fred/v1///", "username": "api", "password": "P@ssw0rd"}

NO_OF_EXISTING_FAILURE = len(Failure.objects.all())
RANDOM_FACILTY_NAME = "TW"+ str(randint(1,9999))

@transaction.commit_on_success
def create_facility(f):
    f.save(False)
    return f

@before.each_scenario
def set_browser(scenario):
  world.browser = Browser()
  FredConfig.store_fred_configs(FRED_CONFIG)
  world.uuid = None

def destroy_data_with_uuid(uuid):
    facilities = HealthFacility.objects.filter(uuid=uuid).all()
    if facilities:
        facilities.delete()
    maps = HealthFacilityIdMap.objects.filter(uuid=uuid).all()
    if maps:
        maps.delete()

@after.each_scenario
def close_browser_and_clean_data(scenario):
  visit("/admin/logout/")
  world.browser.quit()
  if world.uuid:
      destroy_data_with_uuid(world.uuid)

def visit(url):
  world.browser.visit(django_url(url))

@step(u'Given I am logged in as admin')
def log_in(step):
  visit("/account/login/")
  world.browser.fill("username", "smoke")
  world.browser.fill("password", "password")
  world.browser.find_by_css('input[type=submit]').first.click()
  visit("/admin/")

@step(u'When I edit a Facility with invalid values')
def edit_a_facility_with_invalid_values(step):
    visit("/admin/healthmodels/healthfacility")
    world.browser.is_text_present("ThoughtWorks facility ", wait_time=3)
    world.browser.click_link_by_text("ThoughtWorks facility ")
    assert world.browser.is_element_present_by_name("name", wait_time=3)
    world.browser.fill("name", " ")
    world.browser.click_link_by_text("Today")

@step(u'When I edit a HealthFacility')
def edit_a_healthfacility(step):
    visit("/admin/healthmodels/healthfacility")
    world.browser.is_text_present("ThoughtWorks facility ", wait_time=3)
    world.browser.click_link_by_text("ThoughtWorks facility ")
    assert world.browser.is_element_present_by_name("name", wait_time=3)
    world.browser.fill("name", RANDOM_FACILTY_NAME)
    world.browser.click_link_by_text("Today")

@step(u'And I attempt to save')
def edit_a_healthfacility(step):
    world.browser.find_by_css('input[name=_save]').first.click()

@step(u'Then I should see my facility changes are made')
def edit_a_healthfacility(step):
    world.browser.is_text_present(RANDOM_FACILTY_NAME, wait_time=3)
    world.browser.click_link_by_text(RANDOM_FACILTY_NAME + " ")
    assert world.browser.find_by_css('input[name=name]').first.value == RANDOM_FACILTY_NAME

@step(u'Then I should see an error')
def should_see_an_error(step):
    world.uuid = world.browser.find_by_css('input[name=uuid]').first.value
    assert world.browser.find_by_css('.errorlist').text == 'Cascade update failed'

@step(u'And I should have a failure object created to report it')
def should_have_a_failure(step):
    assert len(Failure.objects.all()) == NO_OF_EXISTING_FAILURE + 1
    failure = Failure.objects.latest('time')
    assert ('HTTPError:{"name":"length must be between 2 and 160"}:http://dhis/api-fred/v1/facilities/' in failure.exception) == True
    failure_json = json.loads(failure.json)
    assert failure_json['name'] == " "
    assert failure_json['id'] == world.uuid

@step(u'And I should see my changes are logged')
def then_i_should_see_my_changes_are_logged(step):
  world.uuid = world.browser.find_by_css('input[name=uuid]').first.value
  facility = HealthFacility.objects.filter(uuid=world.uuid)[0]
  version_list = reversion.get_for_object(facility)
  assert len(version_list) > 0
  version = version_list[0]
  assert version.revision.comment == "Changed name."

@step(u'And I see my changes in fred provider')
def verify_changes_in_fred_provider(step):
    fetcher = FredFacilitiesFetcher(FRED_CONFIG)
    facility_in_fred = fetcher.get_facility(world.uuid)
    assert facility_in_fred['name'] == world.browser.find_by_css('input[name=name]').first.value

@step(u'And I create a new health facility')
def create_a_facility(step):
    visit("/admin/healthmodels/healthfacility/add/")
    world.browser.fill("name", "ThoughtWorks facility")
    world.browser.click_link_by_text("Today")
    world.browser.find_by_css('input[name=_save]').first.click()

@step(u'Then I should see my facility in fred provider')
def check_facility_in_provider(step):
    visit("/admin/healthmodels/healthfacility")
    world.browser.is_text_present("ThoughtWorks facility ", wait_time=3)
    world.browser.click_link_by_text("ThoughtWorks facility ")
    uuid = world.browser.find_by_css('input[name=uuid]').first.value
    fetcher = FredFacilitiesFetcher(FRED_CONFIG)
    facility_in_fred = fetcher.get_facility(uuid)
    assert facility_in_fred['name'] == world.browser.find_by_css('input[name=name]').first.value
    HealthFacilityIdMap.objects.get(uuid=uuid).delete()

