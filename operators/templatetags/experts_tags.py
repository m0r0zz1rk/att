from django import template
from expert.models import *
from applications.models import *

register = template.Library()


@register.simple_tag()
def mo_list():
    return Munobr.objects.all()


@register.simple_tag()
def oo_list():
    return Oo.objects.all().order_by('-id')


@register.simple_tag()
def pos_list():
    return Position.objects.all()


@register.simple_tag()
def subj_list():
    return Subjareas.objects.all()


