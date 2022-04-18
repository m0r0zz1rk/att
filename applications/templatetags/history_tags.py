from django import template
from applications.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def apps_list(context):
    request = context['request']
    prof = Profile.objects.get(user_id=request.user.id)
    apps = Apps.objects.filter(user_profile_id=prof.id).order_by('-id')
    return apps
