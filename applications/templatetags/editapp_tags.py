from django import template
from applications.models import *
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag(takes_context=True)
def get_profile(context):
    request = context['request']
    prof = Profile.objects.get(user_id = User.objects.get(id=request.user.id))
    return prof

@register.simple_tag(takes_context=True)
def get_mail(context):
    request = context['request']
    mail = User.objects.get(id=request.user.id).email
    return mail

@register.simple_tag(takes_context=True)
def get_infoapp(context):
    id_app = context['id_app']
    app = Apps.objects.get(id=id_app)
    return app

@register.simple_tag(takes_context=True)
def get_oos(context):
    request = context['request']
    id_mo = Profile.objects.get(user_id=User.objects.get(id=request.user.id)).mo_id
    return Oo.objects.filter(mo_id=id_mo)

@register.simple_tag()
def get_subjareas():
    return Subjareas.objects.all()

@register.simple_tag()
def get_pos():
    return Position.objects.all()