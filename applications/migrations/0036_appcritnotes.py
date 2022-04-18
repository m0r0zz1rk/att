# Generated by Django 4.0.2 on 2022-03-16 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0035_alter_parameters_parameter_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppCritNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(max_length=500, verbose_name='Заметка')),
                ('app', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='applications.apps', verbose_name='Заявка')),
                ('criteria', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='applications.criterias', verbose_name='Критерий')),
            ],
            options={
                'verbose_name': 'Заметка к критериям',
                'verbose_name_plural': 'Заметки к критериям',
            },
        ),
    ]