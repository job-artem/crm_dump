# Generated by Django 4.2 on 2023-05-04 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0015_alter_formclient_section_alter_formclient_visit_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachforclient',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Тренер'),
        ),
    ]
