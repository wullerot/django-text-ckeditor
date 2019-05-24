from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .. import conf


@python_2_unicode_compatible
class Link(models.Model):
    """
    intentionaly simple link model
    """
    url = models.URLField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('URL'),
    )
    target = models.CharField(
        max_length=255,
        blank=True,
        choices=conf.LINK_TARGETS,
        default='',
        verbose_name=_('target'),
    )
    email = models.EmailField(
        _('Email'),
        blank=True,
        default='',
    )

    class Meta:
        managed = False

    def __str__(self):
        return 'link {0}'.format(self.get_link())

    def get_link(self):
        return self.url or 'mailto:{0}'.format(self.email)

    def get_target(self):
        if self.target:
            return self.target
        else:
            return ''

    @property
    def href(self):
        return self.get_link()
