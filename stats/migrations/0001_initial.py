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
            ('projectdomain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webui.ProjectDomain'])),
            ('outlinks', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('richfiles', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pages_not_found', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('page_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'stats', ['DomainStats'])


    def backwards(self, orm):
        # Deleting model 'DomainStats'
        db.delete_table(u'stats_domainstats')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'johnnywalker.academicdomain': {
            'Meta': {'object_name': 'AcademicDomain'},
            'domain': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'stats.domainstats': {
            'Meta': {'object_name': 'DomainStats'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outlinks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'page_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pages_not_found': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'projectdomain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webui.ProjectDomain']"}),
            'richfiles': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'webui.project': {
            'Meta': {'unique_together': "(('name', 'owner'),)", 'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': u"orm['auth.User']"})
        },
        u'webui.projectdomain': {
            'Meta': {'object_name': 'ProjectDomain'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projectdomain_domain'", 'to': u"orm['johnnywalker.AcademicDomain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobid': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projectdomain_project'", 'to': u"orm['webui.Project']"}),
            'starttime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'starturl': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20', 'blank': 'True'}),
            'stoptime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['stats']