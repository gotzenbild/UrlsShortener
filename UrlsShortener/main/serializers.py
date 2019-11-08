from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from main.models import Urls, generate_key



class UrlsSerializer(serializers.Serializer):
    long_url = serializers.URLField()
    short_url_key = serializers.CharField(max_length=6, default=generate_key)
    reg_date = serializers.DateTimeField()
    life_span = serializers.IntegerField(validators=[MaxValueValidator(365), MinValueValidator(1)])