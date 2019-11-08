from django.contrib import admin
from django.urls import path, include

from main.views import (main_view,
                        short_url_view,
                        redirect_view,
                        UrlsApi,
                        )

urlpatterns = [
    path('', main_view, name='main'),
    path('shortUrl', short_url_view, name='short_url'),
    path('<short_url_key>', redirect_view, name='redirect'),

    path('api/', UrlsApi.as_view()),
    path('api/<str:key>', UrlsApi.as_view()),
    ]