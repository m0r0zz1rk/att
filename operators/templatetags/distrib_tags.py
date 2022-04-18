from django import template
from expert.models import *
from operators.models import *
from applications.models import *

register = template.Library()


@register.simple_tag(takes_context=True)
def apps_list(context):
    period = Periods.objects.get(id=int(context['period']))
    apps = Apps.objects.filter(date_reg__range=(period.date_start_supply, period.date_end_supply))
    for dict in context:
        for key, value in dict.items():
            if key == 'filter_app_mo' and value is not None:
                apps = apps.filter(user_profile__mo_id=Munobr.objects.get(name_mo=value).id)
            if key == 'filter_app_subj' and value is not None:
                apps = apps.filter(subj_area_id=Subjareas.objects.get(name=value).id)
            if key == 'filter_app_pos' and value is not None:
                apps = apps.filter(pos_id=Position.objects.get(name_pos=value).id)
            if key == 'filter_app_cat' and value is not None:
                apps = apps.filter(dec_cat_id=Categories.objects.get(name_cat=value).id)
            if key == 'app_surname' and value is not None:
                apps = apps.filter(user_profile__surname__contains=value)
            if key == 'app_name' and value is not None:
                apps = apps.filter(user_profile__name__contains=value)
            if key == 'app_patronymic' and value is not None:
                apps = apps.filter(user_profile__patronymic__contains=value)
    return apps


@register.simple_tag(takes_context=True)
def experts_list(context):
    experts = Experts.objects.filter(status=True)
    for dict in context:
        for key, value in dict.items():
            if key == 'filter_mo' and value is not None:
                experts = experts.filter(mo_id=Munobr.objects.get(name_mo=value).id)
            if key == 'filter_subj' and value is not None:
                experts = experts.filter(subj_id=Subjareas.objects.get(name=value).id)
            if key == 'filter_pos' and value is not None:
                experts = experts.filter(pos_id=Position.objects.get(name_pos=value).id)
            if key == 'exp_surname' and value is not None:
                experts = experts.filter(surname__contains=value)
            if key == 'exp_name' and value is not None:
                experts = experts.filter(name__contains=value)
            if key == 'exp_patronymic' and value is not None:
                experts = experts.filter(patronymic__contains=value)
            if key == 'exp_snils' and value is not None:
                experts = experts.filter(snils=value)
    return experts


@register.simple_tag(takes_context=True)
def filter_exp(context):
    try:
        experts = context['experts']
        id_mos = experts.order_by().values('mo').distinct()
        mo = []
        for el in id_mos:
            mo.append(Munobr.objects.get(id=int(el['mo'])).name_mo)
        id_subj = experts.order_by().values('subj').distinct()
        subj = []
        for el in id_subj:
            subj.append(Subjareas.objects.get(id=int(el['subj'])).name)
        id_pos = experts.order_by().values('pos').distinct()
        pos = []
        for el in id_pos:
            pos.append(Position.objects.get(id=int(el['pos'])).name_pos)
        return {
            'mo': mo,
            'subj': subj,
            'pos': pos,
        }
    except BaseException:
        pass


@register.simple_tag(takes_context=True)
def filter_apps(context):
    try:
        apps = context['apps']
        id_mos = apps.order_by().values('user_profile_id').distinct()
        mo = []
        for el in id_mos:
            mo.append(Munobr.objects.get(id=Profile.objects.get(id=int(el['user_profile_id'])).mo_id).name_mo)
        id_subj = apps.order_by().values('subj_area_id').distinct()
        subj = []
        for el in id_subj:
            subj.append(Subjareas.objects.get(id=int(el['subj_area_id'])).name)
        id_pos = apps.order_by().values('pos_id').distinct()
        pos = []
        for el in id_pos:
            pos.append(Position.objects.get(id=int(el['pos_id'])).name_pos)
        id_cat = apps.order_by().values('dec_cat_id').distinct()
        dec_cat = []
        for el in id_cat:
            dec_cat.append(Categories.objects.get(id=int(el['dec_cat_id'])).name_cat)
        return {
            'mo': mo,
            'subj': subj,
            'pos': pos,
            'dec_cat': dec_cat,
        }
    except BaseException:
        pass


@register.simple_tag(takes_context=True)
def distrib_list(context):
    id_period = context['period']
    return Distributions.objects.filter(period_id=id_period).order_by('-id')


@register.simple_tag
def stages_list():
    return Stages.objects.all()


@register.simple_tag(takes_context=True)
def stages_count(context):
    stages = Stages.objects.all()
    distribs = context['distrib']
    dict = {}
    for el in stages:
        if el.name_stage != 'Оператор':
            dict[el.id] = distribs.filter(stage_id=el.id).count()
    return dict


@register.simple_tag()
def experts_distib():
    return Experts.objects.all()


@register.simple_tag()
def apps_distib():
    return Apps.objects.all()


@register.simple_tag(takes_context=True)
def period_info(context):
    return Periods.objects.get(id=int(context['period']))