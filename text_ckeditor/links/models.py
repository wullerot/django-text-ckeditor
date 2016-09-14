from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from .. import conf


@python_2_unicode_compatible
class Link(models.Model):
    """
    intentionaly simple link model
    """
    url = models.URLField(_('URL'), max_length=255, blank=True, default='')
    target = models.CharField(_('target'), max_length=255, blank=True,
                              choices=conf.LINK_TARGETS, default='')
    email = models.EmailField(_('Email'), blank=True, default='')

    class Meta:
        managed = False

    def __str__(self):
        return 'link {0}'.format(self.get_link())

    def get_link(self):
        return self.url or 'mailto:{0}'.format(self.email)

    @property
    def href(self):
        return self.get_link()

    @property
    def target_tag(self):
        if self.target:
            return self.target
        else:
            return ''
