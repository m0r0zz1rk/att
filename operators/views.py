from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.shortcuts import render, HttpResponse
from applications.views import check_auth
from applications.models import *
from expert.models import *
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from itertools import islice
import pylightxl as xl
import re
import random


class AppDetailView(DetailView):
    model = Apps
    context_object_name = 'app'
    template_name = 'operators/apps/appdetail.html'


class AppListView(ListView):
    model = Apps
    context_object_name = 'apps'
    template_name = 'operators/apps/all.html'

    def get_queryset(self):
        qs = Apps.objects.all().order_by('-id')
        for key, value in self.request.GET.items():
            if key == 'per' and value is not None:
                if value != 'Все':
                    per = Periods.objects.get(id=int(value))
                    qs = qs.filter(date_reg__range=(per.date_start_supply, per.date_end_supply))
            if key == 'surname' and value is not None:
                qs = qs.filter(user_profile__surname__contains=value)
            if key == 'name' and value is not None:
                qs = qs.filter(user_profile__name__contains=value)
            if key == 'patronymic' and value is not None:
                qs = qs.filter(user_profile__patronymic__contains=value)
            if key == 'filter_mo' and value is not None:
                qs = qs.filter(user_profile__mo_id=Munobr.objects.get(name_mo=value).id)
            if key == 'oo' and value is not None:
                qs = qs.filter(oo__in=Oo.objects.filter(short_name__contains=value))
            if key == 'filter_subj' and value is not None:
                qs = qs.filter(subj_area_id=Subjareas.objects.get(name=value).id)
            if key == 'filter_pos' and value is not None:
                qs = qs.filter(pos_id=Position.objects.get(name_pos=value).id)
            if key == 'filter_havecat' and value is not None:
                if value != 'Нет':
                    qs = qs.filter(cat_have_id=Categories.objects.get(name_cat=value).id)
                else:
                    qs = qs.filter(cat_have_id=None)
            if key == 'filter_deccat' and value is not None:
                qs = qs.filter(dec_cat_id=Categories.objects.get(name_cat=value).id)
            if key == 'filter_form' and value is not None:
                qs = qs.filter(form_id=Attform.objects.get(name=value).id)
            if key == 'filter_status' and value is not None:
                qs = qs.filter(status=value)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        apps = super().get_queryset()
        mo = apps.order_by().values('user_profile_id').distinct()
        mos = []
        for el in mo:
            mos.append(Munobr.objects.get(id=Profile.objects.get(id=el['user_profile_id']).mo_id).name_mo)
        subj = apps.order_by().values('subj_area_id').distinct()
        subjs = []
        for el in subj:
            subjs.append(Subjareas.objects.get(id=el['subj_area_id']).name)
        pos = apps.order_by().values('pos_id').distinct()
        poss = []
        for el in pos:
            poss.append(Position.objects.get(id=el['pos_id']).name_pos)
        cathave = apps.order_by().values('cat_have_id').distinct()
        cathaves = []
        for el in cathave:
            if el['cat_have_id'] is not None:
                cathaves.append(Categories.objects.get(id=el['cat_have_id']).name_cat)
            else:
                cathaves.append('Нет')
        deccat = apps.order_by().values('dec_cat_id').distinct()
        deccats = []
        for el in deccat:
            deccats.append(Categories.objects.get(id=el['dec_cat_id']).name_cat)
        id_forms = apps.order_by().values('form_id').distinct()
        forms = []
        for el in id_forms:
            forms.append(Attform.objects.get(id=int(el['form_id'])).name)
        status = apps.order_by().values('status').distinct()
        stats = []
        for el in status:
            stats.append(el['status'])
        filter = {
            'mo': mos,
            'subj': subjs,
            'pos': poss,
            'have_cat': cathaves,
            'dec_cat': deccats,
            'forms': forms,
            'status': stats,
        }
        context['filter'] = filter
        if self.request.GET.get('per') is not None and self.request.GET.get('per') != 'Все':
            context['period'] = Periods.objects.get(id=int(self.request.GET.get('per')))
        return context


