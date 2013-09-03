# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ResultClass'
        db.create_table(u's2results_resultclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('data_csv', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('fields', self.gf('json_field.fields.JSONField')(default=u'null')),
            ('primary_field', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('secret_field', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u's2results', ['ResultClass'])

        # Adding model 'Result'
        db.create_table(u's2results_result', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('result_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['s2results.ResultClass'])),
            ('primary_field_value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('secret_field_value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('data', self.gf('json_field.fields.JSONField')(default=u'null')),
            ('results_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u's2results', ['Result'])


    def backwards(self, orm):
        # Deleting model 'ResultClass'
        db.delete_table(u's2results_resultclass')

        # Deleting model 'Result'
        db.delete_table(u's2results_result')


    models = {
        u's2results.result': {
            'Meta': {'object_name': 'Result'},
            'data': ('json_field.fields.JSONField', [], {'default': "u'null'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary_field_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'result_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['s2results.ResultClass']"}),
            'results_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'secret_field_value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u's2results.resultclass': {
            'Meta': {'object_name': 'ResultClass'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_csv': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fields': ('json_field.fields.JSONField', [], {'default': "u'null'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'primary_field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'secret_field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['s2results']