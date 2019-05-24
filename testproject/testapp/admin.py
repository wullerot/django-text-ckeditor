from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from text_ckeditor.widgets import CKEditorWidget

from .models import TestModel


class TestModelAdminForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = TestModel
        widgets = {
            'text_html': CKEditorWidget
        }


class TestModelAdmin(admin.ModelAdmin):

    form = TestModelAdminForm


admin.site.register(TestModel, TestModelAdmin)
