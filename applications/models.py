# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import Group, User
from phonenumber_field.modelfields import PhoneNumberField
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime


class Stages(models.Model):
    name_stage = models.CharField(default='', unique=True, max_length=50, verbose_name='Этап')

    def __str__(self):
        return self.name_stage

    class Meta:
        verbose_name = 'Этап всестороннего анализа'
        verbose_name_plural = 'Этапы всестороннего анализа'


class Criterias(MPTTModel):
    name = models.CharField(null=False, max_length=50, verbose_name="Критерий")
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родитель'
    )
    description = models.CharField(null=False, max_length=300, verbose_name="Наименование")
    need_upload = models.BooleanField(default=False, verbose_name='Необходимость загрузки файлов')
    description_upload = models.TextField(max_length=1000,
                                          default="",
                                          null=True,
                                          blank=True,
                                          verbose_name="Информация к загружаемым документам"
                                          )
    description_crit = models.TextField(max_length=1000,
                                        default="",
                                        null=True,
                                        blank=True,
                                        verbose_name="Информация к заполнению критерия")

    def __str__(self):
        return self.name+" - "+self.description

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Критерий'
        verbose_name_plural = 'Критерии'


class Categories(models.Model):
    name_cat = models.CharField(max_length=100, unique=True, verbose_name='Категория')

    def __str__(self):
        return self.name_cat

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subjareas(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Предметная область')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предметная область'
        verbose_name_plural = 'Предметные области'


class Attform(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Форма аттестации')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Форма аттестации'
        verbose_name_plural = 'Формы аттестации'


class Munobr(models.Model):
    name_mo = models.CharField(max_length=250,  unique=True, verbose_name='Наименование МО')
    type_mo = models.CharField(max_length=100, verbose_name='Тип МО')

    def __str__(self):
        return self.name_mo

    class Meta:
        verbose_name = 'МО'
        verbose_name_plural = 'МО'


class Position(models.Model):
    name_pos = models.CharField(max_length=150, unique=True, verbose_name='Должность')

    def __str__(self):
        return self.name_pos

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class PosCriterias(models.Model):
    pos = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        default=243,
        null=False,
        related_name='pos_crits',
        verbose_name='Должность'
    )
    crits = models.ManyToManyField(
        Criterias,
        related_name='crits_pos',
        verbose_name='Критерии'
    )

    def __str__(self):
        return self.pos.name_pos

    class Meta:
        verbose_name = 'Должность-Критерии'
        verbose_name_plural = 'Должности-Критерии'


class type_oo(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название типа ОО')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип ОО'
        verbose_name_plural = 'Типы ОО'


class Oo(models.Model):
    full_name = models.CharField(max_length=500, verbose_name='Полное наименование ОО')
    short_name = models.CharField(max_length=150, unique=True, verbose_name='Краткое наименование ОО')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес ОО')
    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name='Телефон ОО')
    email = models.CharField(max_length=254, blank=True, null=True,verbose_name='Электронная почта ОО')
    url = models.CharField(max_length=254, blank=True, null=True,verbose_name='Сайт ОО')
    mo = models.ForeignKey(Munobr,
                           on_delete=models.PROTECT,
                           default=1,
                           verbose_name='МО ОО')
    type = models.ForeignKey(type_oo,
                             on_delete=models.PROTECT,
                             default=1,
                             verbose_name='Тип ОО')

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = 'ОО'
        verbose_name_plural = 'ОО'


class Profile(models.Model):
    registration_date = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1,
        null=True,
        verbose_name='Пользователь'
    )
    surname = models.CharField(max_length=100, null=True, verbose_name='Фамилия')
    name = models.CharField(max_length=100, null=True, verbose_name='Имя')
    patronymic = models.CharField(max_length=100, null=True, verbose_name='Отчество')
    birthday = models.DateField(default=datetime.date.today, null=True, verbose_name="Дата рождения")
    sex = models.BooleanField(default=0, null=True, verbose_name='Пол')
    phone = PhoneNumberField(default=None, unique=True, null=True, blank=False)
    mo = models.ForeignKey(
        Munobr,
        on_delete=models.PROTECT,
        default=1,
        null=False,
        verbose_name='Муниципальное образование',
        related_name='profile_mo'
    )
    first_login = models.BooleanField(default=True, verbose_name='Первое заполнение данных')

    def __str__(self):
        return self.surname+" "+self.name+" "+self.patronymic

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class Apps(models.Model):
    user_profile = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        default=1,
        null=False,
        verbose_name='Пользователь'
    )
    teach_exp = models.PositiveIntegerField(default=0, verbose_name='Педагогический стаж')
    oo = models.ForeignKey(
        Oo,
        on_delete=models.PROTECT,
        default=14765,
        null=True,
        verbose_name='Образовательная организация',
        related_name='apps_oo'
    )
    oo_exp = models.PositiveIntegerField(default=0, verbose_name='Стаж работы в ОО')
    subj_area = models.ForeignKey(
        Subjareas,
        on_delete=models.PROTECT,
        default=194,
        null=True,
        verbose_name='Предметная область',
        related_name='apps_subj'
    )
    pos = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        default=243,
        null=True,
        verbose_name='Должность',
        related_name='apps_pos'
    )
    pos_exp = models.PositiveIntegerField(default=0, verbose_name='Стаж в должности')
    name_doc = models.CharField(max_length=25, default=None, null=True, verbose_name='Номер документа')
    date_doc = models.DateField(default=None, null=True, verbose_name='Дата документа')
    cat_have = models.ForeignKey(
        Categories,
        on_delete=models.PROTECT,
        default=None,
        null=True,
        verbose_name='Имеющаяся категория',
        related_name='apps_cathave'
    )
    start_cat = models.DateField(null=True, default=None,
                                 verbose_name='Дата начала действия атт. категории')
    finish_cat = models.DateField(null=True, default=None,
                                  verbose_name='Дата окончания действия атт. категории')
    dec_cat = models.ForeignKey(
        Categories,
        on_delete = models.PROTECT,
        default = 1,
        null = True,
        related_name = 'dec_category',
        verbose_name = 'Заявленная категория'
    )
    form = models.ForeignKey(
        Attform,
        on_delete = models.PROTECT,
        default = 1,
        null = True,
        verbose_name = 'Форма аттестации'
    )
    date_reg = models.DateField(auto_now_add=True, verbose_name='Дата регистрации завления')
    status = models.CharField(max_length=30, null=True, default='Создание', verbose_name='Статус заявления')

    def __str__(self):
        return self.user_profile.surname + " " + self.user_profile.name + " " + self.user_profile.patronymic

    def get_expertres(self):
        return self.expertresult.all()

    def get_critfile(self):
        values = self.critfile.all()
        dict = {}
        crits = values.order_by().values('criteria').distinct()
        for el in crits:
            value = values.get(criteria=el['criteria'])
            dict[Criterias.objects.get(id=el['criteria']).name+' - '+Criterias.objects.get(id=el['criteria']).description] = value.file.path
        return dict

    def get_critdata(self):
        values = self.critdata.all()
        dict = {}
        crits = values.order_by().values('criteria').distinct()
        for el in crits:
            dict_par = {}
            recs = values.filter(criteria=el['criteria'])
            pars = recs.order_by().values('parameter').distinct()
            for par in pars:
                recs_par = recs.filter(parameter=par['parameter'])
                list = []
                row = 1
                for rec_par in recs_par:
                    if rec_par.row == row:
                        list.append(rec_par.value)
                    row += 1
                dict_par[Parameters.objects.get(id=par['parameter']).parameter_name] = list
            dict[Criterias.objects.get(id=el['criteria']).name+' - '+Criterias.objects.get(id=el['criteria']).description] = dict_par
        return dict

    def get_criterias(self):
        values = self.appcrits.all()
        dict = {}
        for el in values:
            dict[el.criteria.name+" - "+el.criteria.description] = el.criteria.parent_id
        return dict

    def get_experts(self):
        return self.appdistrib.all()

    class Meta:
        verbose_name = 'Заявка на аттестацию'
        verbose_name_plural = 'Заявки на аттестацию'


