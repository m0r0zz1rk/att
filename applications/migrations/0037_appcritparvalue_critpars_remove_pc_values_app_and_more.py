# Generated by Django 4.0.2 on 2022-03-17 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0036_appcritnotes'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppCritParValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(max_length=500, verbose_name='Значение')),
                ('app', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='applications.apps', verbose_name='Заявка')),
                ('criteria', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='applications.criterias', verbose_name='Критерий')),
                ('parameter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='applications.parameters', verbose_name='Параметр')),
            ],
            options={
                'verbose_name': 'Пара Параметр-Значение',
                'verbose_name_plural': 'Пары Параметр-Значение',
            },
        ),
        migrations.CreateModel(
            name='CritPars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subj', models.BooleanField(default=False, verbose_name='Указание предмета')),
                ('criteria', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='applications.criterias', verbose_name='Критерий')),
                ('parameters', models.ManyToManyField(to='applications.Parameters', verbose_name='Параметр')),
            ],
            options={
                'verbose_name': 'Связь Критерий-Параметры',
                'verbose_name_plural': 'Связи Критерий-Параметры',
            },
        ),
        migrations.RemoveField(
            model_name='pc_values',
            name='app',
        ),
        migrations.RemoveField(
            model_name='pc_values',
            name='pc_pair',
        ),
        migrations.DeleteModel(
            name='Pc_pairs',
        ),
        migrations.DeleteModel(
            name='Pc_values',
        ),
    ]
