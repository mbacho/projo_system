# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AcademicDomain'
        db.create_table(u'johnnywalker_academicdomain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('domain', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'johnnywalker', ['AcademicDomain'])

        # Adding model 'AvoidUrl'
        db.create_table(u'johnnywalker_avoidurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['johnnywalker.AcademicDomain'])),
            ('url_pattern', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'johnnywalker', ['AvoidUrl'])


    def backwards(self, orm):
        # Deleting model 'AcademicDomain'
        db.delete_table(u'johnnywalker_academicdomain')

        # Deleting model 'AvoidUrl'
        db.delete_table(u'johnnywalker_avoidurl')


    models = {
        u'johnnywalker.academicdomain': {
            'Meta': {'object_name': 'AcademicDomain'},
            'domain': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'johnnywalker.avoidurl': {
            'Meta': {'object_name': 'AvoidUrl'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['johnnywalker.AcademicDomain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url_pattern': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['johnnywalker']