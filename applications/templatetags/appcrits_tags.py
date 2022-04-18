from django import template
from applications.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def crits_list(context):
    """request = context['request']
    prof = Profile.objects.get(user_id=request.user.id)
    pos = Position.objects.get(id=Apps.objects.filter(user_profile_id=prof.id).latest('id').pos_id)
    crits = PosCriterias.objects.get(pos_id=pos.id).crits.all()"""
    id_app = context['id_app']
    pos = Position.objects.get(id=Apps.objects.get(id=id_app).pos_id)
    crits = PosCriterias.objects.get(pos_id=pos.id).crits.all()
    return crits

@register.simple_tag(takes_context=True)
def get_app_status(context):
    id_app = context['id_app']
    status = Apps.objects.get(id=int(id_app)).status
    return status

@register.simple_tag()
def get_criterias():
    return Criterias.objects.all()