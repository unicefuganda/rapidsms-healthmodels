from healthmodels.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from healthmodels.models.HealthFacility import HealthFacility
from healthmodels.models.HealthProvider import HealthProvider
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect,HttpResponse
from healthmodels.views.forms import *
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings

def facility_index(request,template_name="healthmodels/facility_index.html"):
    healthfacilities=HealthFacility.objects.all()
    return render_to_response(template_name,
        {'healthfacilities':healthfacilities,
         'map_key':settings.MAP_KEY,}, context_instance=RequestContext(request))
    
def new_facility(request,parent,template_name="healthmodels/new_facility.html"):
    facility_form=HealthFacilityForm()
    health_providers=HealthProvider.objects.all()
    health_provider_form=HealthProviderForm()
    report_to_form=ReportToForm({'report_to':parent})
    point_form=PointForm()
    return render_to_response(template_name,{'point_form':point_form,'facility_form':facility_form,'health_provider_form':health_provider_form,'report_to_form':report_to_form}, context_instance=RequestContext(request))

def edit_facility(request,pk,template_name="healthmodels/edit_facility.html"):
    facility=HealthFacility.objects.get(pk=pk)
    parent=facility.report_to_id
    point=facility.location
    facility_form=HealthFacilityForm(instance=facility)
    health_provider_form=HealthProviderForm(initial={'providers':HealthProvider.objects.filter(facility=facility).values_list('id',flat=True)})
    point_form=PointForm(instance=point)
    report_to_form=ReportToForm({'report_to':parent})
    return render_to_response(template_name,{'point_form':point_form,'facility_form':facility_form,'health_provider_form':health_provider_form,'report_to_form':report_to_form,'pk':pk}, context_instance=RequestContext(request))
    
def update_facility(request,pk,template_name="healthmodels/partials/edit_facility.html"):

    if request.method=='POST':
        facility=HealthFacility.objects.get(pk=pk)
        facility_form=HealthFacilityForm(request.POST,instance=facility)
        report_to_form=ReportToForm(request.POST)
        point_form=PointForm(request.POST,instance=facility.location)
        health_provider_form=HealthProviderForm(request.POST)
        report_to_form=ReportToForm(request.POST)
        if facility_form.is_valid() and point_form.is_valid() and report_to_form.is_valid() and health_provider_form.is_valid():
            facility=facility_form.save(commit=False)
            location=point_form.save()
            facility.location=location
            report_to=get_object_or_404(HealthFacility,pk=report_to_form.cleaned_data['report_to'])
            catchment_areas=facility_form.cleaned_data['catchment_areas']
            facility.catchment_areas=catchment_areas
            facility.report_to=report_to
            facility.save()
            providers=health_provider_form.cleaned_data['providers']
            existing_providers=HealthProvider.objects.filter(facility=facility)

            if len(providers)!=0:
                for provider in providers :
                    if provider not in existing_providers:
                        provider.facility=facility
                        provider.save()
            if len(existing_providers)!=0:
                for provider in existing_providers:
                    if provider not in providers:
                        provider.facility=None

        else:
            return render_to_response("healthmodels/edit_facility.html",{'point_form':point_form,'facility_form':facility_form,'health_provider_form':health_provider_form,'report_to_form':report_to_form,'pk':pk}, context_instance=RequestContext(request))
        return HttpResponseRedirect("/healthfacility/1/new")

    
def destroy_facility(request,pk):
    facility = get_object_or_404(HealthFacility, pk=pk)
    facility_health_providers=HealthProvider.objects.filter(facility=facility)
    for provider in facility_health_providers:
        provider.facility=None
    facility.delete()
    return HttpResponseRedirect('/healthfacility/render_tree/')
    

def create_facility(request):
    health_provider_form=HealthProviderForm(request.POST)
    report_to_form=ReportToForm(request.POST)
    facility_form=HealthFacilityForm(request.POST)
    point_form=PointForm(request.POST)
    if facility_form.is_valid() and point_form.is_valid() and report_to_form.is_valid() and health_provider_form.is_valid():
            facility=facility_form.save(commit=False)
            location=point_form.save()
            facility.location=location
            report_to=get_object_or_404(HealthFacility,pk=report_to_form.cleaned_data['report_to'])
            facility.report_to=report_to
            facility.save()
            catchment_areas=facility_form.cleaned_data['catchment_areas']
            facility.catchment_areas=catchment_areas
            facility.save()
            providers=health_provider_form.cleaned_data['providers']
            if len(providers)!=0:
                for provider in providers:
                    provider.facility=facility
                    provider.save()

    else:
        return render_to_response("healthmodels/new_facility.html",{'point_form':point_form,'facility_form':facility_form,'health_provider_form':health_provider_form,'report_to_form':report_to_form}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/healthfacility/1/new")


    
@cache_control(no_cache=True)
def render_facilities(request,template_name="healthmodels/partials/_render_facilities_tree.html"):
    healthfacilities=HealthFacility.objects.all()
    return render_to_response(template_name,{'healthfacilities':healthfacilities}, context_instance=RequestContext(request))
