# Generated by Django 4.2 on 2023-04-22 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_coachforclient_visit_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachforclient',
            name='age',
            field=models.CharField(default=1, max_length=255, verbose_name='Возрастная категория'),
            preserve_default=False,
        ),
    ]
