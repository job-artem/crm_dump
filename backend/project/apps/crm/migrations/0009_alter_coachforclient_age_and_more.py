# Generated by Django 4.2 on 2023-04-23 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_coachforclient_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachforclient',
            name='age',
            field=models.IntegerField(verbose_name='Возрастная категория'),
        ),
        migrations.AlterField(
            model_name='coachforclient',
            name='group_type',
            field=models.IntegerField(verbose_name='Тип тренировки'),
        ),
        migrations.RemoveField(
            model_name='coachforclient',
            name='visit_day',
        ),
        migrations.RemoveField(
            model_name='coachforclient',
            name='visit_time',
        ),
        migrations.AlterField(
            model_name='formclient',
            name='age',
            field=models.IntegerField(verbose_name='Возрастная категория(ID)'),
        ),
        migrations.AlterField(
            model_name='formclient',
            name='class_type',
            field=models.IntegerField(verbose_name='Тип занятий(ID)'),
        ),
        migrations.RemoveField(
            model_name='formclient',
            name='location',
        ),
        migrations.RemoveField(
            model_name='formclient',
            name='section',
        ),
        migrations.RemoveField(
            model_name='formclient',
            name='visit_day',
        ),
        migrations.RemoveField(
            model_name='formclient',
            name='visit_time',
        ),
        migrations.RemoveField(
            model_name='otherdata',
            name='location',
        ),
        migrations.RemoveField(
            model_name='otherdata',
            name='section',
        ),
        migrations.AddField(
            model_name='coachforclient',
            name='visit_day',
            field=models.ManyToManyField(to='crm.days', verbose_name='Дни посещения тренировки с тренером'),
        ),
        migrations.AddField(
            model_name='coachforclient',
            name='visit_time',
            field=models.ManyToManyField(to='crm.alltime', verbose_name='Время посещения тренировки с тренером'),
        ),
        migrations.AddField(
            model_name='formclient',
            name='location',
            field=models.ManyToManyField(blank=True, null=True, to='crm.location', verbose_name='Локации которые были выбраны(ID)'),
        ),
        migrations.AddField(
            model_name='formclient',
            name='section',
            field=models.ManyToManyField(blank=True, null=True, to='crm.section', verbose_name='Секции которое были выбраны(ID)'),
        ),
        migrations.AddField(
            model_name='formclient',
            name='visit_day',
            field=models.ManyToManyField(to='crm.days', verbose_name='Дни которое было выбрано(ID)'),
        ),
        migrations.AddField(
            model_name='formclient',
            name='visit_time',
            field=models.ManyToManyField(blank=True, null=True, to='crm.alltime', verbose_name='Время которое было выбрано(ID)'),
        ),
        migrations.AddField(
            model_name='otherdata',
            name='location',
            field=models.ManyToManyField(blank=True, null=True, to='crm.location', verbose_name='Локации которые были выбраны(TEXT)'),
        ),
        migrations.AddField(
            model_name='otherdata',
            name='section',
            field=models.ManyToManyField(blank=True, null=True, to='crm.section', verbose_name='Секции которое были выбраны(TEXT)'),
        ),
    ]
