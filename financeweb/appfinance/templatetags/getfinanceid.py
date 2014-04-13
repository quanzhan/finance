#-*- coding: utf-8 -*_
#!/usr/bin/env python

from django import template
import re
import time
register =  template.Library()

def get_financeid(times,financepk):
    financeid = str(int(time.mktime(times.timetuple())))+str(financepk)
     
    return financeid[-10:]
register.filter('get_financeid', get_financeid)
