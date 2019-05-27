from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from text_ckeditor.conf import LINK_TARGETS
from text_ckeditor.models import AbstractLink


class Link(AbstractLink):

    LINK_TYPE_CHOICES = [
        ('', _('---')),
        ('link_url', _('URL')),
        ('link_email', _('Email')),
    ]

    link_url = models.URLField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('URL'),
    )
    link_url_target = models.CharField(
        max_length=255,
        blank=True,
        choices=LINK_TARGETS,
        default='',
        verbose_name=_('Target'),
    )
    link_email = models.EmailField(
        blank=True,
        default='',
        verbose_name=_('Email'),
    )

    class Meta:
        abstract = False

    def get_target(self):
        if (self.link_type == 'link_url'
                and getattr(self, 'link_url_target', '')):
            return self.link_url_target
        return ''
