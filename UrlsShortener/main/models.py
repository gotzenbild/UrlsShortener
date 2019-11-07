from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Urls (models.Model):

    long_url = models.TextField()
    short_url = models.TextField()
    reg_date = models.DateTimeField(auto_now=True)
    life_span = models.IntegerField(validators=[MaxValueValidator(365), MinValueValidator(1)])
