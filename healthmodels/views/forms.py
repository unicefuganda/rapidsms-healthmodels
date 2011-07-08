from django import forms
from django.utils.safestring import mark_safe
from healthmodels.models import HealthFacility,HealthProvider
from rapidsms.contrib.locations.models import Point
    
class HealthFacilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HealthFacilityForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance',None)
        self.fields['catchment_areas'].widget.attrs ={'class':'narrow'}
        if instance:
            self.fields['catchment_areas'].initial =[c.pk for c in instance.catchment_areas.all()]



    class Meta:
        model=HealthFacility
        include=('name', 'code', 'type', 'location',  'catchment_areas', )

class ReportToForm(forms.Form):
    report_to=forms.ChoiceField(choices=(('',''),)+tuple([(int(p.pk),p.name) for p in HealthFacility.objects.all() ]),required=False)

class PointForm(forms.ModelForm):
    class Meta:
        model=Point

class HealthProviderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        facility = kwargs.get('facility',None)
        if facility:
            del kwargs['facility']
        super(HealthProviderForm,self).__init__(*args,**kwargs)
        self.fields['providers'] = forms.ModelMultipleChoiceField(queryset=HealthProvider.objects.all(),required=False)
        if facility:
             self.fields['providers'].queryset=HealthProvider.objects.filter(facility=facility)
        


