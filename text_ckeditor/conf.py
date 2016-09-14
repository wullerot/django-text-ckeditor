from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse_lazy


LINK_IFRAME_URL = getattr(
    settings,
    'TEXT_CKEDITOR_LINK_IFRAME_URL',
    '/links/link/add/'
)
LINK_VERIFY_URL = getattr(
    settings,
    'TEXT_CKEDITOR_LINK_VERIFY_URL',
    '/links/link/verify/'
)
LINK_TARGETS = [
    ('', 'same window'),
    ('_blank', 'new window'),
]
CKEDITOR_CONF = getattr(
    settings,
    'TEXT_CKEDITOR_CONF',
    {
        'height': 400,
        'skin': 'minimalist',
        'uiColor': '#ffffff',
        'extraPlugins': 'djangolink',
        'toolbar': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['h1', 'h2', 'h3'],  # ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
            ['NumberedList', 'BulletedList'],
            ['DjangoLink', 'Unlink'],
            ['Subscript', 'Superscript'],
            ['Source'],
            ['Maximize'],
        ],
        'djangolinkIframeURL': LINK_IFRAME_URL,
        'djangolinkVerifyURL': LINK_VERIFY_URL,
    }
)
