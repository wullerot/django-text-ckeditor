from __future__ import unicode_literals

from django import template
from django.template.defaultfilters import stringfilter

from ..utils import CKEditorHtml


register = template.Library()


@register.filter
@stringfilter
def text_ckeditor_render(html):
    ck_html = CKEditorHtml(html)
    return ck_html.render()
