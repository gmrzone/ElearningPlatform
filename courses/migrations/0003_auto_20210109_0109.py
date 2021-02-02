# Generated by Django 3.1.5 on 2021-01-09 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('courses', '0002_content_file_image_text_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ('text', 'file', 'image', 'video')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]