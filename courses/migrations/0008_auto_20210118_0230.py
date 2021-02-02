# Generated by Django 3.1.5 on 2021-01-18 10:30

import courses.utils
from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(default='images/default.png', upload_to=courses.utils.course_image),
        ),
    ]