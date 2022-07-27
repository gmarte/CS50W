from atexit import register
from distutils import extension
import markdown2

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def convert_markdown(value):
    return markdown2.markdown(value, extras=['fenced-code-blocks'])
