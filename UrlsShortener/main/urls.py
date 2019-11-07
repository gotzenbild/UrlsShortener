from django.contrib import admin
from django.urls import path, include

from main.views import (main_view,
                        short_url_view,
                        )

urlpatterns = [
    path('', main_view, name='main'),
    path('short_url', short_url_view, name='short_url')
    ]