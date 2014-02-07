# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'DomainStats.created'
        db.alter_column(u'stats_domainstats', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):

        # Changing field 'DomainStats.created'
        db.alter_column(u'stats_domainstats', 'created', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'stats.domainstats': {
            'Meta': {'object_name': 'DomainStats'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outlinks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'page_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pages_not_found': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'richfiles': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['stats']