# Generated by Django 4.2 on 2023-04-19 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_remove_age_key_remove_days_key_remove_grouptype_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formclient',
            name='age',
            field=models.CharField(max_length=100, verbose_name='Возрастная категория(ID)'),
        ),
        migrations.AlterField(
            model_name='formclient',
            name='class_type',
            field=models.CharField(max_length=100, verbose_name='Тип занятий(ID)'),
        ),
        migrations.AlterField(
            model_name='formclient',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.clients'),
        ),
        migrations.AlterField(
            model_name='formclient',
            name='location',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Локации которые были выбраны(ID)'),
        ),
        migrations.AlterField(
            model_name='formclient',
            name='section',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Секции которое были выбраны(ID)'),
        ),
        migrations.AlterField(
            model_name='formclient',
            name='visit_day',
            field=models.CharField(max_length=1000, verbose_name='Дни которое было выбрано(ID)'),
        ),
        migrations.AlterField(
            model_name='formclient',
            name='visit_time',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Время которое было выбрано(ID)'),
        ),
    ]
