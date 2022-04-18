from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.shortcuts import render, HttpResponse
from django.http import FileResponse
from django.conf import settings
from itertools import islice
from ftplib import FTP
from .forms import UploadForm
from .models import *
from .serializers import *
import pylightxl as xl
from expert.models import Experts
from .middleware import *
from expert.views import main as expmain
import secrets
import string
from datetime import date
from operators.models import *
from collections import namedtuple


nt = namedtuple('object', ['model', 'serializers'])
pattern = {
    'type_oo': nt(type_oo, TypeOoSerializer),
    'position': nt(Position, PositionSerializer),
    'munobr': nt(Munobr, MunobrSerializer),
    'attform': nt(Attform, AttformSerializer),
    'attcategory': nt(Categories, AttcategoriesSerializer),
    'oo': nt(Oo, OoSerializer),
}

@api_view(['GET', 'POST'])
def ListView(request, api_name):
    object = pattern.get(api_name, None)
    if object == None:
        return Response(
            data = 'Invalid URL',
            status = status.HTTP_404_NOT_FOUND,
        )
    if request.method == 'GET':
        object_list = object.model.objects.all()
        serializers = object.serializers(object_list, many=True)
        return Response(serializers.data)
    if request.method == 'POST':
        data = request.data
        serializers = object.serializers(data=data)
        if not serializers.is_valid():
            return Response(
                data = serializers.error,
                status = status.HTTP_404_NOT_FOUND,
            )
        serializers.save()
        return Response(
            data = serializers.error,
            status = status.HTTP_201_CREATED
        )


def import_oo(request):
    if request.method == 'POST':
        file = xl.readxl(request.FILES['excel'])
        name_sheet = file.ws_names[0]
        i = 1
        while i<15:
            if file.ws(ws=name_sheet).index(row=1, col=i) == 'Полное наименование ОО':
                index_fullname = i
            elif file.ws(ws=name_sheet).index(row=1, col=i) == 'Краткое наименование ОО':
                index_shortname = i
            elif file.ws(ws=name_sheet).index(row=1, col=i) == 'Адрес ОО':
                index_address = i
            elif file.ws(ws=name_sheet).index(row=1, col=i) == 'Телефон ОО':
                index_phone = i
            elif file.ws(ws=name_sheet).index(row=1, col=i) == 'Почта ОО':
                index_mail = i
            elif file.ws(ws=name_sheet).index(row=1, col=i) == 'Сайт ОО':
                index_url = i
            elif file.ws(ws=name_sheet).index(row=1, col=i) == 'МО ОО':
                index_mo = i
            else:
                pass
            i += 1
        rows = file.ws(ws=name_sheet).rows
        i = 2
        for row in islice(rows, 2, None):
            mo = file.ws(ws=name_sheet).index(row=i, col=index_mo)
            if mo != '' and type(mo) == int :
                mo_id = int(file.ws(ws=name_sheet).index(row=i, col=index_mo))
                rec = Oo()
                if mo_id > 50:
                    mo_id = 46
                rec.mo_id = mo_id
                fn = file.ws(ws=name_sheet).index(row=i, col=index_fullname)
                if fn is not None:
                    rec.full_name = fn
                sn = file.ws(ws=name_sheet).index(row=i, col=index_shortname)
                if sn is not None:
                    if len(sn) > 150:
                        rec.short_name = sn[:150]
                    else:
                        rec.short_name = sn
                rec.address = file.ws(ws=name_sheet).index(row=i, col=index_address)
                rec.phone = file.ws(ws=name_sheet).index(row=i, col=index_phone)
                rec.email = file.ws(ws=name_sheet).index(row=i, col=index_mail)
                rec.url = file.ws(ws=name_sheet).index(row=i, col=index_url)
                if fn.find('пециальное') != -1 or fn.find('пециального') != -1 or \
                        fn.find('пециальная') != -1:
                    rec.type_id = type_oo.objects.get(name='СПО').id
                elif fn.find('ополнительного') != -1 :
                    rec.type_id = type_oo.objects.get(name='ОДО').id
                elif fn.find('бщеобразовательное') != -1 or fn.find('бщеобразовательная') != -1 or \
                        fn.find('бщеобразовательного') != -1 :
                    rec.type_id = type_oo.objects.get(name='ОО').id
                elif fn.find('ошкольное') != -1 or fn.find('ошкольная') != -1 or fn.find('ошкольного') != -1 :
                    rec.type_id = type_oo.objects.get(name='ДОО').id
                else:
                    rec.type_id = type_oo.objects.get(name='Другое').id
                rec.save()
            i += 1
        return HttpResponse('ABOBA')
    else:
        return render(request, 'import/import.html')


