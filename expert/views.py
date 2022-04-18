from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from .models import *
from applications.models import *
from operators.models import *
from django.views.generic.detail import DetailView
from django.views.generic import ListView


class ArchiveApps(ListView):
    model = Apps
    context_object_name = 'apps'
    template_name = 'expert/expertise/archiveapps.html'

    def get_queryset(self):
        id_exp = Experts.objects.get(snils=self.request.user.username)
        distribs = Distributions.objects.filter(expert_id=id_exp)
        list_apps = []
        for el in distribs:
            list_apps.append(el.app_id)
        return Apps.objects.filter(id__in=list_apps).exclude(status__in=['Назначено', 'На экспертизе'])

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
        return context


class DistribAppDetailView(DetailView):
    model = Apps
    context_object_name = 'app'
    template_name = 'expert/expertise/expertise.html'


class DistribAppsListView(ListView):
    model = Apps
    context_object_name = 'apps'
    template_name = 'expert/expertise/appslist.html'

    def get_queryset(self):
        id_exp = Experts.objects.get(snils=self.request.user.username)
        distribs = Distributions.objects.filter(expert_id=id_exp)
        list_apps = []
        for el in distribs:
            list_apps.append(el.app_id)
        return Apps.objects.filter(id__in=list_apps).filter(status__in=['Назначено', 'На экспертизе'])

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
        return context


def check_auth(request):
    if request.user.is_authenticated:
        return True
    else:
        return False


def recalc_total(id_app, id_exp):
    try:
        rec = AppResult.objects.filter(expert_id=id_exp).get(app_id=id_app)
    except BaseException:
        new = AppResult()
        new.expert_id = id_exp
        new.app_id = id_app
        new.total_mark = 0
        new.result = 'Создано'
        new.save()
        rec = AppResult.objects.get(id=new.id)
    app = Apps.objects.get(id=id_app)
    total = Total.objects.filter(cat_id=app.dec_cat_id).get(pos_id=app.pos_id).total
    count = 0
    marks = ExpertMarks.objects.filter(expert_id=id_exp).filter(app_id=id_app)
    for el in marks:
        count += el.mark
    rec.total_mark = count
    if count >= total:
        rec.result = 'Установить'
    else:
        rec.result = 'Отказать'
    rec.save()
    return None


def add_mark(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    if request.POST.get('app') is not None:
        id_app = int(request.POST.get('app'))
        crit_name = request.POST.get('crit').split(' - ')[0]
        crit_descrpition = request.POST.get('crit').split(' - ')[1]
        id_crit = Criterias.objects.filter(name=crit_name).get(description=crit_descrpition).id
        id_expert = Experts.objects.get(snils=request.user.username).id
        try:
            check = ExpertMarks.objects.filter(app_id=id_app).filter(expert_id=id_expert).get(criteria_id=id_crit)
            check.delete()
        except BaseException:
            pass
        new = ExpertMarks()
        new.expert_id = id_expert
        new.app_id = id_app
        new.criteria_id = id_crit
        new.mark = int(request.POST.get('mark'))
        new.info = request.POST.get('info')
        new.save()
        new.refresh_from_db()
        recalc_total(id_app, id_expert)
        return HttpResponseRedirect('/expert/app_expertise/'+request.POST.get('app')+'#'+request.POST.get('anchor'))
    else:
        return render(request, 'expert/expertise/main.html')


def expertise(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    return render(request, 'expert/expertise/main.html')


def main(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    return render(request, 'expert/main.html')


def profile(request):
    if check_auth(request) is False:
        return render(request, 'auth/login.html')
    expert = Experts.objects.get(snils=request.user.username)
    if request.method == 'POST':
        return HttpResponse('YES')
    context = {
        'expert': expert,
    }
    return render(request, 'profile/profile_exp.html', context)

# Create your views here.
