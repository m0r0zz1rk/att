from django.db import models
from applications.models import *
import datetime


class Experts(models.Model):
    surname = models.CharField(max_length=100, null=True, default='', verbose_name='Фамилия')
    name = models.CharField(max_length=100, null=True, default='', verbose_name='Имя')
    patronymic = models.CharField(max_length=100, null=True, default='', verbose_name='Отчество')
    mo = models.ForeignKey(
        Munobr,
        on_delete = models.PROTECT,
        default = 1,
        verbose_name = 'МО'
    )
    oo = models.ForeignKey(
        Oo,
        on_delete = models.PROTECT,
        default = 1,
        verbose_name = 'ОО'
    )
    subj = models.ForeignKey(
        Subjareas,
        on_delete=models.PROTECT,
        default=194,
        null=True,
        verbose_name='Предметная область',
        related_name='experts_subj'
    )
    pos = models.ForeignKey(
        Position,
        on_delete = models.PROTECT,
        default = 1,
        verbose_name = 'Должность'
    )
    email = models.CharField(null=True, default='', max_length=150, verbose_name="email")
    snils = models.CharField(unique=True, null=False, default='000-000-000 00', max_length=20, verbose_name="СНИЛС")
    status = models.BooleanField(default=True, verbose_name='Статус активности')
    date_add = models.DateField(default=datetime.datetime.now, verbose_name='Дата внесения в базу')

    def get_marks_info(self):
        values = self.expertmarks.all()
        dict_main = {}
        for el in values:
            recs = values.filter(app_id=el.app_id)
            dict = {}
            for rec in recs:
                dict[rec.criteria.name+" - "+rec.criteria.description] = [rec.mark, rec.info]
            dict_main[el.app_id] = dict
        return dict_main

    def get_apps(self):
        values = self.expertresult.all()
        list = []
        for el in values:
            list.append(el.app_id)
        return list

    def get_result(self):
        return self.expertresult.all()

    def __str__(self):
        return self.surname + " " + self.name + " " + self.patronymic

    class Meta:
        verbose_name = 'Эксперт'
        verbose_name_plural = 'Эксперты'


class Marks(models.Model):
    pos = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        default=243,
        null=False,
        verbose_name='Должность'
    )
    criteria = models.ForeignKey(
        Criterias,
        on_delete = models.PROTECT,
        default = 1,
        null = False,
        blank = False,
        verbose_name = 'Критерий'
    )
    mark_list = models.CharField(max_length=100, default='', null=False, verbose_name='Список возможных баллов')

    def __str__(self):
        return self.criteria.name + "-" + self.criteria.description

    class Meta:
        unique_together = ('pos', 'criteria')
        verbose_name = 'Баллы за критерий'
        verbose_name_plural = 'Баллы за критерии'


class Total(models.Model):
    cat = models.ForeignKey(
        Categories,
        on_delete = models.CASCADE,
        default = 1,
        null = False,
        verbose_name = 'Категория'
    )
    pos = models.ForeignKey(
        Position,
        on_delete = models.CASCADE,
        default = 243,
        null = False,
        verbose_name = 'Должность'
    )
    total = models.PositiveIntegerField(default=0, verbose_name='Граница баллов')

    def __str__(self):
        return self.cat.name_cat +" - "+self.pos.name_pos

    class Meta:
        unique_together = ('cat', 'pos')
        verbose_name = 'Сумма баллов для установления КК'
        verbose_name_plural = 'Суммы баллов для установления КК'


class ExpertMarks(models.Model):
    expert = models.ForeignKey(
        Experts,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Эксперт',
        related_name='expertmarks'
    )
    app = models.ForeignKey(
        Apps,
        on_delete=models.CASCADE,
        default=1,
        null=False,
        blank=False,
        verbose_name='Заявка'
    )
    criteria = models.ForeignKey(
        Criterias,
        on_delete=models.CASCADE,
        default='1',
        null=False,
        blank=False,
        verbose_name='Критерий'
    )
    mark = models.PositiveIntegerField(default=0, verbose_name='Баллы')
    info = models.TextField(null=True, default='', max_length=1000, verbose_name='Замечание')

    def __str__(self):
        return self.expert.surname + " : "+self.app.user_profile.surname + " - "+self.criteria.name

    class Meta:
        unique_together = ('app', 'expert', 'criteria')
        verbose_name = 'Оценка эксперта'
        verbose_name_plural = 'Оценки экспертов'


class AppResult(models.Model):
    expert = models.ForeignKey(
        Experts,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Эксперт',
        related_name='expertresult'
    )
    app = models.ForeignKey(
        Apps,
        on_delete=models.CASCADE,
        default=1,
        null=False,
        blank=False,
        verbose_name='Заявка',
        related_name='expertresult'
    )
    total_mark = models.PositiveIntegerField(default=0, verbose_name='Итоговое количество баллов')
    result = models.CharField(max_length=50, default='Отказать', verbose_name='Результат')
    date = models.DateField(auto_now=True, verbose_name='Дата проведения экспертизы')

    def __str__(self):
        return self.expert.surname +' - '+self.app.user_profile.surname

    class Meta:
        unique_together = ('expert', 'app')
        verbose_name = 'Результат аттестации'
        verbose_name_plural = 'Результаты аттестации'


# Create your models here.
