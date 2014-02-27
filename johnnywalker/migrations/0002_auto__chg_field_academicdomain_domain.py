# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AcademicDomain.domain'
        db.alter_column(u'johnnywalker_academicdomain', 'domain', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):

        # Changing field 'AcademicDomain.domain'
        db.alter_column(u'johnnywalker_academicdomain', 'domain', self.gf('django.db.models.fields.URLField')(max_length=200))

    models = {
        u'johnnywalker.academicdomain': {
            'Meta': {'object_name': 'AcademicDomain'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'johnnywalker.avoidurl': {
            'Meta': {'object_name': 'AvoidUrl'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'avoidurl_domain'", 'to': u"orm['johnnywalker.AcademicDomain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url_pattern': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['johnnywalker']