from django import template
from applications.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def app(context):
    request = context['id_app']
    app = Apps.objects.get(id=int(request))
    return app

@register.simple_tag()
def cat_list():
    return Categories.objects.all()

@register.simple_tag()
def forms_list():
    return Attform.objects.all()
