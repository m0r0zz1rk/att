# Generated by Django 4.0.3 on 2022-04-15 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0006_alter_marks_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expertmarks',
            name='info',
            field=models.TextField(default='', max_length=1000, null=True, verbose_name='Замечание'),
        ),
    ]