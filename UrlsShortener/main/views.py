import threading
import time as t
from datetime import datetime
from main.models import Urls
from django.shortcuts import render
from django.http import JsonResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UrlsSerializer

# Removing obsolete links, circus in 10 minutes
def time_check():
    date_format = "%d/%m/%Y %H:%M"
    while True:
        objs = Urls.objects.all()
        now = datetime.strptime('{0}/{1}/{2} {3}:{4}'.format(datetime.now().day,
                                                     datetime.now().month,
                                                     datetime.now().year,
                                                     datetime.now().hour,
                                                     datetime.now().month),
                                date_format)
        for obj in objs:
            set = datetime.strptime('{0}/{1}/{2} {3}:{4}'.format(obj.reg_date.day,
                                                         obj.reg_date.month,
                                                         obj.reg_date.year,
                                                         obj.reg_date.hour,
                                                         obj.reg_date.month),
                                  date_format)

            if (now - set).days - obj.life_span == 0:
                obj.delete()
        t.sleep(600)


tChThr = threading.Thread(target=time_check, name='tchThr')
tChThr.start()

# Site domain name
DOMAIN_NAME = 'http://127.0.0.1:8000/'


def redirect_view(request, short_url_key):
    target = get_object_or_404(Urls, short_url_key=short_url_key)
    return HttpResponseRedirect(target.long_url)

# Data Validator
def validator(long_url, life_span):
    try:
        validate = URLValidator(schemes=('http', 'https', 'ftp', 'ftps', 'rtsp', 'rtmp'))
        validate(long_url)
    except ValidationError:
        return {"code": "400", "description": "Invalid URL"}
    print(DOMAIN_NAME, " ", long_url)
    if DOMAIN_NAME in long_url.lower():
        print(DOMAIN_NAME, " ",  long_url)
        return {"code": "400", "description": "Invalid URL"}
    url_len = len(long_url)
    if url_len < 20:
        return {"code": "411", "description": "URL must be longer than 20 characters"}

    try:
        life_span = int(life_span)
        if life_span < 1 or life_span > 365:
            return {"code": "400", "description": "Invalid range"}
    except:
        return {"code": "400", "description": "Invalid input"}

    return {"code": "200", "description": "OK"}


def make_short_url(long_url, life_span):
    short_url = Urls.objects.get_or_create(long_url=long_url, life_span=life_span)[0]
    short_url.save()
    return short_url


def short_url_view(request):
    long_url = request.GET.get('long_url')
    life_span = int(request.GET.get('life_span'))
    req = validator(long_url, life_span)

    if req['code'] == "200":
        short_url = DOMAIN_NAME + '%s' % make_short_url(long_url, life_span).short_url_key
        res = {"req": req, "short_url": short_url}
    else:
        res = {"req": req}

    return JsonResponse(res)


def main_view(request):
    ranges = [i for i in range(1, 365)]
    context = {
        'ranges': ranges,
    }
    return render(request, 'wrapper.html', context)


# API
class UrlsApi(APIView):

    # Get the original address by key
    def get(self, request, key):
        target = Urls.objects.filter(short_url_key=key)
        serializer = UrlsSerializer(target, many=True)
        if len(serializer.data) == 0:
            res = {"code": "404", "description": "Nothing found"}
        else:
            res = {"url": serializer.data}
        return Response(res)

    # Short address creation
    def post(self, request):
        article = request.data.get('url')
        long_url = article['long_url']
        life_span = article['life_span']
        req = validator(long_url, life_span)
        if req['code'] == "200":
            short_url = make_short_url(long_url, life_span)
            return self.get(request, short_url.short_url_key)
        else:
            return Response(req)
