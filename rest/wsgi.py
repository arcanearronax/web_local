"""
WSGI config for blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ['SKEY'] = 'qlax4%-sn$jfbxki435x2!1*w7%%mhxi5kzrc7@4(q#enlp5-5'
os.environ['AHOST'] = 'rest.arcanedomain.duckdns.org'
os.environ['BHOST'] = '10.0.0.4'
os.environ['userName'] = 'webmaster'
os.environ['userPass'] = 'Dexter313!'

application = get_wsgi_application()
