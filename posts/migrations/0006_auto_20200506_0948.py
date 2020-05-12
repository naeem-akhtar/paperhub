# Generated by Django 3.0.5 on 2020-05-06 04:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20200506_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_modifed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]