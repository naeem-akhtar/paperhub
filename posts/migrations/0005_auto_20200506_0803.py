# Generated by Django 3.0.5 on 2020-05-06 02:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20200505_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='document',
            field=models.FileField(upload_to='documents', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]),
        ),
    ]
