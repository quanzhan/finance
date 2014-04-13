from __future__ import unicode_literals

import os,sys

#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
#settings_module = "%s.settings" % PROJECT_ROOT.split(os.sep)[-1]
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
#
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
if not os.path.dirname(__file__) in sys.path[:1]:
    sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
