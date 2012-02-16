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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'healthmodels.facilityreport': {
            'Meta': {'object_name': 'FacilityReport', '_ormbases': ['healthmodels.FacilityReportBase']},
            'facilityreportbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.FacilityReportBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'healthmodels.facilityreportbase': {
            'Meta': {'object_name': 'FacilityReportBase'},
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.HealthFacility']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'healthmodels.healthfacility': {
            'Meta': {'object_name': 'HealthFacility', '_ormbases': ['healthmodels.HealthFacilityBase']},
            'healthfacilitybase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.HealthFacilityBase']", 'unique': 'True', 'primary_key': 'True'})
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
            'patientencounterbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['healthmodels.PatientEncounterBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'healthmodels.patientencounterbase': {
            'Meta': {'object_name': 'PatientEncounterBase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthmodels.Patient']"})
        },
        'locations.location': {
            'Meta': {'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'rapidsms.contact': {
            'Meta': {'object_name': 'Contact'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'anc_visits': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'birthdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'last_menses': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'owns_phone': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'villagers'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['healthmodels']
