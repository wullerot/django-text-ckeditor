from django import template
from django.template.defaultfilters import stringfilter

from ..utils import CKEditorHtml


register = template.Library()


@register.filter
@stringfilter
def text_ckeditor_render(html):
    ck_html = CKEditorHtml(html)
    return ck_html.render()


@register.filter
@stringfilter
def text_ckeditor_render_unprotected(html):
    ck_html = CKEditorHtml(html)
    return ck_html.render(unprotected=True)
