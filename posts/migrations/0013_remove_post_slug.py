# Generated by Django 3.0.5 on 2020-07-02 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_post_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]