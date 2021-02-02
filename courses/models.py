from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import os
from .utils import file_location, image_location
from .fields import OrderField
from .utils import course_image
from easy_thumbnails.fields import ThumbnailerImageField
from django.template.loader import render_to_string

# Create your models here.

class Subject(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        index_together = ('id', "slug")

class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    owner =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created')
    title = models.CharField(max_length=200, db_index=True)
    image = ThumbnailerImageField(upload_to=course_image, default='images/default.png')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    overview = models.TextField()
    student = models.ManyToManyField(User, related_name='enrolled_courses')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)
        index_together = ('id', 'slug')

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    order = OrderField(for_fields=['course'], blank=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name

class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='contents')
    order = OrderField(for_fields=['module'], blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('text', 'file', 'image', 'video')})
    content_id = models.PositiveIntegerField()
    content = GenericForeignKey('content_type', 'content_id')

    class Meta:
        ordering = ('order',)

class AbstractContent(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='%(class)s_contents')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        return render_to_string(f'contents/{self._meta.model_name}.html', context={'item': self})

    def __str__(self):
        return self.title



class Text(AbstractContent):
    content = models.TextField()
    
class File(AbstractContent):
    file = models.FileField(upload_to=file_location)

class Image(AbstractContent):
    image = models.ImageField(upload_to=image_location)

class Video(AbstractContent):
    url = models.URLField()