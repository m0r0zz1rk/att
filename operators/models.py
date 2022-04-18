from django.db import models
from expert.models import *
from applications.models import *
from datetime import datetime


class Periods(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name='Название периода')
    date_start_supply = models.DateField(default=datetime.now, verbose_name='Дата начала подачи заявок')
    date_end_supply = models.DateField(default=datetime.now, verbose_name='Дата окончания подачи заявок')
    date_com_miting = models.DateField(default=datetime.now, verbose_name='Дата заседания аттестационной комиссии')
    date_stat_doc = models.DateField(default=datetime.now,
                                     verbose_name='Дата начала предоставления документов оператору')
    date_end_doc = models.DateField(default=datetime.now,
                                     verbose_name='Дата окончания предоставления документов оператору')
    date_start_first = models.DateField(default=datetime.now, verbose_name='Дата начала первого этапа экспертизы')
    date_end_first = models.DateField(default=datetime.now, verbose_name='Дата окончания первого этапа экспертизы')
    date_start_second = models.DateField(default=datetime.now, verbose_name='Дата начала второго этапа экспертизы')
    date_end_second = models.DateField(default=datetime.now, verbose_name='Дата окончания второго этапа экспертизы')
    date_start_last = models.DateField(default=datetime.now,
                                         verbose_name='Дата начала подведения итогов всестороннего анализа')
    date_end_last = models.DateField(default=datetime.now,
                                         verbose_name='Дата окончания подведения итогов всестороннего анализа')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Период'
        verbose_name_plural = 'Периоды'


class Distributions(models.Model):
    date = models.DateField(default=datetime.now, verbose_name='Дата создания назначения')
    period = models.ForeignKey(
        Periods,
        on_delete=models.CASCADE,
        default=2,
        null=False,
        verbose_name='Период'
    )
    expert = models.ForeignKey(
        Experts,
        on_delete=models.CASCADE,
        default=1,
        null=False,
        verbose_name='Эксперт'
    )
    app = models.ForeignKey(
        Apps,
        on_delete=models.CASCADE,
        default=1,
        null=False,
        verbose_name='Заявка',
        related_name='appdistrib'
    )
    stage = models.ForeignKey(
        Stages,
        on_delete=models.PROTECT,
        default=1,
        verbose_name='Этап всестороннего анализа'
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Распределение'
        verbose_name_plural = 'Распределения'
# Create your models here.
