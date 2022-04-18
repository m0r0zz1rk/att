from django import template
from expert.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def get_group(context):
    request = context['request']
    try:
        group = request.user.groups.values_list('name', flat=True)
        return group[0]
    except BaseException:
        return 'Оператор'


@register.simple_tag(takes_context=True)
def get_username(context):
    request = context['request']
    exp = Experts.objects.get(snils=request.user.username)
    usname = exp.surname+" "+exp.name[:1]+"."+exp.patronymic[:1]+"."
    return usname
