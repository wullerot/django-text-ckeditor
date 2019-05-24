from __future__ import unicode_literals

from django.conf.urls import url

from .views import TestModelListView


urlpatterns = [
    url(
        r'^$',
        TestModelListView.as_view(),
        name='index'
    ),
]
