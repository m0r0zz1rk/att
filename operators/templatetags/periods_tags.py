from django import template
from applications.models import *
from operators.models import *

register = template.Library()

@register.simple_tag()
def periods_list():
    return Periods.objects.all().order_by('-id')