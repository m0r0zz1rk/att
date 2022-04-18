from django import template
from applications.middleware import *

register = template.Library()


@register.simple_tag(takes_context=True)
def check_net(context):
    request = context['request']
    return check_network(request)

@register.simple_tag(takes_context=True)
def get_adinfo(context):
    request = context['request']
    try:
        from_ad = GetDataFromAD(request)
        username = from_ad[0][0]
        group = from_ad[1][0]
        return {'username': username, 'group': group}
    except BaseException:
        return None