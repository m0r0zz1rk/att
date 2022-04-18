# Generated by Django 4.0.3 on 2022-04-08 03:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Periods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Название периода')),
                ('date_start_supply', models.DateField(default=datetime.datetime.now, verbose_name='Дата начала подачи заявок')),
                ('date_end_supply', models.DateField(default=datetime.datetime.now, verbose_name='Дата окончания подачи заявок')),
                ('date_com_miting', models.DateField(default=datetime.datetime.now, verbose_name='Дата заседания аттестационной комиссии')),
                ('date_stat_doc', models.DateField(default=datetime.datetime.now, verbose_name='Дата начала предоставления документов оператору')),
                ('date_end_doc', models.DateField(default=datetime.datetime.now, verbose_name='Дата окончания предоставления документов оператору')),
                ('date_start_first', models.DateField(default=datetime.datetime.now, verbose_name='Дата начала первого этапа экспертизы')),
                ('date_end_first', models.DateField(default=datetime.datetime.now, verbose_name='Дата окончания первого этапа экспертизы')),
                ('date_start_second', models.DateField(default=datetime.datetime.now, verbose_name='Дата начала второго этапа экспертизы')),
                ('date_end_second', models.DateField(default=datetime.datetime.now, verbose_name='Дата окончания второго этапа экспертизы')),
                ('date_start_last', models.DateField(default=datetime.datetime.now, verbose_name='Дата начала подведения итогов всестороннего анализа')),
                ('date_end_last', models.DateField(default=datetime.datetime.now, verbose_name='Дата окончания подведения итогов всестороннего анализа')),
            ],
            options={
                'verbose_name': 'Период',
                'verbose_name_plural': 'Периоды',
            },
        ),
    ]