class Parameters(models.Model):
    parameter_name = models.CharField(max_length = 250, unique = True, verbose_name='Имя параметра')

    def __str__(self):
        return self.parameter_name

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметр'


class CritPars(models.Model):
    criteria = models.OneToOneField(
        Criterias,
        on_delete=models.CASCADE,
        default='1',
        null=False,
        blank=False,
        verbose_name='Критерий'
    )
    parameters = models.ManyToManyField(
        Parameters,
        verbose_name='Параметр'
    )
    subj = models.BooleanField(default=False, verbose_name='Указание предмета')

    def __str__(self):
        return str(self.criteria)

    class Meta:
        verbose_name = 'Связь Критерий-Параметры'
        verbose_name_plural = 'Связи Критерий-Параметры'


class AppCritCheck(models.Model):
    app = models.ForeignKey(
        Apps,
        on_delete=models.CASCADE,
        default=1,
        null=False,
        blank=False,
        verbose_name='Заявка',
        related_name='appcrits'
    )
    criteria = models.ForeignKey(
        Criterias,
        on_delete=models.CASCADE,
        default='1',
        null=False,
        blank=False,
        verbose_name='Критерий'
    )
    check_red = models.BooleanField(default=False, verbose_name='Отредактировано')

    def __str__(self):
        return str(self.app)+ " : "+str(self.criteria)

    class Meta:
        verbose_name = 'Связь Заявка-Параметр'
        verbose_name_plural = 'Связи Заявки-Параметры'


