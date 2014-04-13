# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext as _
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from financeweb.apphome import models
from django.core.urlresolvers import reverse
from financeweb.apphome.views import auth_required
from financeweb import api
from financeweb import settings 
from decimal import Decimal
from django.core.paginator import Paginator, InvalidPage, EmptyPage

class ExamineMessages(View):
    model = models.Finance
    def get(self, request, *args, **kwargs):
        financelist = self.model.objects.filter(status=0)
        count=0
        for finance in financelist:
            if request.user not in finance.examineperson.all():
                count+=1
        return HttpResponse(count)

class Index(View):
    template_name = 'appfinance/index.html'
    @auth_required
    def get(self, request):
        
        user = request.user
        (status,msg,objects) = api.finance.get_all_finance_data()
        completeobjects = models.Finance.objects.filter(status=2) 
        comp = Paginator(completeobjects,10)
        try:
            page = int(request.GET.get('objectspage', '1'))
        except ValueError:
            page = 1
        try:
            comppageobjects =  comp.page(page) 
        except (InvalidPage, EmptyPage):
            comppageobjects =  comp.page(comp.num_pages) 
        if status == 0:
            moneycount = Decimal(0.0) 
            for oneobject in objects:
                moneycount += oneobject.maneycount 
            return render_to_response(self.template_name, {'user': user, 'objects':objects,'moneycount':moneycount,'completeobjects':comppageobjects})
        else:
            return HttpResponse(u"获取数据失败")

class SelfFinance(View):
    template_name = 'appfinance/selffinance.html'
    @auth_required
    def get(self, request):
        user = request.user
        (status, msg, objects) = api.finance.get_user_finance_data(user)
        completeobjects = models.Finance.objects.filter(startperson=user,status=2)
        comp = Paginator(completeobjects,10)
        try:
            page = int(request.GET.get('objectspage', '1'))
        except ValueError:
            page = 1
        try:
            comppageobjects =  comp.page(page) 
        except (InvalidPage, EmptyPage):
            comppageobjects =  comp.page(comp.num_pages) 
        return render_to_response(self.template_name, {'user': user, 'objects':objects,'completeobjects':comppageobjects})
        
class ExamineDate(View):
    template_name = 'appfinance/examinedatashow.html'
    model = models.Finance
    @auth_required
    def get(self, request, *args, **kwargs):
        user = request.user
        financelist = self.model.objects.filter(status=0)
        objects = []
        for finance in financelist:
            if request.user not in finance.examineperson.all():  
                objects.append(finance)
        return render_to_response(self.template_name, {'user': user,'objects':objects})

class ExamineHistroyDate(View):
    template_name = 'appfinance/examinehistoryshow.html'
    @auth_required
    def get(self, request, *args, **kwargs):
        user = request.user
        objects = user.financeuser_set.all()
        p = Paginator(objects,10)
        try:
            page = int(request.GET.get('objectspage', '1'))
        except ValueError:
            page = 1
        try:
            pageobjects =  p.page(page) 
        except (InvalidPage, EmptyPage):
            pageobjects =  p.page(p.num_pages) 
        return render_to_response(self.template_name, {'objects':pageobjects,'user':user})

class DoCompFinance(View):
    """修改单据状态为已领款"""
    @auth_required
    def post(self, request, *args, **kwargs):
        financepk = request.POST.get("financepk", "")
        cashstatus = request.POST.get("cashstatus", "")
        if not financepk:
            return HttpResponse(u"单据号不能为空!")
        financeobject = models.Finance.objects.get(pk=int(financepk))
        if financeobject.status == 1 and request.user.userprofile.usertype == "financemanager":
            financeobject.status = 2
            financeobject.save()
            if cashstatus:
                cashobject = models.Cash(startperson=request.user, cashname=financeobject.financename, cashintro=financeobject.financeintro, cashsum=financeobject.maneycount, cashtype="-1")
                cashobject.save()
            return HttpResponse("")
        else:
            return HttpResponse(u"请确认你是财务部门主管，并且单据审批成功!")
        
        

class ExaminemakeShow(View):
    template_name = 'appfinance/examinemakeshow.html'
    @auth_required
    def get(self, request, *args, **kwargs):
        financepk = request.GET.get('finance', '')
        operate = request.GET.get('operate', '')
        if financepk:
            try:
                financeobject = models.Finance.objects.get(pk=int(financepk))
                return render_to_response(self.template_name, {'financeobject':financeobject,'operate':operate})
            except:
                return HttpResponse(u'数据错误，申请单不存在')
        else:
            return HttpResponse(u'数据错误，申请单编号不能为空')
    def post(self, request, *args, **kwargs):
        user = request.user
        financepk = request.POST.get('finance', '')
        operate = request.POST.get('operate', '')
        info = request.POST.get('info', '')
        financeobject=models.Finance.objects.get(pk=int(financepk))
        if operate:
            status = True 
        else:
            status = False 
        if models.FinanceUser.objects.filter(user=user, finance=financeobject): 
            financeuser=models.FinanceUser.objects.get(user=user, finance=financeobject)
            financeuser.status = status
            financeuser.examineinfo = info
            financeuser.save()
            if  len(models.FinanceUser.objects.filter(finance=financeobject,status=True)) >= 4:
                    financeobject.status = 1 
            elif models.FinanceUser.objects.filter(finance=financeobject,status=False):
                    financeobject.status = -1 
            else:
                    financeobject.status = 0 
            financeobject.save()
        else:
            financeuser = models.FinanceUser(user=user, finance=financeobject, status=status, examineinfo=info)
            financeuser.save()
            if  len(models.FinanceUser.objects.filter(finance=financeobject,status=True)) >= 4:
                    financeobject.status = 1 
            elif models.FinanceUser.objects.filter(finance=financeobject,status=False):
                    financeobject.status = -1 
            else:
                    financeobject.status = 0 
            financeobject.save()
        return HttpResponse(u'审批成功')

