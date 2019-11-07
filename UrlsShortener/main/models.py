from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from random import choice
import string


def generate_key():
    chars = string.digits + string.ascii_letters
    return ''.join(choice(chars) for _ in range(6))


class Urls (models.Model):

    long_url = models.URLField(blank=True)
    short_url_key = models.CharField(max_length=6, primary_key=True, default=generate_key)
    reg_date = models.DateTimeField(auto_now=True)
    life_span = models.IntegerField(validators=[MaxValueValidator(365), MinValueValidator(1)])

    def __unicode__(self):
        return '%s  %s' % (self.target, self.key)


