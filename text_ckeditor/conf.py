from __future__ import unicode_literals

from django.conf import settings


CKEDITOR_CONF = getattr(
    settings,
    'TEXT_CKEDITOR_CONF',
    {
        'height': 400,
        'skin': 'minimalist',
        'uiColor': 'ffffff',
        'toolbar': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['h2', 'h3', 'h4'],  # ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['Subscript', 'Superscript'],
            ['Source'],
            ['Maximize'],
        ],
    }
)
