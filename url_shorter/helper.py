import json
from django.conf import settings
from test_task.settings import SITE_URL
from .models import ShortenedLink
from django.utils import timezone
from django.utils.crypto import get_random_string
from .core.exceptions import SubpartAlreadyExistsException



def create_shorten_link(original_link, session_key, subpart=None):
    subpart = subpart if subpart else get_random_string(length=5)

    if ShortenedLink.objects.filter(pk=subpart).exists():
        raise SubpartAlreadyExistsException("such subpart alredy exists")

    shortened_link = ShortenedLink(
        original_link=original_link,
        session_id = session_key, 
        subpart = subpart
        )
    shortened_link.save()
    return shortened_link.get_full_link()

