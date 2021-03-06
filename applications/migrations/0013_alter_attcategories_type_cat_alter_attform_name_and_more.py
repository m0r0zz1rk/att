# Generated by Django 4.0.2 on 2022-02-21 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0012_alter_profile_cat_have'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attcategories',
            name='type_cat',
            field=models.CharField(max_length=250, unique=True, verbose_name='Заявленная категория'),
        ),
        migrations.AlterField(
            model_name='attform',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Форма аттестации'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='name_cat',
            field=models.CharField(max_length=100, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='munobr',
            name='name_mo',
            field=models.CharField(max_length=250, unique=True, verbose_name='Наименование МО'),
        ),
        migrations.AlterField(
            model_name='subjareas',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Предметная область'),
        ),
        migrations.AlterField(
            model_name='type_oo',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название типа ОО'),
        ),
    ]
