from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse_lazy

LINK_MODEL = getattr(
    settings,
    'TEXT_CKEDITOR_LINK_MODEL',
    'links.Link'
)
LINK_MODEL_LIST = LINK_MODEL.split(".")
LINK_MODEL_NAME = LINK_MODEL_LIST.pop()
LINK_MODULE = '.'.join(LINK_MODEL_LIST)

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
