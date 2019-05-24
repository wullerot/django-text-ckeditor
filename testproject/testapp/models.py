from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TestModel(models.Model):

    text_html = models.TextField(
        default='',
        blank=True,
    )

    class Meta:
        ordering = ['pk']
        verbose_name = 'Test model'
        verbose_name_plural = 'Test models'

    def __str__(self):
        return 'Testmodel {}'.format(self.pk)
