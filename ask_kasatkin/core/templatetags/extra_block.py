from django import template
from django.core.cache import cache

register = template.Library()

# load "popular_users", "popular_tags" from cache, render

