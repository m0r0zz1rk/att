# Generated by Django 4.0.2 on 2022-02-28 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0028_alter_position_name_pos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apps',
            name='finish_cat',
            field=models.DateField(default=None, null=True, verbose_name='Дата окончания действия атт. категории'),
        ),
        migrations.AlterField(
            model_name='apps',
            name='start_cat',
            field=models.DateField(default=None, null=True, verbose_name='Дата начала действия атт. категории'),
        ),
    ]
