# Generated by Django 3.0.3 on 2021-02-07 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0008_auto_20210207_1852'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='like',
            new_name='likes',
        ),
    ]