class ExpertsListView(ListView):
    model = Experts
    context_object_name = 'experts'
    template_name = 'operators/experts/all.html'

    def get_queryset(self):
        qs = Experts.objects.all().order_by('-id')
        for key, value in self.request.GET.items():
            if key == 'filter_mo' and value is not None:
                qs = qs.filter(mo_id=Munobr.objects.get(name_mo=value).id)
            if key == 'filter_subj' and value is not None:
                qs = qs.filter(subj_id=Subjareas.objects.get(name=value).id)
            if key == 'filter_pos' and value is not None:
                qs = qs.filter(pos_id=Position.objects.get(name_pos=value).id)
            if key == 'filter_status' and value is not None:
                if value == 'Активен':
                    qs = qs.filter(status=True)
                else:
                    qs = qs.filter(status=False)
            if key == 'surname' and value is not None:
                qs = qs.filter(surname__contains=value)
            if key == 'name' and value is not None:
                qs = qs.filter(name__contains=value)
            if key == 'patronymic' and value is not None:
                qs = qs.filter(patronymic__contains=value)
            if key == 'oo' and value is not None:
                qs = qs.filter(oo__in=Oo.objects.filter(short_name__contains=value))
            if key == 'snils' and value is not None:
                qs = qs.filter(snils__contains=value)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experts = super().get_queryset()
        mo = experts.order_by().values('mo_id').distinct()
        mos = []
        for el in mo:
            mos.append(Munobr.objects.get(id=el['mo_id']).name_mo)
        subj = experts.order_by().values('subj_id').distinct()
        subjs = []
        for el in subj:
            subjs.append(Subjareas.objects.get(id=el['subj_id']).name)
        pos = experts.order_by().values('pos_id').distinct()
        poss = []
        for el in pos:
            poss.append(Position.objects.get(id=el['pos_id']).name_pos)
        status = experts.order_by().values('status').distinct()
        stats = []
        for el in status:
            if el['status'] is True:
                stats.append('Активен')
            else:
                stats.append('Не активен')
        filter = {
            'mo': mos,
            'subj': subjs,
            'pos': poss,
            'status': stats,
        }
        context['filter'] = filter
        return context


class DistributionListView(ListView):
    model = Distributions
    context_object_name = 'distrib'
    template_name = 'operators/expertise/distrib_list.html'

    def get_queryset(self):
        if self.request.GET.get('period') is not None:
            return Distributions.objects.filter(period_id=int(self.request.GET.get('period'))).order_by('-id')
        else:
            return Distributions.objects.\
                filter(period_id=Periods.objects.latest('id').id).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('period') is not None:
            context['period'] = self.request.GET.get('period')
        else:
            context['period'] = str(Periods.objects.latest('id').id)
        return context


class PeriodsListView(ListView):
    model = Periods
    context_object_name = 'periods'
    template_name = 'operators/periods/all.html'