class MakeFinance(View):
    template_name="appfinance/makefinance.html"
    @auth_required
    def get(self, request, *args, **kwargs):
        user=request.user
        financetypelist = settings.FINANCE_TYPE
        financepk = request.GET.get('financepk','')
        if financepk:
            try:
                financeobject = models.Finance.objects.get(pk=int(financepk))
                financename = financeobject.financename
                financeinfo = financeobject.financeintro
                financecount = financeobject.maneycount
                financetype = financeobject.financetype
                financeimg = financeobject.financeimg
            except:
                financename = ""
                financeinfo = ""
                financecount = ""
                financeimg = ""
                financetype = settings.finance.FINANCE_TYPE[0][0] 
        else:
            financename = ""
            financeinfo = ""
            financecount = ""
            financeimg = ""
            financetype = settings.FINANCE_TYPE[0][0] 
        context={
            'financepk':financepk,
            'financeimg':financeimg,
            'financename':financename,
            'financeinfo':financeinfo,
            'financetype':financetype,
            'financetypelist':financetypelist,
            'financecount':financecount,
            'user':user,

        }
        return render_to_response(self.template_name,context) 
    @auth_required
    def post(self, request, *args, **kwargs):
        financename = request.POST.get('financename','')
        financeinfo = request.POST.get('financeinfo','')
        financetype = request.POST.get('financetype','')
        financecount = request.POST.get('financecount','')
        financepk = request.POST.get('financepk','')
        financeattach = request.FILES.get('financeattach','')
        try:
            float(financecount)
        except:
            return HttpResponse(u"金额必需是浮点数或整数")
        if financename and financeinfo and financetype and financecount:
            user = request.user
            if financepk:
                newobject = models.Finance.objects.get(pk=int(financepk))
                if newobject.startperson != request.user or newobject.status != -1:
                    return HttpResponse(u"只能修改自己提交后驳回的单据!")
                financeuserlist = newobject.financeuser_set.all()
                for financeuser in financeuserlist:
                    financeuser.delete()
                newobject.maneycount = financecount
                newobject.financename = financename
                newobject.financeintro = financeinfo
                newobject.financetype = financetype
                newobject.financeimg = financeattach
                newobject.status = 0 
            else:
                newobject = models.Finance(startperson=user, maneycount=financecount, financename=financename, financeintro=financeinfo, financetype=financetype, financeimg = financeattach)
            newobject.save()
            return HttpResponseRedirect(reverse("home"))
        else:
            return HttpResponse(u'名称:'+financename+u' 描述:'+financeinfo+u'类型:'+financetype+u'金额:'+financecount+u" 都不能为空,且金额为浮点型")

class GetAttach(View):
    template_name="appfinance/getattach.html"
    @auth_required
    def get(self, request, *args, **kwrargs):
        imgpath = request.GET.get("imgpath","")
        if imgpath:
            return render_to_response(self.template_name,{'imgpath':imgpath})
        else:
            return HttpResponse(u"加载附件失败，请驳回重新上传附件!")

# 计算相关

class DeleteFinance(View):
    @auth_required
    def post(self, request, *args, **kwargs):
        financepk = request.POST.get('financepk', '')
        financeobject = models.Finance.objects.get(pk=int(financepk))
        if financeobject.startperson == request.user and financeobject.status == -1:
            financeuserlist = financeobject.financeuser_set.all()
            for financeuser in financeuserlist:
                financeuser.delete()
            financeobject.delete()
            return HttpResponse("")
        else:
            return HttpResponse(u"只能删除自己提交后驳回的单据！")

class GETNowSum(View):
    @auth_required
    def get(self, request, *args, **kwargs):
        incountlist = models.InFinance.objects.filter(status=True)
        outcountlist =models.Finance.objects.filter(status=2)
        sumin = 0.00
        sumout = 0.00
        for incount in incountlist:
            sumin += float(incount.maneycount)
        for outcount in outcountlist:
            sumout += float(outcount.maneycount)
        endcount = sumin-sumout
        if request.user.userprofile.usertype == "financemanager":
            cashlist = models.Cash.objects.filter(status=True)
            cashsum=Decimal(0.0)
            for cash in cashlist:
                cashsum += Decimal(cash.cashtype)*cash.cashsum
            cardsum = Decimal(endcount)-cashsum
            strs = u"余额:"+str(endcount)+u"元<a  target='_blank' href='/admin/apphome/cash/'>(现金:" + str(cashsum) + u"银行卡:" + str(cardsum) + u")</a>|总额:"+str(sumin)+u"元|总支出:"+str(sumout)+u"元"
        else:
            strs = u"余额:"+str(endcount)+u"元|总额:"+str(sumin)+u"元|总支出:"+str(sumout)+u"元"
        return HttpResponse(strs)
