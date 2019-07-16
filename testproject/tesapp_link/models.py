from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from text_ckeditor.text_ckeditor_links.models import AbstractLink


@python_2_unicode_compatible
class CKEditorLink(AbstractLink):
    pass
