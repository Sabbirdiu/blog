# Generated by Django 3.0.5 on 2020-07-06 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comment_count',
        ),
    ]
