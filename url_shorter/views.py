import django.contrib.sessions.backends.db
import json
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import ShortenedLink
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import helper
import redis
from django.conf import settings
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from .core.views import base_view
from .core.exceptions import EmptyUrlException


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, 
                                   db=0)
@base_view
@require_http_methods(["GET"])
def index(request):
    shorten_links = ShortenedLink.objects.filter(session_id=request.session.session_key)
    paginator = Paginator(shorten_links, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    shortened_link = request.GET.get('shortened_link')
    exception = request.GET.get('exception')

    return render(request, 'index.html', {
        'shortened_link': shortened_link,
        'shorten_links': shorten_links,
        'page_obj': page_obj,
        'exception': exception
    })
    
@base_view
@require_http_methods(["POST"])
@csrf_exempt
def shorten_url(request):
    if not request.session.session_key:
        request.session.save()

    original_link = request.POST.get('url')
    subpart = request.POST.get('subpart')
    if not original_link:
        raise EmptyUrlException("URL is empty")
    shortened_link = helper.create_shorten_link(original_link, request.session.session_key, subpart = subpart)
    return redirect(reverse('index')+'?shortened_link='+shortened_link)

@base_view
def redirect_by_short_link(request, subpart):

    original_link = redis_instance.get(subpart)
    if not original_link:
        shortened_link = get_object_or_404(ShortenedLink, pk=subpart)
        original_link = shortened_link.original_link
        redis_instance.set(subpart, original_link, ex=6000)

    return redirect(original_link)




