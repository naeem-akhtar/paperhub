# Generated by Django 3.0.5 on 2020-05-18 12:08

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('posts', '0017_auto_20200517_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='posts.PostTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
