# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from financeweb.settings import FINANCE_TYPE,INFINANCE_TYPE,USER_TYPE
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    usertype = models.CharField(_('usertype'),max_length=50,choices=USER_TYPE)
    userimg =  models.ImageField(u"用户头像", max_length=256, upload_to='./user', blank=True, null=True)
    
class Finance(models.Model):
    startperson = models.ForeignKey(User)
    maneycount = models.DecimalField(max_digits=8,decimal_places=2)
    financename = models.CharField(_('name'), max_length=80)
    financeintro = models.CharField(_('intro'), max_length=200)
    examineperson = models.ManyToManyField(User, through="FinanceUser", null=True, blank=True, related_name="examineperson", verbose_name=_("users"))
    financedate = models.DateTimeField(auto_now_add=True)
    financetype = models.CharField(_('financetype'), max_length=80, choices=FINANCE_TYPE, default='payment')
    financeimg =  models.ImageField(u"单据附件", max_length=256, upload_to='./finance', blank=True, null=True)
    status = models.IntegerField(_("Status"), default=0) #0审批中，1审批通过，-1审批驳回, 2已领款
    def __unicode__(self):
        return self.financename
    class Meta:
        ordering = ['-financedate']

class Cash(models.Model):
    CASH_TYPE = (
    ('1', u"公司卡取现"),
    ('-1', u"现金支出")
    )
    startperson = models.ForeignKey(User)
    cashname = models.CharField(_('name'), max_length=80)
    cashintro = models.CharField(_('intro'), max_length=200)
    cashsum = models.DecimalField(max_digits=8,decimal_places=2) 
    cashtype = models.CharField(_('cashtype'), max_length=80, choices=CASH_TYPE)
    cashdate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(_("status"), default=True)
    def __unicode__(self):
        return self.cashname
    class Meta:
        ordering = ['-cashdate']

class InFinance(models.Model):
    startperson = models.ForeignKey(User)
    maneycount = models.DecimalField(max_digits=12,decimal_places=2)
    infinancename = models.CharField(_('name'), max_length=80)
    financeintro = models.CharField(_('intro'), max_length=80)
    financetype = models.CharField(_('financetype'), max_length=80, choices=INFINANCE_TYPE, default='payment')
    financedate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(_("status"), default=False)
    def __unicode__(self):
        return self.infinancename
    class Meta:
        ordering = ['-financedate']

class FinanceUser(models.Model):
    finance = models.ForeignKey(Finance)
    user = models.ForeignKey(User)
    status = models.BooleanField(_("examinestatus"), default=False)
    examinedate = models.DateTimeField(auto_now_add=True)
    examineinfo = models.CharField(_("examineinfo"), max_length=80, null=True, blank=True)
    def __unicode__(self):
        return self.finance
    class Meta:
        ordering = ['-examinedate']
