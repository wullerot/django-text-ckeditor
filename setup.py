from setuptools import setup, find_packages
import os

version = __import__('text_ckeditor').__version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

DESCRIPTION = 'CKEditor Textarea widget for rouxcode & e621'

setup(
    name="django-text-ckeditor",
    version=version,
    url='http://github.com/rouxcode/django-text-ckeditor',
    license='MIT',
    platforms=['OS Independent'],
    description="text_ckeditor",
    long_description=read('README.rst'),
    author=u'Alaric Maegerle',
    author_email='info@rouxcode.ch',
    packages=find_packages(),
    install_requires=(
        'Django>=1.8',
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
