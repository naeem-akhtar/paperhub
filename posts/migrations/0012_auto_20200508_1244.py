# Generated by Django 3.0.5 on 2020-05-08 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_bookmark_dislike_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='posts.Post'),
        ),
    ]
