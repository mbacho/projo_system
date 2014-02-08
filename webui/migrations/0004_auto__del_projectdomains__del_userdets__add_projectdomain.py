# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ProjectDomains'
        db.delete_table(u'webui_projectdomains')

        # Deleting model 'UserDets'
        db.delete_table(u'webui_userdets')

        # Adding model 'ProjectDomain'
        db.create_table(u'webui_projectdomain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webui.Project'])),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['johnnywalker.AcademicDomain'])),
            ('subdomain', self.gf('django.db.models.fields.CharField')(default='', max_length=50, null=True, blank=True)),
            ('starturl', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('jobid', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('starttime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 8, 0, 0), auto_now_add=True, blank=True)),
            ('stoptime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('stopreason', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
        ))
        db.send_create_signal(u'webui', ['ProjectDomain'])


    def backwards(self, orm):
        # Adding model 'ProjectDomains'
        db.create_table(u'webui_projectdomains', (
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webui.Project'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 8, 0, 0), auto_now_add=True, blank=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['johnnywalker.AcademicDomain'])),
            ('reason', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('starturl', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('stop', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('jobid', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal(u'webui', ['ProjectDomains'])

        # Adding model 'UserDets'
        db.create_table(u'webui_userdets', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'webui', ['UserDets'])

        # Deleting model 'ProjectDomain'
        db.delete_table(u'webui_projectdomain')


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
        u'webui.project': {
            'Meta': {'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'webui.projectdomain': {
            'Meta': {'object_name': 'ProjectDomain'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['johnnywalker.AcademicDomain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['webui.Project']"}),
            'starttime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 8, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'starturl': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'stopreason': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'stoptime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['webui']