# Generated by Django 3.0.5 on 2020-05-05 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20200505_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='document',
            field=models.FileField(upload_to='documents'),
        ),
    ]