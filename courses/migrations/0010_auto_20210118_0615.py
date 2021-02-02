# Generated by Django 3.1.5 on 2021-01-18 14:15

import courses.utils
from django.conf import settings
from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0009_auto_20210118_0241'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='student',
            field=models.ManyToManyField(related_name='enrolled_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(default='images/default.png', upload_to=courses.utils.course_image),
        ),
    ]
