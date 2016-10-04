from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.db import models
from django.http import JsonResponse


class DjangoLinkAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        '''
        http://stackoverflow.com/questions/2431727/django-admin-hide-a-model
        Return empty perms dict thus hiding the model from admin index.
        '''
        return {}

    def get_urls(self):
        '''
        add our verify url.
        '''
        urls = [
            url(
                r'^verify/$',
                self.admin_site.admin_view(self.verify),
                name=self._get_verify_url_name()
            ),
        ]
        return urls + super(DjangoLinkAdmin, self).get_urls()

    def _get_verify_url_name(self):
        return '{0}_{1}_verify'.format(self.model._meta.app_label,
                                       self.model._meta.model_name)

    def verify(self, request):
        # TODO cleanup this mess
        form = self.get_form(request, )(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            obj = self.model(**data)
            link_value = ''
            # prepopulate href
            if hasattr(obj, 'get_link'):
                link_value = obj.get_link()
            # basic serialize only
            for key, value in data.items():
                if isinstance(value, models.Model):
                    data[key] = value.id
            return_data = {
                'valid': 'true',
                'data': data,
                'link_value': link_value
            }
        else:
            errors = []
            for k, values in form.errors.items():
                e = [k]
                for v in values:
                    e.append(v)
                errors.append(e)
            return_data = {'valid': 'false', 'errors': errors}
        return JsonResponse(return_data)

    def save_model(self, request, obj, form, change):
        '''
        avoid save!
        '''
        return False
