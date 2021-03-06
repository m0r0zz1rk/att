# Generated by Django 4.0.2 on 2022-02-22 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0014_alter_profile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='apps',
            name='mo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='apps_mo', to='applications.munobr', verbose_name='Муниципальное образование'),
        ),
        migrations.AddField(
            model_name='apps',
            name='oo',
            field=models.ForeignKey(default=14765, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='apps_oo', to='applications.oo', verbose_name='Образовательная организация'),
        ),
    ]
