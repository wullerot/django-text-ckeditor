from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from text_ckeditor.text_ckeditor_links.models import AbstractLink


@python_2_unicode_compatible
class CKEditorLink(AbstractLink):
    pass
