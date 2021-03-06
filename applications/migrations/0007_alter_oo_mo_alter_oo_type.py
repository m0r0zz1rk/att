# Generated by Django 4.0.2 on 2022-02-21 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0006_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oo',
            name='mo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='applications.munobr', verbose_name='МО ОО'),
        ),
        migrations.AlterField(
            model_name='oo',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='applications.type_oo', verbose_name='Тип ОО'),
        ),
    ]
