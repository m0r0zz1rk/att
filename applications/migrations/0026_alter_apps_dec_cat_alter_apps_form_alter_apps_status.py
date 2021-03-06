# Generated by Django 4.0.2 on 2022-02-28 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0025_remove_position_type_pos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apps',
            name='dec_cat',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dec_category', to='applications.categories', verbose_name='Заявленная категория'),
        ),
        migrations.AlterField(
            model_name='apps',
            name='form',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='applications.attform', verbose_name='Форма аттестации'),
        ),
        migrations.AlterField(
            model_name='apps',
            name='status',
            field=models.CharField(default='Создание', max_length=30, null=True, verbose_name='Статус заявления'),
        ),
    ]
