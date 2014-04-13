#-!- coding:UTF-8 -!-

from financeweb.apphome import models 


def apply_bill(title, detail, finance_type, amount):
    """Apply a bill

    Anyone can apply a bill, we use bill to manage our various expenses 
    and spending.

    Params: 
        title STRING    # Bill title
        detail STRING   # Bill explanation
        finance_type STRING     # Bill type
        amount FLOAT    # Bill

    Return:
        status INT  # 0: success; other integer: failure
        msgs STRING # If status equal 0, msgs will show the error message
        results None

    Author: XXXX
    MAIL: xxxx@gmail.com
    Create_at: 2014-02-03
    Update_at:
    """

    # Initialization
    status = 0; msgs = ''; results = None

    return (status, msgs, results)


def get_expenditure_total():
    """ Get the total expenditure

    Note: this does not include the deposit

    Return:
       status INT  # 0: success; other integer: failure
       msgs STRING # If status equal 0, msgs will show the error message
       results INT # Total expenses

    Author: XXX
    MAIL: xxx@gmail.com
    Create_at: 2014-03-20
    Update_at:
    """

    # Initialization
    status = 0; msgs = ''; results = 208888

    return (status, msgs, results)


def get_expenditure_permonth(year, month):
    """ 获取每个月的总支出

    注意，这里也是不包括押金，真正花出去的支出

    Params: 
       year INT    # 年，例如2014
       month INT   # 月份，例如3月

    Return:
       status INT  # 0: success; other integer: failure
       msgs STRING # If status equal 0, msgs will show the error message
       results INT # 总支出(不包含押金的，实际真正花出去，无法收回的)

    Author: XXXX
    MAIL: xxxx@gmail.com
    Create_at: 2014-02-03
    Update_at:
    """

    # Initialization
    status = 0; msgs = ''; results = 400

    alldate = models.Finance.objects.exclude(financetype='bond').filter(status='2', financedate__year=year, financedate__month=month)
    results = 0
    for date in alldate:
        results = results + date.maneycount
    

    return (status, msgs, results)


def get_all_finance_data():
    """获取所有申请单数据

    Params: None

    Return:
       status INT  # 0: success; other integer: failure
       msgs STRING # If status equal 0, msgs will show the error message
       results OBJECTLIST #fiance object list

    Author: XXX
    MAIL: xxx@gmail.com
    Create_at: 2014-03-20
    Update_at:
    """
    
    # Initialization
    status = 0; msgs = ''; results = [] 
    results = models.Finance.objects.exclude(status=2)

    return (status, msgs, results)

def get_user_finance_data(user):
    """获取指定用户所有提交请款单数据

    Params: 
        user STR #用户

    Return:
       status INT  # 0: success; other integer: failure
       msgs STRING # If status equal 0, msgs will show the error message
       results OBJECTLIST #finance object list above the user

    Author: XXX
    MAIL: xxx@gmail.com
    Create_at: 2014-03-20
    Update_at:
    """
    
    # Initialization
    status = 0; msgs = ''; results = [] 
    results = models.Finance.objects.filter(startperson=user).exclude(status=2)

    return (status, msgs, results)
    

def make_finance(user, financename, financeintro, financetype, financecount, financeattach, financepk=None):
    """创建和更加请款单
    @Params:
        user STR    #发起人
        financename STR #请款单名称
        financeintro STR#请款单描述
        financetype STR #请款单类型
        financecount STR#请款单金额
        financeattach IMAGEFILE#截图
        financepk INT #当为None，为创建新的请款单，当整数时更新指定pk的请款单数据

    Return:
       status INT  # 0: success; other integer: failure
       msgs STRING # If status equal 0, msgs will show the error message
       results None

    Author: XXX
    MAIL: xxx@gmail.com
    Create_at: 2014-03-20
    Update_at:
    """

    # Initialization
    status = 0; msgs = ''; results = [] 
    try:
        float(financecount)
    except:
        return ('1', u'金额必需是浮点数或整数', [])

    if not financename:
        return ('2', u'名称: 不能为空', [])

    if not financeintro:
        return ('3', u'描述: 不能为空', [])

    if not financetype:
        return ('4', u'类型: 不能为空', [])

    if not financecount:
        return ('5', u'金额: 不能为空', [])
        
    if fianncepk:
        newobject = models.Finance.objects.get(pk=int(financepk))
        if newobject.startperson != user or newobject.status != -1:
            return ('6', u'只能修改自己提交后驳回的单据!', [])
        financeuserlist = newobject.financeuser_set.all() 
        for financeuser in financeuserlist: 
            financeuser.delete() 

        newobject.startperson = user
        newobject.financename = financename
        newobject.financeintro = financeintro
        newobject.financetype = financetype
        newobject.maneycount = financecount
        newobject.financeimg = financeattach
        newobject.save
    else:
        models.Finance.objects.create(startperson=user, financename=financename, financeintro=financeintro, financetype=financetype, financeimg=financeattach, maneycount=financecount)

    return (status, msgs, results)


def make_examine_change_status_for_finance(financepk, user, examineinfo, operate):
    """创建或更新审批信息,同时更新请款单状态
    @Params:
        financepk INT #需审核的请款单pk
        user      STR #审核人
        examineinfo STR#审核意见
        operate   BOOL#True为审核通过、False为审核失败

    Return:
       status INT  # 0: success; other integer: failure
       msgs STRING # If status equal 0, msgs will show the error message
       results None

    Author: XXX
    MAIL: xxx@gmail.com
    Create_at: 2014-03-20
    Update_at:
    """

    # Initialization
    status = 0; msgs = ''; results = None 

    return (status, msgs, results)

def get_user_examine_data(user): 
    """获取指定用户需要审批的数据，及审批历史数据
    
    @Params:
        user STR # 用户

    Return:
       status INT  # 0: success; other integer: failure
       msgs STRING # If status equal 0, msgs will show the error message
       results DICT# {'needexamine': need examine finance object list,
                      'examinehistory': history examine finance object list
        }

    Author: XXX
    MAIL: xxx@gmail.com
    Create_at: 2014-03-20
    Update_at:
    """

    # Initialization
    status = 0; msgs = ''; results = {'needexamine':[],'examinehistory':[]} 

    financelist = models.Finance.objects.all()

    for financedate in financelist:
        if user in financedate.examineperson.all():
            results['examinehistory'].append(financedate)
        elif financedate.status == 0:
            results['needexamine'].append(financedate)
 
    return (status, msgs, results)

