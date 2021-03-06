# Generated by Django 4.0.2 on 2022-02-25 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0022_criterias_level_criterias_lft_criterias_rght_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='criterias',
            options={'verbose_name': 'Критерий', 'verbose_name_plural': 'Критерии'},
        ),
        migrations.AlterField(
            model_name='criterias',
            name='need_upload',
            field=models.BooleanField(default=False, verbose_name='Необходимость загрузки файлов'),
        ),
    ]
