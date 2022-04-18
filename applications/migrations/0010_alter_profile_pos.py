# Generated by Django 4.0.2 on 2022-02-21 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0009_alter_profile_oo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pos',
            field=models.ForeignKey(default=243, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profile_pos', to='applications.position', verbose_name='Должность'),
        ),
    ]
