# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'HealthIdBase'
        db.create_table('healthmodels_healthidbase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('health_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('generated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('printed_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('issued_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('revoked_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('issued_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthmodels.Patient'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='G', max_length=1)),
        ))
        db.send_create_signal('healthmodels', ['HealthIdBase'])

        # Adding model 'HealthId'
        db.create_table('healthmodels_healthid', (
            ('healthidbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['healthmodels.HealthIdBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('healthmodels', ['HealthId'])

        # Adding model 'HealthFacilityTypeBase'
        db.create_table('healthmodels_healthfacilitytypebase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('healthmodels', ['HealthFacilityTypeBase'])

        # Adding model 'HealthFacilityType'
        db.create_table('healthmodels_healthfacilitytype', (
            ('healthfacilitytypebase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['healthmodels.HealthFacilityTypeBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('healthmodels', ['HealthFacilityType'])

        # Adding model 'HealthFacilityBase'
        db.create_table('healthmodels_healthfacilitybase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthmodels.HealthFacilityType'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Point'], null=True, blank=True)),
            ('report_to_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('report_to_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('healthmodels', ['HealthFacilityBase'])

        # Adding M2M table for field catchment_areas on 'HealthFacilityBase'
        db.create_table('healthmodels_healthfacilitybase_catchment_areas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('healthfacilitybase', models.ForeignKey(orm['healthmodels.healthfacilitybase'], null=False)),
            ('location', models.ForeignKey(orm['locations.location'], null=False))
        ))
        db.create_unique('healthmodels_healthfacilitybase_catchment_areas', ['healthfacilitybase_id', 'location_id'])

        # Adding model 'HealthFacility'
        db.create_table('healthmodels_healthfacility', (
            ('healthfacilitybase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['healthmodels.HealthFacilityBase'], unique=True, primary_key=True)),
            ('supply_point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.SupplyPoint'], null=True, blank=True)),
        ))
        db.send_create_signal('healthmodels', ['HealthFacility'])

        # Adding model 'HealthProviderBase'
        db.create_table('healthmodels_healthproviderbase', (
            ('contact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['rapidsms.Contact'], unique=True, primary_key=True)),
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthmodels.HealthFacility'], null=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'], null=True)),
        ))
        db.send_create_signal('healthmodels', ['HealthProviderBase'])

        # Adding model 'HealthProvider'
        db.create_table('healthmodels_healthprovider', (
            ('healthproviderbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['healthmodels.HealthProviderBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('healthmodels', ['HealthProvider'])

        # Adding model 'PatientBase'
        db.create_table('healthmodels_patientbase', (
            ('health_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthmodels.HealthId'], unique=True, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('estimated_birthdate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deathdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('health_worker', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='patients', null=True, to=orm['healthmodels.HealthProvider'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'], null=True, blank=True)),
            ('health_facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthmodels.HealthFacility'], null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rapidsms.Contact'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
        ))
        db.send_create_signal('healthmodels', ['PatientBase'])

        # Adding model 'Patient'
        db.create_table('healthmodels_patient', (
            ('patientbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['healthmodels.PatientBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('healthmodels', ['Patient'])

        # Adding model 'PatientEncounterBase'
        db.create_table('healthmodels_patientencounterbase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthmodels.Patient'])),
        ))
        db.send_create_signal('healthmodels', ['PatientEncounterBase'])

        # Adding model 'PatientEncounter'
        db.create_table('healthmodels_patientencounter', (
            ('patientencounterbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['healthmodels.PatientEncounterBase'], unique=True, primary_key=True)),
            ('submission', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='report', unique=True, null=True, to=orm['rapidsms_xforms.XFormSubmission'])),
            ('reporter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthmodels.HealthProvider'], null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rapidsms_httprouter.Message'], null=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('healthmodels', ['PatientEncounter'])

        # Adding model 'FacilityReportBase'
        db.create_table('healthmodels_facilityreportbase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthmodels.HealthFacility'])),
        ))
        db.send_create_signal('healthmodels', ['FacilityReportBase'])

        # Adding model 'FacilityReport'
        db.create_table('healthmodels_facilityreport', (
            ('facilityreportbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['healthmodels.FacilityReportBase'], unique=True, primary_key=True)),
            ('submission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rapidsms_xforms.XFormSubmission'], null=True, blank=True)),
            ('reporter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthmodels.HealthProvider'], null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rapidsms_httprouter.Message'], null=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('healthmodels', ['FacilityReport'])


    def backwards(self, orm):
        
        # Deleting model 'HealthIdBase'
        db.delete_table('healthmodels_healthidbase')

        # Deleting model 'HealthId'
        db.delete_table('healthmodels_healthid')

        # Deleting model 'HealthFacilityTypeBase'
        db.delete_table('healthmodels_healthfacilitytypebase')

        # Deleting model 'HealthFacilityType'
        db.delete_table('healthmodels_healthfacilitytype')

        # Deleting model 'HealthFacilityBase'
        db.delete_table('healthmodels_healthfacilitybase')

        # Removing M2M table for field catchment_areas on 'HealthFacilityBase'
        db.delete_table('healthmodels_healthfacilitybase_catchment_areas')

        # Deleting model 'HealthFacility'
        db.delete_table('healthmodels_healthfacility')

        # Deleting model 'HealthProviderBase'
        db.delete_table('healthmodels_healthproviderbase')

        # Deleting model 'HealthProvider'
        db.delete_table('healthmodels_healthprovider')

        # Deleting model 'PatientBase'
        db.delete_table('healthmodels_patientbase')

        # Deleting model 'Patient'
        db.delete_table('healthmodels_patient')

        # Deleting model 'PatientEncounterBase'
        db.delete_table('healthmodels_patientencounterbase')

        # Deleting model 'PatientEncounter'
        db.delete_table('healthmodels_patientencounter')

        # Deleting model 'FacilityReportBase'
        db.delete_table('healthmodels_facilityreportbase')

        # Deleting model 'FacilityReport'
        db.delete_table('healthmodels_facilityreport')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'eav.attribute': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('site', 'slug'),)", 'object_name': 'Attribute'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'datatype': ('eav.fields.EavDatatypeField', [], {'max_length': '6'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'enum_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eav.EnumGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('eav.fields.EavSlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'eav.enumgroup': {
            'Meta': {'object_name': 'EnumGroup'},
            'enums': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eav.EnumValue']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'eav.enumvalue': {
            'Meta': {'object_name': 'EnumValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'eav.value': {
            'Meta': {'object_name': 'Value'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eav.Attribute']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'entity_ct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value_entities'", 'to': "orm['contenttypes.ContentType']"}),
            'entity_id': ('django.db.models.fields.IntegerField', [], {}),
            'generic_value_ct': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'value_values'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'generic_value_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value_bool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'value_enum': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'eav_values'", 'null': 'True', 'to': "orm['eav.EnumValue']"}),
            'value_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_int': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'healthmodels.facilityreport': {
            'Meta': {'object_name': 'FacilityReport', '_ormbases': ['healthmodels.FacilityReportBase']},
            'facilityreportbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.FacilityReportBase']", 'unique': 'True', 'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms_httprouter.Message']", 'null': 'True', 'blank': 'True'}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.HealthProvider']", 'null': 'True', 'blank': 'True'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms_xforms.XFormSubmission']", 'null': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'healthmodels.facilityreportbase': {
            'Meta': {'object_name': 'FacilityReportBase'},
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.HealthFacility']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'healthmodels.healthfacility': {
            'Meta': {'object_name': 'HealthFacility', '_ormbases': ['healthmodels.HealthFacilityBase']},
            'healthfacilitybase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.HealthFacilityBase']", 'unique': 'True', 'primary_key': 'True'}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']", 'null': 'True', 'blank': 'True'})
        },
        'healthmodels.healthfacilitybase': {
            'Meta': {'object_name': 'HealthFacilityBase'},
            'catchment_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Point']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'report_to_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'report_to_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.HealthFacilityType']", 'null': 'True', 'blank': 'True'})
        },
        'healthmodels.healthfacilitytype': {
            'Meta': {'object_name': 'HealthFacilityType', '_ormbases': ['healthmodels.HealthFacilityTypeBase']},
            'healthfacilitytypebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.HealthFacilityTypeBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'healthmodels.healthfacilitytypebase': {
            'Meta': {'object_name': 'HealthFacilityTypeBase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'healthmodels.healthid': {
            'Meta': {'object_name': 'HealthId', '_ormbases': ['healthmodels.HealthIdBase']},
            'healthidbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.HealthIdBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'healthmodels.healthidbase': {
            'Meta': {'object_name': 'HealthIdBase'},
            'generated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'health_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'issued_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.Patient']", 'null': 'True', 'blank': 'True'}),
            'printed_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'revoked_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'G'", 'max_length': '1'})
        },
        'healthmodels.healthprovider': {
            'Meta': {'object_name': 'HealthProvider', '_ormbases': ['healthmodels.HealthProviderBase']},
            'healthproviderbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.HealthProviderBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'healthmodels.healthproviderbase': {
            'Meta': {'object_name': 'HealthProviderBase', '_ormbases': ['rapidsms.Contact']},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['rapidsms.Contact']", 'unique': 'True', 'primary_key': 'True'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.HealthFacility']", 'null': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']", 'null': 'True'})
        },
        'healthmodels.patient': {
            'Meta': {'object_name': 'Patient', '_ormbases': ['healthmodels.PatientBase']},
            'patientbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.PatientBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'healthmodels.patientbase': {
            'Meta': {'object_name': 'PatientBase'},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Contact']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deathdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'estimated_birthdate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'health_facility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.HealthFacility']", 'null': 'True', 'blank': 'True'}),
            'health_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.HealthId']", 'unique': 'True', 'primary_key': 'True'}),
            'health_worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'patients'", 'null': 'True', 'to': "orm['healthmodels.HealthProvider']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'healthmodels.patientencounter': {
            'Meta': {'object_name': 'PatientEncounter', '_ormbases': ['healthmodels.PatientEncounterBase']},
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms_httprouter.Message']", 'null': 'True', 'blank': 'True'}),
            'patientencounterbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.PatientEncounterBase']", 'unique': 'True', 'primary_key': 'True'}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.HealthProvider']", 'null': 'True', 'blank': 'True'}),
            'submission': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'report'", 'unique': 'True', 'null': 'True', 'to': "orm['rapidsms_xforms.XFormSubmission']"}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'healthmodels.patientencounterbase': {
            'Meta': {'object_name': 'PatientEncounterBase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.Patient']"})
        },
        'locations.location': {
            'Meta': {'object_name': 'Location'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Point']", 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'to': "orm['locations.LocationType']"})
        },
        'locations.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        },
        'locations.point': {
            'Meta': {'object_name': 'Point'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'})
        },
        'logistics.contactrole': {
            'Meta': {'object_name': 'ContactRole'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'responsibilities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['logistics.Responsibility']", 'null': 'True', 'blank': 'True'})
        },
        'logistics.product': {
            'Meta': {'object_name': 'Product'},
            'average_monthly_consumption': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'emergency_order_level': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'equivalents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'equivalents_rel_+'", 'null': 'True', 'to': "orm['logistics.Product']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'product_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sms_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.ProductType']"}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'logistics.producttype': {
            'Meta': {'object_name': 'ProductType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'logistics.responsibility': {
            'Meta': {'object_name': 'Responsibility'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'logistics.supplypoint': {
            'Meta': {'object_name': 'SupplyPoint'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_reported': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'supplied_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPointType']"})
        },
        'logistics.supplypointtype': {
            'Meta': {'object_name': 'SupplyPointType'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'primary_key': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rapidsms.backend': {
            'Meta': {'object_name': 'Backend'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'rapidsms.connection': {
            'Meta': {'unique_together': "(('backend', 'identity'),)", 'object_name': 'Connection'},
            'backend': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Backend']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Contact']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rapidsms.contact': {
            'Meta': {'object_name': 'Contact'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'commodities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'reported_by'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['logistics.Product']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'needs_reminders': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.ContactRole']", 'null': 'True', 'blank': 'True'}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contact'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'villagers'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'rapidsms_httprouter.message': {
            'Meta': {'object_name': 'Message'},
            'application': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'null': 'True', 'to': "orm['rapidsms_httprouter.MessageBatch']"}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': "orm['rapidsms.Connection']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_response_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'null': 'True', 'to': "orm['rapidsms_httprouter.Message']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'rapidsms_httprouter.messagebatch': {
            'Meta': {'object_name': 'MessageBatch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'rapidsms_xforms.xform': {
            'Meta': {'object_name': 'XForm'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'command_prefix': ('django.db.models.fields.CharField', [], {'default': "'+'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('eav.fields.EavSlugField', [], {'max_length': '32', 'db_index': 'True'}),
            'keyword_prefix': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'restrict_message': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'restrict_to': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'separator': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'rapidsms_xforms.xformsubmission': {
            'Meta': {'object_name': 'XFormSubmission'},
            'confirmation_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'null': 'True', 'to': "orm['rapidsms.Connection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'has_errors': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'null': 'True', 'to': "orm['rapidsms_httprouter.Message']"}),
            'raw': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'xform': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'to': "orm['rapidsms_xforms.XForm']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['healthmodels']
