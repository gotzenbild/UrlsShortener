from sqlite3 import IntegrityError

from main.models import Urls
from django.shortcuts import render
from django.http import JsonResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404



DOMAIN_NAME = 'http://127.0.0.1:8000/'

def redirect_view(request, short_url_key):
    target = get_object_or_404(Urls, short_url_key=short_url_key)
    return HttpResponseRedirect(target.long_url)



def main_view(request):
    return render(request, 'wrapper.html')


def validator(long_url):

    try:
        validate = URLValidator(schemes=('http', 'https', 'ftp', 'ftps', 'rtsp', 'rtmp'))
        validate(long_url)
    except ValidationError:
        return "400"

    url_len = len(long_url)
    if url_len < 20:
        return "411"

    return "200"

def make_short_url(long_url, life_span):
    short_url = Urls.objects.get_or_create(long_url=long_url, life_span=life_span)[0]
    short_url.save()
    return DOMAIN_NAME + '%s' % short_url.short_url_key


def short_url_view(request):

    long_url = request.GET.get('long_url')
    life_span = request.GET.get('life_span')

    req = validator(long_url)
    if req == "200":
        short_url = make_short_url(long_url, life_span)

    else:
        short_url = long_url

    return JsonResponse({
        "req": req,
        "short_url": short_url
    })