class AppCritParValue(models.Model):
    app = models.ForeignKey(
        Apps,
        on_delete = models.CASCADE,
        default = 1,
        null = False,
        blank = False,
        verbose_name = 'Заявка',
        related_name = 'critdata'
    )
    criteria = models.ForeignKey(
        Criterias,
        on_delete=models.CASCADE,
        default='1',
        null=False,
        blank=False,
        verbose_name='Критерий'
    )
    parameter = models.ForeignKey(
        Parameters,
        on_delete = models.CASCADE,
        default = 1,
        null = False,
        blank = False,
        verbose_name = 'Параметр'
    )
    row = models.PositiveIntegerField(null=False, default=1, verbose_name='Строка')
    value = models.TextField(max_length=500, verbose_name='Значение')

    def __str__(self):
        return self.app + " - "+self.pc_pair

    class Meta:
        verbose_name = 'Пара Параметр-Значение'
        verbose_name_plural = 'Пары Параметр-Значение'


def get_path(instance, filename):
    format = filename[-3:]
    return settings.MEDIA_ROOT+'\\{0}\\{1}\\{2}\\{3}.{4}'.\
        format(instance.app.date_reg.year, instance.app.date_reg.month,
               instance.app_id, instance.criteria.name, format)


class AppCritFile(models.Model):
    app = models.ForeignKey(
        Apps,
        on_delete=models.CASCADE,
        default=1,
        null=False,
        blank=False,
        verbose_name='Заявка',
        related_name='critfile'
    )
    criteria = models.ForeignKey(
        Criterias,
        on_delete=models.CASCADE,
        default='1',
        null=False,
        blank=False,
        verbose_name='Критерий'
    )
    file = models.FileField(upload_to=get_path, verbose_name='Документ')

    def __str__(self):
        return str(self.app.id)+" : "+self.criteria

    class Meta:
        verbose_name = 'Загруженный файл'
        verbose_name_plural = 'Загруженные файлы'

