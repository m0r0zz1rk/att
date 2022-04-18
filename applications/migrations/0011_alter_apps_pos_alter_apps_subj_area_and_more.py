# Generated by Django 4.0.2 on 2022-02-21 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0010_alter_profile_pos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apps',
            name='pos',
            field=models.ForeignKey(default=243, on_delete=django.db.models.deletion.PROTECT, to='applications.position', verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='apps',
            name='subj_area',
            field=models.ForeignKey(default=194, on_delete=django.db.models.deletion.PROTECT, to='applications.subjareas', verbose_name='Предметная область'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='subj_area',
            field=models.ForeignKey(default=194, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profile_subj', to='applications.subjareas', verbose_name='Предметная область'),
        ),
    ]