def main(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    return render(request, 'operators/main.html')


def del_distrib(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    if request.POST.get('del_distrib') is not None:
        dist = Distributions.objects.get(id=int(request.POST.get('del_distrib')))
        app = Apps.objects.get(id=dist.app_id)
        app.status = 'Зарегистрировано'
        app.save()
        dist.delete()
        return HttpResponseRedirect('/operator/distribution_list')
    else:
        return render(request, 'operators/main.html')


def new_distribution(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    if request.POST.get('new_distrib') is None:
        return render(request, 'operators/main.html')
    if request.POST.get('save_distrib') == 'yes':
        id_apps = request.POST.getlist('id_apps')
        if len(id_apps) == 0:
            context = {
                'info': 'Не было отмечено ни одной заявки!'
            }
            return render(request, 'operators/expertise/main.html', context)
        expert = Experts.objects.get(id=int(request.POST.get('expert_id')))
        apps = Apps.objects.filter(id__in=id_apps)
        for el in apps:
            new = Distributions()
            new.period_id = int(request.POST.get('period'))
            new.expert_id = expert.id
            new.app_id = el.id
            new.stage_id = int(request.POST.get('stage'))
            new.save()
            el.status = 'Назначено'
            el.save()
            context = {
                'period': request.POST.get('period')
            }
            return render(request, 'operators/expertise/transit.html', context)
    context = {}
    if request.POST.get('filter_search') is not None:
        if request.POST.get('exp_surname') is not None:
            context['exp_surname'] = request.POST.get('exp_surname')
        if request.POST.get('exp_name') is not None:
            context['exp_name'] = request.POST.get('exp_name')
        if request.POST.get('exp_patronymic') is not None:
            context['exp_patronymic'] = request.POST.get('exp_patronymic')
        if request.POST.get('filter_mo') is not None and len(request.POST.get('filter_mo')) > 0:
            context['filter_mo'] = request.POST.get('filter_mo')
        if request.POST.get('filter_subj') is not None and len(request.POST.get('filter_subj')) > 0:
            context['filter_subj'] = request.POST.get('filter_subj')
        if request.POST.get('filter_pos') is not None and len(request.POST.get('filter_pos')) > 0:
            context['filter_pos'] = request.POST.get('filter_pos')
        if request.POST.get('snils') is not None and len(request.POST.get('snils')) > 0:
            context['exp_snils'] = request.POST.get('exp_snils')
        context['period'] = request.POST.get('period')
        if request.POST.get('app_surname') is not None:
            context['app_surname'] = request.POST.get('app_surname')
        if request.POST.get('app_name') is not None:
            context['app_name'] = request.POST.get('app_name')
        if request.POST.get('app_patronymic') is not None:
            context['app_patronymic'] = request.POST.get('app_patronymic')
        if request.POST.get('filter_app_mo') is not None and len(request.POST.get('filter_app_mo')) > 0:
            context['filter_app_mo'] = request.POST.get('filter_app_mo')
        if request.POST.get('filter_app_subj') is not None and len(request.POST.get('filter_app_subj')) > 0:
            context['filter_app_subj'] = request.POST.get('filter_app_subj')
        if request.POST.get('filter_app_pos') is not None and len(request.POST.get('filter_app_pos')) > 0:
            context['filter_app_pos'] = request.POST.get('filter_app_pos')
        if request.POST.get('filter_app_cat') is not None and len(request.POST.get('filter_app_cat')) > 0:
            context['filter_app_cat'] = request.POST.get('filter_app_cat')
        if request.POST.get('expert') is not None:
            context['expert'] = Experts.objects.get(id=int(request.POST.get('expert')))
        return render(request, 'operators/expertise/manual_distrib.html', context)
    if request.POST.get('id_exp') is not None:
        context = {
            'expert': Experts.objects.get(id=int(request.POST.get('id_exp'))),
            'period': request.POST.get('period'),
        }
        return render(request, 'operators/expertise/manual_distrib.html', context)
    if request.POST.get('type') == 'Ручной':
        context = {
            'period': request.POST.get('period')
        }
        return render(request, 'operators/expertise/manual_distrib.html', context)
    period = Periods.objects.get(id=int(request.POST.get('period')))
    apps = Apps.objects.filter(date_reg__range=(period.date_start_supply, period.date_end_supply))
    if apps.count() == 0:
        context = {
            'info': 'На выбранный период не найдено поданных заявок'
        }
        return render(request, 'operators/expertise/main.html', context)
    experts = Experts.objects.filter(status=True)
    apps_broke = []
    for el in apps:
        id_mo = el.user_profile.mo_id
        id_subj = el.subj_area_id
        id_pos = el.pos_id
        if Munobr.objects.get(id=id_mo).type_mo == 'Гос':
            id_oo = el.oo_id
            exps = experts.exclude(oo_id=id_oo).filter(subj_id=id_subj).filter(pos_id=id_pos)
        else:
            exps = experts.exclude(mo_id=id_mo).filter(subj_id=id_subj).filter(pos_id=id_pos)
        if exps.count() != 0:
            rand_index = random.randint(0, len(exps)-1)
            exp = exps[rand_index]
            new = Distributions()
            new.period_id = int(request.POST.get('period'))
            new.expert_id = exp.id
            new.app_id = el.id
            new.stage_id = int(request.POST.get('stage'))
            try:
                new.save()
                new.refresh_from_db()
                el.status = 'Назначено'
                el.save()
                return render(request, 'operators/expertise/transit.html', {'period': request.POST.get('period')})
            except BaseException:
                fio = el.user_profile.surname+' '+el.user_profile.name+' '+el.user_profile.patronymic
                apps_broke.append(fio+': не удалось сохранить назначение')
        else:
            fio = el.user_profile.surname + ' ' + el.user_profile.name + ' ' + el.user_profile.patronymic
            apps_broke.append(fio + ': не найдено подходящих специалистов предметной области и должности из другого МО')
    if len(apps_broke) > 0:
        context = {
            'apps_broke': apps_broke
        }
    return render(request, 'operators/expertise/main.html', context)


def expertise_main(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    return render(request, 'operators/expertise/main.html')


def period_del(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    if request.POST.get('del_period') is not None:
        Periods.objects.get(id=int(request.POST.get('del_period'))).delete()
        return HttpResponseRedirect('/operator/periods_list')
    else:
        return render(request, 'operators/main.html')


def period_edit(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    if request.POST.get('edit_period') is not None:
        new = Periods.objects.get(id=int(request.POST.get('edit_period')))
        new.name = request.POST.get('name')
        new.date_start_supply = request.POST.get('date_start_supply')
        new.date_end_supply = request.POST.get('date_end_supply')
        new.date_com_miting = request.POST.get('date_com_miting')
        new.date_stat_doc = request.POST.get('date_stat_doc')
        new.date_end_doc = request.POST.get('date_end_doc')
        new.date_start_first = request.POST.get('date_start_first')
        new.date_end_first = request.POST.get('date_end_first')
        new.date_start_second = request.POST.get('date_start_second')
        new.date_end_second = request.POST.get('date_end_second')
        new.date_start_last = request.POST.get('date_start_last')
        new.date_end_last = request.POST.get('date_end_last')
        new.save()
        return HttpResponseRedirect('/operator/periods_list')
    else:
        return render(request, 'operators/main.html')


def period_new(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    if request.POST.get('new_period') is not None:
        new = Periods()
        new.name = request.POST.get('name')
        new.date_start_supply = request.POST.get('date_start_supply')
        new.date_end_supply = request.POST.get('date_end_supply')
        new.date_com_miting = request.POST.get('date_com_miting')
        new.date_stat_doc = request.POST.get('date_stat_doc')
        new.date_end_doc = request.POST.get('date_end_doc')
        new.date_start_first = request.POST.get('date_start_first')
        new.date_end_first = request.POST.get('date_end_first')
        new.date_start_second = request.POST.get('date_start_second')
        new.date_end_second = request.POST.get('date_end_second')
        new.date_start_last = request.POST.get('date_start_last')
        new.date_end_last = request.POST.get('date_end_last')
        new.save()
        return HttpResponseRedirect('/operator/periods_list')
    else:
        return render(request, 'operators/main.html')


def del_app(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    if request.POST.get('del_app') is not None:
        Apps.objects.get(id=int(request.POST.get('del_app'))).delete()
        return HttpResponseRedirect('/operator/apps_list')
    else:
        return render(request, '/operators/main.html')


def del_exp(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    if request.POST.get('del_exp') is not None:
        exp = Experts.objects.get(id=int(request.POST.get('del_exp'))).delete()
        return HttpResponseRedirect('/operator/experts_list')
    else:
        return render(request, 'operators/main.html')


def new_exp(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    if request.POST.get('new_exp') is not None:
        exp = Experts()
        exp.surname = request.POST.get('surname')
        exp.name = request.POST.get('name')
        exp.patronymic = request.POST.get('patronymic')
        exp.mo_id = Munobr.objects.get(name_mo=request.POST.get('mo')).id
        exp.oo_id = Oo.objects.get(short_name=request.POST.get('oo')).id
        exp.subj_id = Subjareas.objects.get(name=request.POST.get('subj')).id
        exp.pos_id = Position.objects.get(name_pos=request.POST.get('pos')).id
        exp.email = request.POST.get('email')
        exp.snils = request.POST.get('snils')
        if request.POST.get('status') == 'Да':
            exp.status = True
        else:
            exp.status = False
        exp.save()
        return HttpResponseRedirect('/operator/experts_list')
    else:
        return render(request, 'operators/main.html')


def edit_exp(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    if request.POST.get('edit_exp') is not None:
        id_exp = int(request.POST.get('edit_exp'))
        exp = Experts.objects.get(id=id_exp)
        exp.surname = request.POST.get('surname')
        exp.name = request.POST.get('name')
        exp.patronymic = request.POST.get('patronymic')
        exp.mo_id = Munobr.objects.get(name_mo=request.POST.get('mo')).id
        exp.oo_id = Oo.objects.get(short_name=request.POST.get('oo')).id
        exp.subj_id = Subjareas.objects.get(name=request.POST.get('subj')).id
        exp.pos_id = Position.objects.get(name_pos=request.POST.get('pos')).id
        exp.email = request.POST.get('email')
        exp.snils = request.POST.get('snils')
        if request.POST.get('status') == 'Да':
            exp.status = True
        else:
            exp.status = False
        exp.save()
        return HttpResponseRedirect('/operator/experts_list')
    else:
        return render(request, 'operators/main.html')


def import_exp(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    if request.POST.get('import_exp') is not None:
        file = xl.readxl(request.FILES['excel'])
        worksheets = file.ws_names
        error = []
        for sheet in worksheets:
            cols = file.ws(ws=sheet).cols
            index_fio = None
            index_mo = None
            index_oo = None
            index_subj = None
            index_pos = None
            index_email = None
            index_snils = None
            el = 1
            for col in cols:
                if str(file.ws(ws=sheet).index(row=1, col=el)) == 'ФИО':
                    index_fio = el
                if str(file.ws(ws=sheet).index(row=1, col=el)) == 'МО':
                    index_mo = el
                if str(file.ws(ws=sheet).index(row=1, col=el)) == 'ОО':
                    index_oo = el
                if str(file.ws(ws=sheet).index(row=1, col=el)) == 'Предметная область':
                    index_subj = el
                if str(file.ws(ws=sheet).index(row=1, col=el)) == 'Должность':
                    index_pos = el
                if str(file.ws(ws=sheet).index(row=1, col=el)) == 'Электронная почта':
                    index_email = el
                if str(file.ws(ws=sheet).index(row=1, col=el)) == 'СНИЛС':
                    index_snils = el
                el += 1
            if index_fio is None:
                error.append('Не найден столбец "ФИО"')
            if index_mo is None:
                error.append('Не найден столбец "МО"')
            if index_oo is None:
                error.append('Не найден столбец "ОО"')
            if index_subj is None:
                error.append('Не найден столбец "Предметная область"')
            if index_pos is None:
                error.append('Не найден столбец "Должность"')
            if index_email is None:
                error.append('Не найден столбец "Электронная почта"')
            if index_snils is None:
                error.append('Не найден столбец "СНИЛС"')
            if len(error) > 0:
                context = {
                    'error': error
                }
                return render(request, 'operators/experts/import_errors.html', context)
            rows = file.ws(ws=sheet).rows
            i = 2
            for row in islice(rows, 1, None):
                error_add = ""
                exfio = str(file.ws(ws=sheet).index(row=i, col=index_fio))
                cor_str = exfio.strip()
                fio = re.split(' |\n', cor_str)
                if len(fio) >= 3:
                    surname = fio[0]
                    name = fio[1]
                    patronymic = fio[2]
                elif len(fio) == 2:
                    surname = fio[0]
                    name = fio[1]
                else:
                    surname = fio[0]
                mo = str(file.ws(ws=sheet).index(row=i, col=index_mo))
                pos = str(file.ws(ws=sheet).index(row=i, col=index_pos))
                subj = str(file.ws(ws=sheet).index(row=i, col=index_subj))
                oo = str(file.ws(ws=sheet).index(row=i, col=index_oo))
                check_error = len(error)
                try:
                    id_mo = Munobr.objects.get(name_mo=mo).id
                except BaseException:
                    error.append(exfio + ": не найдено МО '" + mo + "'")
                try:
                    id_pos = Position.objects.get(name_pos=pos).id
                except BaseException:
                    error.append(exfio + ": не найдена должность '" + pos + "'")
                try:
                    id_subj = Subjareas.objects.get(name=subj).id
                except BaseException:
                    try:
                        id_subj = Subjareas.objects.get(name=subj.lower()).id
                    except BaseException:
                        error.append(exfio + ": не найдена предметная область '" + subj + "'")
                try:
                    id_oo = Oo.objects.get(full_name=oo).id
                except BaseException:
                    try:
                        id_oo = Oo.objects.get(short_name=oo).id
                    except BaseException:
                        error.append(exfio + ": не найдена образовательая организация '" + oo + "'")
                if check_error == len(error):
                    rec = str(file.ws(ws=sheet).index(row=i, col=index_snils)).strip()
                    snils = rec[:3] + "-" + rec[3:6] + "-" + rec[6:9] + " " + rec[:2]
                    new_exp = Experts()
                    new_exp.surname = surname
                    new_exp.name = name
                    new_exp.patronymic = patronymic
                    new_exp.mo_id = id_mo
                    new_exp.oo_id = id_oo
                    new_exp.subj_id = id_subj
                    new_exp.pos_id = id_pos
                    new_exp.email = str(file.ws(ws=sheet).index(row=i, col=index_email)).strip()
                    new_exp.snils = snils
                    try:
                        new_exp.save()
                    except BaseException:
                        error_add = "Ошибка при попытке загрузить специалиста (возможно дубль СНЛИС): " + fio
                i += 1
                if len(error_add) != 0:
                    error.append(error_add)
            error.append(str(i))
        if len(error) > 0:
            return render(request, 'operators/experts/import_errors.html', {'error': error})
        return HttpResponseRedirect('/operator/experts_list')
    else:
        return render(request, 'operators/main.html')


# Create your views here.
