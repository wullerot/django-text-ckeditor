from django.urls import path

from .views import TestModelListView


urlpatterns = [
    path(
        '',
        TestModelListView.as_view(),
        name='index'
    ),
]
