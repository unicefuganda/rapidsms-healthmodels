from django.conf.urls.defaults import *
from healthmodels.views.health_management import *
urlpatterns = patterns('',
 url(r'^healthfacility/index/$', facility_index ,name="health_management"),
 url(r'^healthfacility/(?P<parent>\d+)/new/$', new_facility ),
 url(r'^healthfacility/(?P<pk>\d+)/delete/$', destroy_facility ),
 url(r'^healthfacility/(?P<pk>\d+)/edit/$', edit_facility ),
 url(r'^healthfacility/(?P<pk>\d+)/update/$', update_facility ),
 url(r'^healthfacility/create/$', create_facility ),
 url(r'^healthfacility/render_tree/$', render_facilities ),
)
