from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class AbstractLink(models.Model):
    """
    intentionaly simple link model
    """

    LINK_TYPE_CHOICES = [
        ('', _('---')),
        ('link_url', _('URL')),
    ]

    link_type = models.CharField(
        max_length=80,
        blank=True,
        default='',
        verbose_name=_('Link Type'),
    )

    link_url = models.URLField(
        blank=True,
        default='',
        verbose_name=_('URL'),
    )

    class Meta:
        abstract = True
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def __str__(self):
        return 'link {}'.format(self.get_link())

    def get_link(self):
        try:
            link = getattr(self, self.link_type, '')
        except Exception:
            link = ''
        if link and self.link_type == 'link_email':
            link = 'mailto:{}'.format(link)
        return '{}'.format(link)

    def get_link_type(self):
        if self.link_type and hasattr(self, self.link_type):
            return self.link_type
        for name, title in self.LINK_TYPE_CHOICES:
            value = getattr(self, name, None)
            if value:
                return name

    def get_target(self):
        return ''

    @property
    def href(self):
        return self.get_link()
