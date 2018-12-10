import hashlib
from urllib.parse import urlencode

from django import template
from django.conf import settings

register = template.Library()
import libgravatar

@register.filter
def gravatar(user):
    email = user.email.lower()
    default = 'mm'
    size = 75
    url = 'https://www.gravatar.com/avatar/{md5}'.format(
        md5=libgravatar.md5_hash(email)
    )
    return url