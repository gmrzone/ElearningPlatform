from django.contrib import admin
from .models import Subject, Course, Module
# Register your models here.

admin.site.index_template = 'memcache_status/admin_index.html'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', "slug", 'subject', 'created')
    list_editable = ("slug",)
    prepopulated_fields =  {'slug': ('title',)}
    inlines = [ModuleInline]