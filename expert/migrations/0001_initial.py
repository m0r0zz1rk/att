# Generated by Django 3.2.7 on 2022-03-31 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0047_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Total',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='Граница баллов')),
                ('cat', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='applications.categories', verbose_name='Категория')),
                ('pos', models.ForeignKey(default=243, on_delete=django.db.models.deletion.CASCADE, to='applications.position', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Сумма баллов для установления КК',
                'verbose_name_plural': 'Суммы баллов для установления КК',
            },
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark_list', models.CharField(default='', max_length=100, verbose_name='Список возможных баллов')),
                ('criteria', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='applications.criterias', verbose_name='Критерий')),
            ],
            options={
                'verbose_name': 'Баллы за критерий',
                'verbose_name_plural': 'Баллы за критерии',
            },
        ),
        migrations.CreateModel(
            name='Experts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(default='', max_length=100, null=True, verbose_name='Фамилия')),
                ('name', models.CharField(default='', max_length=100, null=True, verbose_name='Имя')),
                ('patronymic', models.CharField(default='', max_length=100, null=True, verbose_name='Отчество')),
                ('email', models.CharField(default='', max_length=150, null=True, verbose_name='email')),
                ('snils', models.CharField(default='00000000000', max_length=25, verbose_name='СНИЛС')),
                ('status', models.BooleanField(default=True, verbose_name='Статус')),
                ('oo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='applications.oo', verbose_name='ОО')),
                ('pos', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='applications.position', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Эксперт',
                'verbose_name_plural': 'Эксперты',
            },
        ),
        migrations.CreateModel(
            name='ExpertMarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Mark', models.PositiveIntegerField(default=0, verbose_name='Баллы')),
                ('app', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='applications.apps', verbose_name='Заявка')),
                ('criteria', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='applications.criterias', verbose_name='Критерий')),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.experts', verbose_name='Эксперт')),
            ],
            options={
                'verbose_name': 'Оценка эксперта',
                'verbose_name_plural': 'Оценки экспертов',
            },
        ),
        migrations.CreateModel(
            name='AppResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_mark', models.PositiveIntegerField(default=0, verbose_name='Итоговое количество баллов')),
                ('result', models.CharField(default='Отказать', max_length=50, verbose_name='Результат')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата проведения экспертизы')),
                ('app', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='applications.apps', verbose_name='Заявка')),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.experts', verbose_name='Эксперт')),
            ],
            options={
                'verbose_name': 'Результат аттестации',
                'verbose_name_plural': 'Результаты аттестации',
            },
        ),
    ]