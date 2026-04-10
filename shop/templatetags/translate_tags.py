from django import template
from django.utils.safestring import mark_safe
from shop.translations import get_translation

register = template.Library()

@register.simple_tag
def t(text, language=None):
    """
    Translate text based on current language
    Usage: {% t 'Home' %}
    """
    if language is None:
        # This will be set in context processor
        language = 'bn'
    return get_translation(text, language)

@register.filter
def translate_text(text, language='bn'):
    """Filter version of translation"""
    return get_translation(text, language)
