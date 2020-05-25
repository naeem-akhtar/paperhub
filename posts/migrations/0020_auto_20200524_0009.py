# Generated by Django 3.0.5 on 2020-05-23 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('posts', '0019_posttag_follower'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posttag',
            name='follower',
        ),
        migrations.CreateModel(
            name='PostTagExtended',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.ManyToManyField(related_name='tags_following', to=settings.AUTH_USER_MODEL)),
                ('tag', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='taggit.Tag')),
            ],
        ),
    ]