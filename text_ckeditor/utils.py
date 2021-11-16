import random
import re
from lxml.html import fragments_fromstring, fragment_fromstring, tostring

from django.apps import apps
from django.utils.safestring import mark_safe

from . import conf


try:
    basestring
except NameError:
    basestring = str


class CKEditorHtml(object):

    # TODO replace data-djangolink="true" constant
    link_model = apps.get_model(
        app_label=conf.LINK_MODULE,
        model_name=conf.LINK_MODEL_NAME
    )

    def __init__(self, input):
        self.input = input
        self.empty_link = self.link_model()

    def render(self, unprotected=False):
        # set if email needs scrambling
        if not conf.CKEDITOR_HTML_PROTECT_MAILTO:
            self.unprotected = True
        else:
            self.unprotected = unprotected

        output = ''
        fragments = fragments_fromstring(self.input)
        for fragment in fragments:
            output += self._render_fragment(fragment)
        if conf.CKEDITOR_HTML_MARK_SAFE:
            output = mark_safe(output)
        return output

    def _render_fragment(self, fragment):
        if isinstance(fragment, basestring):
            fragment = fragment_fromstring('<p>' + fragment + '</p>')
        django_links = fragment.cssselect('a[data-djangolink="true"]')
        for link in django_links:
            self._alter_link(link, fragment)
        return tostring(fragment, encoding='unicode')

    def _alter_link(self, link, fragment):
        link.attrib.pop('data-djangolink')
        kwargs = {}
        for key, value in link.items():
            if key.startswith('data-'):
                field = key.replace('data-', '', 1)
                value = link.attrib.pop(key)
                if value:
                    # convert to id int field if foreign key
                    if hasattr(self.empty_link, '{}_id'.format(field)):
                        field = '{}_id'.format(field)
                        value = int(value)
                    # if we the filed exists and the value is set add it to the
                    # model creation kwargs
                    if hasattr(self.empty_link, field):
                        kwargs.update({field: value})
        obj = self.link_model(**kwargs)
        href = obj.get_link()
        if hasattr(obj, 'get_css_class'):
            css_class = obj.get_css_class()
        else:
            css_class = ''
        if 'mailto:' in href:
            self._render_email(obj, link, href, css_class)
        else:
            link.set('href', href)
            if hasattr(obj, 'get_target'):
                link.set('target', obj.get_target())
            if css_class:
                link.set('class', css_class)

    def _render_email(self, obj, link, href, css_class=''):
        email = obj.get_email()
        text = link.text or email
        if self.unprotected:
            link.set('href', 'mailto:{}'.format(email))
            if css_class:
                link.set('class', css_class)
        else:
            mail = mail_to_js(email, link_text=text, css_class=css_class)
            link_new = fragment_fromstring(mail)
            link.addnext(link_new)
            link.getparent().remove(link)


def mail_to_js(email, *args, **kwargs):
    result = ''
    text = kwargs.get('link_text', email)
    css_class = kwargs.get('css_class', '')
    email_array_content = ''
    text_array_content = ''

    def r(c):
        return '"' + str(ord(c)) + '",'

    for c in email:
        email_array_content += r(c)
    for c in text:
        text_array_content += r(c)
    id = "_tyjsdfss-" + str(random.randint(1000, 999999999999999999))
    re_email = re.sub(r',$', '', email_array_content)
    re_text = re.sub(r',$', '', text_array_content)
    result = (
        '<span id="%s"><script>'
        'var _tyjsdf=[%s];'
        'var _qplmks=[%s];'
        'var content=('
        '\'<a class="%s" href="&#x6d;&#97;&#105;&#x6c;&#000116;&#111;&#x3a;\''
        ');'
        'for(_i=0;_i<_tyjsdf.length;_i++){'
        'content+=("&#"+_tyjsdf[_i]+";");'
        '}'
        'content+=(\'">\');'
        'for(_i=0;_i<_qplmks.length;_i++){'
        'content+=(\'&#\'+_qplmks[_i]+\';\');'
        '}'
        'content+=(\'</a>\');'
        'document.getElementById(\'%s\').innerHTML=content;'
        '</script></span>'
    ) % (id, re_email, re_text, css_class, id)
    return mark_safe(result)
