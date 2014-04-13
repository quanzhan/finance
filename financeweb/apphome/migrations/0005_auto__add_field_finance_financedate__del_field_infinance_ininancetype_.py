# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Finance.financedate'
        db.add_column(u'apphome_finance', 'financedate',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 3, 20, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'InFinance.ininancetype'
        db.delete_column(u'apphome_infinance', 'ininancetype')

        # Adding field 'InFinance.financetype'
        db.add_column(u'apphome_infinance', 'financetype',
                      self.gf('django.db.models.fields.CharField')(default='payment', max_length=80),
                      keep_default=False)

        # Adding field 'InFinance.financedate'
        db.add_column(u'apphome_infinance', 'financedate',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 3, 20, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Finance.financedate'
        db.delete_column(u'apphome_finance', 'financedate')

        # Adding field 'InFinance.ininancetype'
        db.add_column(u'apphome_infinance', 'ininancetype',
                      self.gf('django.db.models.fields.CharField')(default='payment', max_length=80),
                      keep_default=False)

        # Deleting field 'InFinance.financetype'
        db.delete_column(u'apphome_infinance', 'financetype')

        # Deleting field 'InFinance.financedate'
        db.delete_column(u'apphome_infinance', 'financedate')


    models = {
        u'apphome.finance': {
            'Meta': {'object_name': 'Finance'},
            'examineperson': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'examineperson'", 'to': u"orm['auth.User']", 'through': u"orm['apphome.FinanceUser']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'financedate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'financeintro': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'financename': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'financetype': ('django.db.models.fields.CharField', [], {'default': "'payment'", 'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maneycount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'startperson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'apphome.financeuser': {
            'Meta': {'object_name': 'FinanceUser'},
            'examinedate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'examineinfo': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'finance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apphome.Finance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'apphome.infinance': {
            'Meta': {'object_name': 'InFinance'},
            'financedate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'financeintro': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'financetype': ('django.db.models.fields.CharField', [], {'default': "'payment'", 'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infinancename': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'maneycount': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'startperson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
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
        }
    }

    complete_apps = ['apphome']