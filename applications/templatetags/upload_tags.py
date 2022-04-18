from django import template
from applications.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def get_crit(context):
    request = context['id_crit']
    criteria = Criterias.objects.get(id=int(request))
    return criteria

@register.simple_tag(takes_context=True)
def get_path(context):
    id_app = context['id_app']
    id_crit = context['id_crit']
    try:
        path = AppCritFile.objects.filter(app_id=id_app).get(criteria_id=id_crit).file.path
    except BaseException:
        path = None
    return path