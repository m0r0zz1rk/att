# Generated by Django 4.0.3 on 2022-04-07 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0049_delete_attforms'),
        ('expert', '0003_experts_mo'),
    ]

    operations = [
        migrations.AddField(
            model_name='experts',
            name='subj',
            field=models.ForeignKey(default=194, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='experts_subj', to='applications.subjareas', verbose_name='Предметная область'),
        ),
    ]