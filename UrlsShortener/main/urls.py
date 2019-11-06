from django.contrib import admin
from django.urls import path, include

from main.views import (main_view,
                        )

urlpatterns = [
    path('', main_view, name='main'),

    ]