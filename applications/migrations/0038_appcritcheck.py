# Generated by Django 4.0.2 on 2022-03-17 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0037_appcritparvalue_critpars_remove_pc_values_app_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppCritCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_red', models.BooleanField(default=False, verbose_name='Отредактировано')),
                ('app', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='applications.apps', verbose_name='Заявка')),
                ('criteria', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='applications.criterias', verbose_name='Критерий')),
            ],
            options={
                'verbose_name': 'Отредактированный параметр',
                'verbose_name_plural': 'Отредактированные параметры',
            },
        ),
    ]
