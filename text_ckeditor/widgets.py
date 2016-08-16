from __future__ import unicode_literals

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms import Textarea
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe


class CKEditorWidget(Textarea):
    widget = Textarea
    template_name = 'ckeditor/widget.html'

    class Media:
        css = {
            'screen': [
                static('ckeditor/css/widget.css'),
            ],
        }
        js = [
            static('ckeditor/ckeditor/ckeditor.js'),
            static('ckeditor/js/widget.js'),
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
        data_tags = ' '.join(['data-{0}="{1}"'.format(k, v)
                             for k, v in self.conf.items()])
        context = {
            'attrs': attrs,
            'attrs_tags': mark_safe(attrs_tags),
            'data': self.conf,
            'data_tags': mark_safe(data_tags),
            'value': force_text(value),
        }
        return render_to_string(self.template_name, context)
