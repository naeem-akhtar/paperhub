# Generated by Django 3.0.5 on 2020-05-13 18:34

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_profile_thumbnail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userconnection',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(blank=True, null=True, verbose_name='DOB'),
        ),
    ]
