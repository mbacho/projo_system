# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DomainStats'
        db.create_table(u'stats_domainstats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('outlinks', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('richfiles', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pages_not_found', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('page_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'stats', ['DomainStats'])


    def backwards(self, orm):
        # Deleting model 'DomainStats'
        db.delete_table(u'stats_domainstats')


    models = {
        u'stats.domainstats': {
            'Meta': {'object_name': 'DomainStats'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outlinks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'page_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pages_not_found': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'richfiles': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['stats']