def check_auth(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

def main(request):
    if check_auth(request) is False:
        return login_user(request)
    username = request.user.username
    context = {
        'username': username,
    }
    return render(request, 'apps/main.html', context)


def logout_user(request):
    logout(request)
    request.method = 'GET'
    return HttpResponse('<meta http-equiv="refresh" content="0; URL=/">')


def login_user(request):
    if request.method == "POST":
        snils = request.POST['snils']
        if snils != '':
            try:
                exp = Experts.objects.get(snils=snils)
            except BaseException:
                error = 'Эксперт не найден. Проверьте правильность ввода СНИЛС'
                return render(request, 'auth/login.html', {'error': error})
            try:
                user = User.objects.get(username=snils)
            except BaseException:
                alphabet = string.ascii_letters + string.digits
                passw = ''.join(secrets.choice(alphabet) for i in range(20))
                new_user = User()
                new_user.username = snils
                new_user.set_password(passw)
                new_user.save()
                new_user.refresh_from_db()
                my_group = Group.objects.get(name='Эксперт')
                my_group.user_set.add(new_user)
                user = authenticate(request, username=snils, password=passw)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            request.method = 'GET'
            return HttpResponse('<meta http-equiv="refresh" content="0; URL=/expert">')
        user = request.POST['username']
        passw = request.POST['password']
        user = authenticate(request, username=user, password=passw)
        if user is not None:
            request.method = 'GET'
            login(request, user)
            id_user = user.id
            try:
                check_fl = Profile.objects.get(user_id=id_user).first_login
                if check_fl is True:
                    request.method = 'GET'
                    return profile(request)
                else:
                    return HttpResponse('<meta http-equiv="refresh" content="0; URL=/">')
            except BaseException:
                return HttpResponse('<meta http-equiv="refresh" content="0; URL=/">')
        else:
            error = 'Неверное имя пользователя или пароль. Повторите попытку'
            return render(request, 'auth/login.html', {'error': error})
    return render(request, 'auth/login.html')


def login_operator(request):
   if check_network(request) is False:
       return render(request, 'error.html',
                     {'error': 'Вход разрешен только из внутренней сети организации'})
   username = request.POST['username']
   password = request.POST['password']
   user = authenticate(request, username=username, password=password)
   if user is None:
       error = 'Неверное имя пользователя или пароль. Повторите попытку'
       return render(request, 'auth/login.html', {'error_operator': error})
   login(request, user)
   return render(request, 'operators/main.html')


def registr(request):
    mos = Munobr.objects.all()
    if request.method == 'POST':
        logins = User.objects.all()
        for el in logins:
            if el.username == request.POST['username']:
                error = "Пользователь с таким логином уже существует"
                return render(request, 'auth/registration.html', {'error': error, 'mos':mos})
            if el.email == request.POST['email']:
                error = "Пользователь с таким email уже существует"
                return render(request, 'auth/registration.html', {'error': error, 'mos':mos})
        if request.POST['password'] != request.POST['password2']:
            error = "Введенные пароли не совпадают"
            return render(request, 'auth/registration.html', {'error': error, 'mos':mos})
        new_user = User()
        new_user.username = request.POST['username']
        new_user.email = request.POST['email']
        new_user.set_password(request.POST['password'])
        new_user.save()
        new_user.refresh_from_db()
        my_group = Group.objects.get(name='Аттестуемый')
        my_group.user_set.add(new_user)
        name_mo = request.POST['mo']
        id_mo = Munobr.objects.get(name_mo=name_mo).id
        new_profile = Profile()
        new_profile.user = new_user
        new_profile.mo_id = id_mo
        new_profile.save()
        return render(request, 'auth/good.html')
    else:
        return render(request, 'auth/registration.html', {'mos':mos})


def profile(request):
    if check_auth(request) is False:
        return login_user(request)
    prof = Profile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        prof.surname = request.POST.get('surname')
        prof.name = request.POST.get('name')
        prof.patronymic = request.POST.get('patronymic')
        prof.birthday = request.POST.get('birthday')
        if request.POST.get('sex') == 'Мужской':
            prof.sex = True
        else:
            prof.sex = False
        prof.phone = request.POST.get('phone')
        if prof.first_login is True:
            prof.first_login = False
        prof.save()
        context = {
            'username': request.user.username,
            'message': 'Информация в профиле успешно изменена'
        }
        return render(request, 'main.html', context)
    username = request.user.username
    id_us = request.user.id
    prof = Profile.objects.get(user_id=id_us)
    if prof.first_login is True:
        message = 'Заполните информацию'
    else:
        message = 'Профиль пользователя'
    context = {
        'username': username,
        'message': message,
        'profile': prof,
    }
    return render(request, 'profile/profile_app.html', context)


def apps_choose(request):
    if check_auth(request) is False:
        return login_user(request)
    username = request.user.username
    context = {
        'username': username,
    }
    return render(request, 'apps/choose.html', context)


def new_app(request):
    if check_auth(request) is False:
        return login_user(request)
    periods = Periods.objects.all()
    check_date = False
    for el in periods:
        if el.date_start_supply <= date.today() <=el.date_end_supply:
            check_date = True
            break
    if check_date == False:
        context = {
            'error': 'Сегодняшняя дата не попадает в сроки подачи заявки',
        }
        return render(request, 'apps/choose.html', context)
    profi = Profile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        app = Apps()
        app.user_profile = profi
        app.teach_exp = request.POST.get('teach_exp')
        app.oo_id = Oo.objects.get(short_name=request.POST.get('oo')).id
        app.oo_exp = request.POST.get('oo_exp')
        app.subj_area = Subjareas.objects.get(name=request.POST.get('subj_area'))
        app.pos_id = Position.objects.get(name_pos=request.POST.get('pos')).id
        app.pos_exp = request.POST.get('pos_exp')
        app.status = 'Черновик'
        app.save()
        id_app = app.id
        app.refresh_from_db()
        request.method = 'GET'
        context = {
            'id_app': id_app
        }
        return render(request, 'apps/transit_one.html', context)
    oos = Oo.objects.filter(mo_id=profi.mo_id)
    sas = Subjareas.objects.all()
    pos = Position.objects.all()
    context = {
        'username': request.user.username,
        'mail': request.user.email,
        'profile': profi,
        'oos': oos,
        'sas': sas,
        'pos': pos,
    }
    return render(request, 'apps/new/new_app.html', context)


def new_app_cat(request):
    if check_auth(request) is False:
        return login_user(request)
    id_app = int(request.POST.get('id_app'))
    if request.POST.get('to_crits') == 'yes':
        app = Apps.objects.get(id=id_app)
        if request.POST.get('cat_have') == 'не имею':
            app.name_doc = None
            app.date_doc = None
            app.cat_have = None
            app.start_cat = None
            app.finish_cat = None
        else:
            app.name_doc = request.POST.get('name_doc')
            app.date_doc = request.POST.get('date_doc')
            app.cat_have = Categories.objects.get(name_cat=request.POST.get('cat_have'))
            app.start_cat = request.POST.get('start_cat')
            app.finish_cat = request.POST.get('finish_cat')
        app.dec_cat = Categories.objects.get(name_cat=request.POST.get('dec_cat'))
        app.form_id=int(request.POST.get('att_form'))
        app.save()
        request.method == 'GET'
        context = {
            'create_app': 'yes'
        }
        return render(request, 'apps/history.html', context)
    context = {
        'id_app': id_app
    }
    return render(request, 'apps/new/new_app_cat.html', context)


def new_app_crits(request):
    if check_auth(request) is False:
        return login_user(request)
    periods = Periods.objects.all()
    check_date = False
    for el in periods:
        if el.date_stat_doc <= date.today() <= el.date_end_doc:
            check_date = True
    if check_date == False:
        context = {
            'wrong_date': 'yes'
        }
        return render(request, 'apps/history.html', context)
    id_app = int(request.POST.get('id_app'))
    if request.POST.get('finish_app') == 'yes':
        app = Apps.objects.get(id=id_app)
        if app.status == 'Зарегистрирована':
            context = {
                'username': request.user.username,
                'edit_app': 'success'
            }
        else:
            app.status = 'Зарегистрирована'
            app.save()
            context = {
                'username': request.user.username,
                'create_app': 'success'
            }
        return render(request, 'apps/history.html', context)
    pos = Apps.objects.get(id=id_app).pos_id
    if AppCritCheck.objects.filter(app_id=id_app).count() != 0:
        app_crits = AppCritCheck.objects.filter(app_id=id_app)
    else:
        for crit in PosCriterias.objects.get(pos_id=pos).crits.values_list('id', flat=True):
            new_check = AppCritCheck()
            new_check.app_id = id_app
            new_check.criteria = Criterias.objects.get(id=crit)
            new_check.check_red = False
            new_check.save()
            new_check.refresh_from_db()
        app_crits = AppCritCheck.objects.filter(app_id=id_app)
    dict_crits = {}
    dict_tables = {}
    dict_upload = {}
    for el in app_crits:
        dict_crits[el.criteria_id] = el.check_red
        if CritPars.objects.filter(criteria_id=el.criteria_id).count() == 0:
            dict_tables[el.criteria_id] = False
        else:
            dict_tables[el.criteria_id] = True
        dict_upload[el.criteria_id] = Criterias.objects.get(id=el.criteria_id).need_upload
    context = {
        'username': request.user.username,
        'dict_crits': dict_crits,
        'dict_upload': dict_upload,
        'dict_tables': dict_tables,
        'finish': check_all_crits(id_app),
        'id_app': id_app,
    }
    return render(request, 'apps/new/new_app_crits.html', context)


def change_crit(request):
    if check_auth(request) is False:
        return login_user(request)
    id_app = request.POST.get('id_app')
    crit_id = request.POST.get('crit_id')
    parameters = CritPars.objects.get(criteria_id=crit_id).parameters.values_list('id', flat=True)
    if request.POST.get('delete') == "1":
        number = int(request.POST.get('del_row'))
        rows = AppCritParValue.objects.filter(app_id=int(id_app)).filter(criteria_id=int(crit_id)).filter(row=number)
        for el in rows:
            el.delete()
    if request.POST.get('new_rec') == '1':
        try:
            recs = AppCritParValue.objects.filter(app_id=int(id_app)).filter(criteria_id=int(crit_id))
            last = recs.latest('row')
            row_num = last.row
        except BaseException:
            row_num = 0
        row_num += 1
        for el in parameters:
            data = request.POST.get('par_'+str(el))
            new_rec = AppCritParValue()
            new_rec.app_id = id_app
            new_rec.criteria_id = crit_id
            new_rec.parameter_id = el
            new_rec.row = row_num
            new_rec.value = data
            new_rec.save()
            new_rec.refresh_from_db()
    if request.POST.get('finish_change') == "1":
        rec = AppCritCheck.objects.filter(app_id=id_app).get(criteria_id=crit_id)
        rec.check_red = True
        rec.save()
        if not Criterias.objects.get(id=crit_id).children.exists():
            check_node_crit(id_app, crit_id)
        context = {
            'username': request.user.username,
            'id_app': id_app
        }
        return render(request, 'apps/transit_crits.html', context)
    crit = Criterias.objects.get(id=crit_id)
    par_values = AppCritParValue.objects.filter(app_id=id_app).filter(criteria_id=crit_id)
    rows = par_values.values('row').distinct()
    pars = par_values.values('parameter').distinct()
    dict_rows = {}
    dict_pars = {}
    if rows.count() == 0:
        pars = CritPars.objects.get(criteria_id=crit_id).parameters.values_list('id', flat=True)
        for el in pars:
            name = Parameters.objects.get(id=el).parameter_name
            dict_pars[el] = name
    for el in rows:
        list = []
        for el_p in pars:
            name = Parameters.objects.get(id=el_p['parameter']).parameter_name
            dict_pars[el_p['parameter']] = name
            for el_pv in par_values:
                if el['row'] == el_pv.row and el_p['parameter'] == el_pv.parameter_id:
                    list.append(el_pv.value)
        dict_rows[el['row']] = list
    context = {
        'username': request.user.username,
        'id_app': id_app,
        'crit': crit,
        'pars': dict_pars,
        'dict': dict_rows,
    }
    return render(request, 'apps/change_crit.html', context)


def upload_crit(request):
    if check_auth(request) is False:
        return login_user(request)
    id_app = int(request.POST.get('id_app'))
    id_crit = int(request.POST.get('id_crit'))
    if request.POST.get('no_upload') == 'yes':
        rec = AppCritCheck.objects.filter(app_id=id_app).get(criteria_id=id_crit)
        rec.check_red = True
        rec.save()
        if not Criterias.objects.get(id=id_crit).children.exists():
            check_node_crit(id_app, id_crit)
        context = {
            'username': request.user.username,
            'id_app': id_app,
            'info': 'Возврат к списку критериев. Подождите...'
        }
        return render(request, 'apps/transit_app.html', context)
    if request.POST.get('upload') == 'yes':
        file = request.FILES['file']
        if file.size > 20971520 or file.name[-3:] not in ('pdf', 'jpg', 'tif'):
            if file.size > 20971520:
                error = 'Размер файла превышает 20 мб!'
            else:
                error = 'Некорректный формат файла!'
            context = {
                'username': request.user.username,
                'id_app': id_app,
                'id_crit': id_crit,
                'form': UploadForm(),
                'error': error,
            }
            return render(request, 'apps/app_file.html', context)
        try:
            rec = AppCritFile.objects.filter(app_id=id_app).get(criteria_id=id_crit)
            rec.delete()
        except BaseException:
            pass
        new = AppCritFile()
        new.app_id = id_app
        new.criteria_id = id_crit
        new.file = file
        new.save()
        rec = AppCritCheck.objects.filter(app_id=id_app).get(criteria_id=id_crit)
        rec.check_red = True
        rec.save()
        if not Criterias.objects.get(id=id_crit).children.exists():
            check_node_crit(id_app, id_crit)
        context = {
            'username': request.user.username,
            'id_app': id_app
        }
        return render(request, 'apps/transit_app.html', context)
    context = {
        'username': request.user.username,
        'id_app': id_app,
        'id_crit': id_crit,
        'form': UploadForm()
    }
    return render(request, 'apps/app_file.html', context)


def doc_view(request):
    if check_auth(request) is False:
        return login_user(request)
    path = request.POST.get('path')
    if path[-3:] == 'pdf':
        return FileResponse(open(path, 'rb'), content_type='application/pdf')
    elif path[-3:] == 'jpg':
        return FileResponse(open(path, 'rb'))
    else:
        return FileResponse(open(path, 'rb'), content_type='image/tiff')


def history_apps(request):
    if check_auth(request) is False:
        return login_user(request)
    context = {
        'username': request.user.username
    }
    return render(request, 'apps/history.html', context)


def rejection_app(request, id):
    if check_auth(request) is False:
        return login_user(request)
    app = Apps.objects.get(id=int(id))
    app.status = 'Отозвано'
    app.save()
    context = {
        'username': request.user.username,
        'rejection_app': 'yes',
    }
    return render(request, 'apps/history.html', context)


def edit_cat(request):
    if check_auth(request) is False:
        return login_user(request)
    id_app = int(request.POST.get('id_app'))
    app = Apps.objects.get(id=id_app)
    if request.POST.get('save_cat') == 'yes':
        if request.POST.get('cat_have') == 'не имею':
            app.name_doc = None
            app.date_doc = None
            app.cat_have = None
            app.start_cat = None
            app.finish_cat = None
        else:
            app.name_doc = request.POST.get('name_doc')
            app.date_doc = request.POST.get('date_doc')
            app.cat_have = Categories.objects.get(name_cat=request.POST.get('cat_have'))
            app.start_cat = request.POST.get('start_cat')
            app.finish_cat = request.POST.get('finish_cat')
        app.dec_cat = Categories.objects.get(name_cat=request.POST.get('dec_cat'))
        app.save()
        request.method == 'GET'
        context = {
            'username': request.user.username,
            'edit_app': 'yes'
        }
        return render(request, 'apps/history.html', context)
    context = {
        'username': request.user.username,
        'id_app': id_app
    }
    return render(request, 'apps/edit/edit_cat.html', context)


def edit_app(request):
    if check_auth(request) is False:
        return login_user(request)
    id_app = request.POST.get('id_app')
    if request.POST.get('save') == 'yes':
        app = Apps.objects.get(id=int(id_app))
        app.teach_exp = request.POST.get('teach_exp')
        app.oo_id = Oo.objects.get(short_name=request.POST.get('oo')).id
        app.oo_exp = request.POST.get('oo_exp')
        app.subj_area = Subjareas.objects.get(name=request.POST.get('subj_area'))
        app.pos_id = Position.objects.get(name_pos=request.POST.get('pos')).id
        app.pos_exp = request.POST.get('pos_exp')
        app.save()
        app.refresh_from_db()
        context = {
            'username': request.user.username,
            'edit_app': 'yes'
        }
        return render(request, 'apps/history.html', context)
    return render(request, 'apps/edit/edit_app.html', {'id_app': id_app})


def check_node_crit(app_id, crit_id):
    parent = Criterias.objects.get(id=crit_id).parent
    try:
        children = Criterias.objects.get(id=parent.id).get_children()
    except BaseException:
        return None
    count = children.count()
    if count == 0:
        return None
    check = 0
    for el in children:
        try:
            if AppCritCheck.objects.filter(app_id=app_id).get(criteria_id=el.id).check_red == True:
                check += 1
        except BaseException:
            count -= 1
    if count == check:
        rec = AppCritCheck.objects.filter(app_id=app_id).get(criteria_id=parent.id)
        rec.check_red = True
        rec.save()
    return None


def check_all_crits(app_id):
    crits = AppCritCheck.objects.filter(app_id=app_id)
    count = crits.count()
    check = 0
    for el in crits:
        if el.check_red == True:
            check += 1
    if check == count:
        return True
    else:
        return False
# Create your views here.
