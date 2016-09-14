from __future__ import unicode_literals

import re
from lxml.html import fragment_fromstring, tostring

from django import template
from django.apps import apps
from django.template.defaultfilters import stringfilter

from .. import conf

register = template.Library()


PATTERN = r'<a [^>]*\bdjangolink="true"[^>]*/?>'
RE = re.compile(PATTERN, flags=re.DOTALL)


@register.filter
@stringfilter
def text_ckeditor_link(html):
    # TODO get rid of extra <div>
    # TODO get rid of lxml
    # TODO add email spam protection
    LinkModel = apps.get_model(app_label=conf.LINK_MODULE,
                               model_name=conf.LINK_MODEL_NAME)
    fragment = fragment_fromstring("<div>" + html + "</div>")
    links = fragment.cssselect('a[data-djangolink="true"]')
    for link in links:
        link.attrib.pop('data-djangolink')
        link_model = LinkModel()
        kwargs = {}
        for key, value in link.items():
            if key.startswith('data-'):
                field = key.replace('data-', '', 1)
                if hasattr(link_model, field):
                    value = link.attrib.pop(key)
                    if value:
                        kwargs.update({field: value})

        link_model = LinkModel(**kwargs)
        link.set('href', link_model.href)
        if link_model.target:
            link.set('target', link_model.target_tag)
    return tostring(fragment)
