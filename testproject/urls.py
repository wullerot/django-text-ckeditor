from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(
        r'^admin/',
        admin.site.urls
    ),
    url(
        r'^',
        include('testapp.urls')
    ),
]
