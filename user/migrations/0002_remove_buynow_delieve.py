# Generated by Django 2.2.2 on 2019-07-09 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buynow',
            name='delieve',
        ),
    ]
