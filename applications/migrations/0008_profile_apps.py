# Generated by Django 4.0.2 on 2022-02-21 03:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0007_alter_oo_mo_alter_oo_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=100, verbose_name='Отчество')),
                ('birthday', models.DateField(default=datetime.date.today, verbose_name='Дата рождения')),
                ('sex', models.BooleanField(default=0, verbose_name='Пол')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(default='895000000', max_length=128, null=True, region=None, unique=True)),
                ('teach_exp', models.PositiveIntegerField(default=0, verbose_name='Педагогический стаж')),
                ('oo_exp', models.PositiveIntegerField(default=0, verbose_name='Стаж работы в ОО')),
                ('pos_exp', models.PositiveIntegerField(default=0, verbose_name='Стаж в должности')),
                ('start_cat', models.DateField(default=datetime.date.today, null=True, verbose_name='Дата начала действия атт. категории')),
                ('finish_cat', models.DateField(default=datetime.date.today, null=True, verbose_name='Дата окончания действия атт. категории')),
                ('first_login', models.BooleanField(default=True, verbose_name='Первое заполнение данных')),
                ('cat_have', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profile_cathave', to='applications.categories', verbose_name='Имеющаяся категория')),
                ('mo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='profile_mo', to='applications.munobr', verbose_name='Муниципальное образование')),
                ('oo', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profile_oo', to='applications.oo', verbose_name='Образовательная организация')),
                ('pos', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profile_pos', to='applications.position', verbose_name='Должность')),
                ('subj_area', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profile_subj', to='applications.subjareas', verbose_name='Предметная область')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
        migrations.CreateModel(
            name='Apps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=100, verbose_name='Отчество')),
                ('sex', models.BooleanField(verbose_name='Пол')),
                ('email', models.EmailField(default='it@coko38.ru', max_length=254, verbose_name='Электронная почта')),
                ('start_cat', models.DateField(default=datetime.date.today, verbose_name='Дата начала действия атт. категории')),
                ('finish_cat', models.DateField(default=datetime.date.today, verbose_name='Дата окончания действия атт. категории')),
                ('date_reg', models.DateField(auto_now_add=True, verbose_name='Дата регистрации завления')),
                ('status', models.CharField(max_length=30, null=True, verbose_name='Статус заявления')),
                ('cat_have', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='av_category', to='applications.categories', verbose_name='Имеющаяся категория')),
                ('dec_cat', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='dec_category', to='applications.categories', verbose_name='Заявленная категория')),
                ('form', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='applications.attform', verbose_name='Форма аттестации')),
                ('pos', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='applications.position', verbose_name='Должность')),
                ('subj_area', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='applications.subjareas', verbose_name='Предметная область')),
                ('user_profile', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='applications.profile', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка на аттестацию',
                'verbose_name_plural': 'Заявки на аттестацию',
            },
        ),
    ]
