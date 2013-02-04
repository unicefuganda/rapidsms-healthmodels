# -*- coding: utf-8 -*-
from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals
from splinter import Browser
from lettuce.django import django_url
from time import sleep
from random import randint
from datetime import datetime
from healthmodels.models.HealthFacility import *
import time, reversion

@before.all
def set_browser():
  world.browser = Browser()

@after.all
def close_browser(*args):
  world.browser.quit()

def visit(url):
  world.browser.visit(django_url(url))

@step(u'Given I am logged in as admin')
def log_in(step):
  visit("/account/login/")
  world.browser.fill("username", "smoke")
  world.browser.fill("password", "password")
  world.browser.find_by_css('input[type=submit]').first.click()
  visit("/admin/")

@step(u'And I edit a HealthFacility')
def and_i_edit_a_healthfacility(step):
  facility = HealthFacilityBase.objects.filter(name="Kochi")[0]
  version_list = reversion.get_for_object(facility)
  version_list.delete()
  uuid = str(randint(1,9999))
  visit("/admin/healthmodels/healthfacility")
  world.browser.click_link_by_text("Kochi hciii")
  world.browser.fill("uuid", uuid)
  world.browser.find_by_css('input[name=_save]').first.click()
  world.browser.click_link_by_text("Kochi hciii")
  assert world.browser.find_by_css('input[name=uuid]').first.value == uuid

@step(u'Then I should see my changes are logged')
def then_i_should_see_my_changes_are_logged(step):
  facility = HealthFacilityBase.objects.filter(name="Kochi")[0]
  version_list = reversion.get_for_object(facility)
  assert len(version_list) > 0
  version = version_list[0]
  assert version.revision.comment == "Changed uuid."