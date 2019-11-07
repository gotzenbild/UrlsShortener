import re
import urllib.parse
import urllib.request
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def main_view(request):
    return render(request, 'wrapper.html')

chars = ['0','1','2','3','4','5','6','7','8','9','']
def make_short_url(long_url):

    url_len = len(long_url)
    if re.match("^https?://[^ ]+", long_url) and url_len > 20:
        apiURL = urllib.parse.urlencode(dict(longURL=long_url))
        print(apiURL)
    return apiURL;


def short_url_view(request):
    long_url = request.GET.get('long_url')
    life_span = request.GET.get('life_span')
    short_url = make_short_url(long_url)

    return JsonResponse({
        "short_url": short_url
    })
