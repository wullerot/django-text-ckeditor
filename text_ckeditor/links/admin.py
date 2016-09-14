from __future__ import unicode_literals

from django.contrib import admin

from text_ckeditor.admin import DjangoLinkAdmin

from ..admin import DjangoLinkAdmin
from .models import Link


@admin.register(Link)
class LinkAdmin(DjangoLinkAdmin):
    pass
