# Generated by Django 4.0.2 on 2022-02-25 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0023_alter_criterias_options_alter_criterias_need_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosCriterias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crits', models.ManyToManyField(related_name='crits_pos', to='applications.Criterias', verbose_name='Критерии')),
                ('pos', models.ForeignKey(default=243, on_delete=django.db.models.deletion.PROTECT, related_name='pos_crits', to='applications.position', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Должность-Критерии',
                'verbose_name_plural': 'Должности-Критерии',
            },
        ),
    ]
