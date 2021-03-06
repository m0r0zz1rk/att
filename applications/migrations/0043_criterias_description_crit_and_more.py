# Generated by Django 4.0.2 on 2022-03-23 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0042_appcritparvalue_row'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterias',
            name='description_crit',
            field=models.TextField(default='', max_length=500, null=True, verbose_name='Информация к заполнению критерия'),
        ),
        migrations.AddField(
            model_name='criterias',
            name='description_upload',
            field=models.TextField(default='', max_length=500, null=True, verbose_name='Информация к загружаемым документам'),
        ),
    ]
