# Generated by Django 4.2 on 2023-04-19 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='age',
            name='key',
        ),
        migrations.RemoveField(
            model_name='days',
            name='key',
        ),
        migrations.RemoveField(
            model_name='grouptype',
            name='key',
        ),
        migrations.RemoveField(
            model_name='location',
            name='key',
        ),
    ]
