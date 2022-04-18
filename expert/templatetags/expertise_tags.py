from django import template
from expert.models import *
from applications.models import *

register = template.Library()


@register.simple_tag(takes_context=True)
def get_stages(context):
    return Stages.objects.all()


@register.simple_tag(takes_context=True)
def change_status(context):
    app = context['app']
    curr_app = Apps.objects.get(id=app.id)
    curr_app.status = 'На экспертизе'
    curr_app.save()
    return None


@register.simple_tag(takes_context=True)
def get_marks(context):
    app = context['app']
    marks = Marks.objects.filter(pos_id=int(app.pos_id))
    dict = {}
    for el in marks:
        marks = el.mark_list.split(",")
        dict[el.criteria.name+" - "+el.criteria.description] = marks
    return dict


@register.simple_tag(takes_context=True)
def get_have_marks(context):
    app = context['app']
    request = context['request']
    recs = ExpertMarks.objects.filter(app_id=app.id).\
        filter(expert_id=Experts.objects.get(snils=request.user.username).id)
    if recs.count() == 0:
        return None
    dict = {}
    for el in recs:
        dict[el.criteria.name+" - "+el.criteria.description] = [el.mark, el.info]
    return dict


@register.simple_tag(takes_context=True)
def get_appres(context):
    app = context['app']
    request = context['request']
    dict = {}
    try:
        appres = AppResult.objects.\
            filter(expert_id=Experts.objects.get(snils=request.user.username)).get(app_id=app.id).total_mark
        dict['res'] = appres
    except BaseException:
        pass
    dict['total'] = Total.objects.filter(cat_id=app.dec_cat_id).get(pos_id=app.pos_id).total
    return dict