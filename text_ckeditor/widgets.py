from __future__ import unicode_literals

import json

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms import Textarea
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from . import conf


class CKEditorWidget(Textarea):
    widget = Textarea
    template_name = 'text_ckeditor/widget.html'

    class Media:
        css = {
            'screen': [
                static('text_ckeditor/css/widget.css'),
            ],
        }
        js = [
            static('text_ckeditor/ckeditor/ckeditor.js'),
            static('text_ckeditor/js/widget.js'),
        ]

    def __init__(self, *args, **kwargs):
        self.conf = kwargs.pop('conf', {})
        attrs = {
            'cols': 120,
            'rows': 20,
            'class': 'textarea-ckeditor default'
        }
        super(CKEditorWidget, self).__init__(attrs)

    def render(self, name, value='', attrs=None):
        attrs = self.build_attrs(attrs, name=name)
        attrs_tags = ' '.join(['{0}="{1}"'.format(k, v)
                              for k, v in attrs.items()])
        context = {
            'attrs': attrs,
            'attrs_tags': mark_safe(attrs_tags),
            'data_tags': self.data_tags,
            'value': force_text(value),
        }
        return render_to_string(self.template_name, context)

    @property
    def data_tags(self):
        # TODO test if conf is ok
        default = conf.CKEDITOR_CONF.copy()
        default.update(self.conf)
        data = []
        for k, v in default.items():
            if type(v) is list or type(v) is tuple or type(v) is dict:
                v = json.dumps(v)
            elif type(v) is bool:
                v = str(v).lower()
            data.append("data-{0}='{1}'".format(k, v))
        return mark_safe(' '.join(data))
