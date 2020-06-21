# Generated by Django 3.0.5 on 2020-06-21 14:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20200614_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='view_count',
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.CharField(blank=True, max_length=60, validators=[django.core.validators.RegexValidator('^[, a-zA-Z]*$', 'Enter comma separated tags. (use space for two words tag)')]),
        ),
    ]
