# Generated by Django 4.0.2 on 2022-02-21 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0008_profile_apps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='oo',
            field=models.ForeignKey(default=14765, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profile_oo', to='applications.oo', verbose_name='Образовательная организация'),
        ),
    ]
