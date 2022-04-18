from django import template
from applications.models import *
from operators.models import *

register = template.Library()


@register.simple_tag()
def profiles_list():
    return Profile.objects.all()


@register.simple_tag()
def periods_list():
    return Periods.objects.all()


