from django import template
from applications.models import *
from expert.models import *
from operators.models import *
from django.shortcuts import HttpResponse

register = template.Library()


@register.simple_tag(takes_context=True)
def get_results(context):
    apps = context['apps']
    request = context['request']
    ids = []
    for app in apps:
        ids.append(app.id)
    return AppResult.objects.filter(app_id__in=ids).filter(expert_id=Experts.objects.get(snils=request.user.username))