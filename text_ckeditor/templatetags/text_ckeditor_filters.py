from __future__ import unicode_literals

from lxml.html import fragment_fromstring, tostring

from django import template
from django.apps import apps
from django.template.defaultfilters import stringfilter

from .. import conf

register = template.Library()
LinkModel = apps.get_model(app_label=conf.LINK_MODULE,
                           model_name=conf.LINK_MODEL_NAME)

wrappers = [
    '<div>',
    '</div>'
]

@register.filter
@stringfilter
def text_ckeditor_link(html):
    # TODO get rid of extra <div>
    # TODO get rid of lxml
    # TODO add email spam protection
    fragment = fragment_fromstring(
        '{0}{1}{2}'.format(wrappers[0], html, wrappers[1])
    )
    dummy_model = LinkModel()
    links = fragment.cssselect('a[data-djangolink="true"]')
    for link in links:
        link.attrib.pop('data-djangolink')
        kwargs = {}
        for key, value in link.items():
            if key.startswith('data-'):
                field = key.replace('data-', '', 1)
                if hasattr(dummy_model, field):
                    value = link.attrib.pop(key)
                    if value:
                        kwargs.update({field: value})

        link_model = LinkModel(**kwargs)
        link.set('href', link_model.href)
        if link_model.get_target():
            link.set('target', link_model.get_target())
    return tostring(fragment)[len(wrappers[0]):-len(wrappers[1])]
