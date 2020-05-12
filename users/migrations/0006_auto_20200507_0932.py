# Generated by Django 3.0.5 on 2020-05-07 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200507_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], default='OTHER', max_length=10, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(blank=True, null=True, verbose_name='DOB'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pictures/default_thumbnail.jpg', upload_to='profile_pictures', verbose_name='User Avatar'),
        ),
    ]
