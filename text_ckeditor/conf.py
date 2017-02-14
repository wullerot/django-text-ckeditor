from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

LINK_MODEL = getattr(
    settings,
    'TEXT_CKEDITOR_LINK_MODEL',
    'links.Link'
)
LINK_MODULE, LINK_MODEL_NAME = LINK_MODEL.rsplit('.', 1)
LINK_IFRAME_URL = reverse_lazy(
    'admin:{0}_{1}_add'.format(
        LINK_MODULE,
        LINK_MODEL_NAME.lower()
    )
)
LINK_VERIFY_URL = reverse_lazy(
    'admin:{0}_{1}_verify'.format(
        LINK_MODULE,
        LINK_MODEL_NAME.lower()
    )
)
LINK_TARGETS = [('', 'same window'), ('_blank', 'new window')]
CKEDITOR_HTML_MARK_SAFE = getattr(
    settings,
    'TEXT_CKEDITOR_HTML_MARK_SAFE',
    True
)
CKEDITOR_HTML_PROTECT_MAILTO = getattr(
    settings,
    'TEXT_CKEDITOR_HTML_PROTECT_MAILTO',
    True
)
CKEDITOR_CONF = getattr(
    settings,
    'TEXT_CKEDITOR_CONF',
    {
        'height': 400,
        'skin': 'moono-lisa',
        'uiColor': '#ffffff',
        'extraPlugins': 'djangolink',
        'toolbar': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['h1', 'h2', 'h3', 'h4'],
            ['NumberedList', 'BulletedList'],
            ['DjangoLink', 'Unlink'],
            ['Subscript', 'Superscript'],
            ['PasteText' ],
            ['Source'],
            ['Maximize'],
        ],
    }
)

CKEDITOR_CONF.update({
    'djangolinkIframeURL': LINK_IFRAME_URL,
    'djangolinkVerifyURL': LINK_VERIFY_URL,
})
