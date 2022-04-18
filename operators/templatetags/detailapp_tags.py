from django import template
from applications.models import *
from expert.models import Total
from operators.models import *
from django.shortcuts import HttpResponse

register = template.Library()


@register.simple_tag(takes_context=True)
def get_total(context):
    app = context['app']
    return Total.objects.filter(cat_id=app.dec_cat_id).get(pos_id=app.pos_id).total


@register.filter
def list_item(lst, i):
    try:
        return lst[i]
    except:
        return None


