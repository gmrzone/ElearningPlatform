from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Course, Module, Content, Subject
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import FormView
from .forms import LoginForm, ModuleFormSet
from django.forms.models import modelform_factory
from django.apps import apps
from django.forms import TextInput, URLInput, FileInput, Textarea
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from django.views.generic.detail import DetailView
from students.forms import EnrollmentForm
from django.core.cache import cache
from django.contrib.auth import login, authenticate
from django.core.cache import cache
# Create your views here.

class OwnMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(owner=self.request.user)
        return qs

class OwnEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CourseOwnMixin(OwnMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['title', 'subject', 'slug', 'overview']
    success_url = reverse_lazy('courses:manage_course_list')
    

class CourseOwnEditMixin(OwnEditMixin, CourseOwnMixin):
    template_name  = "courses/form.html"


class ListCourse(CourseOwnMixin, ListView):
    template_name = 'courses/list.html'
    context_object_name = "courses"
    permission_required = 'courses.view_course'


class CreateCourse(CourseOwnEditMixin, CreateView):
    permission_required = 'courses.add_course'


class UpdateCourse(CourseOwnEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class DeleteCourse(CourseOwnMixin, DeleteView):
    template_name = 'courses/delete.html'
    permission_required = 'courses.delete_course'


class ModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/module_formset.html'
    course = None

    def dispatch(self, request, course_id):
        key = f"selected_course_{course_id}"
        self.course = cache.get(key)
        if not self.course:
            self.course = get_object_or_404(Course, id=course_id)
            cache.set(key, self.course)
        return super().dispatch(request, course_id)

    def get_formset(self, data=None):
        formset = ModuleFormSet(instance=self.course, data=data)
        return formset

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = {'formset': formset, 'course': self.course}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:manage_course_list')
        return self.render_to_response({'formset': formset, 'course': self.course})

class ContentCreateUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/content_form.html'
    module = None
    content_model = None
    content_obj = None

    def get_model(self, model_name):
        content_model_names = ['text', 'image', 'video', 'file']
        if model_name in content_model_names:
            model = apps.get_model(app_label='courses', model_name=model_name)
            return model
        return None

    def dispatch(self, request, module_id, model_name, content_id=None):
        self.module = get_object_or_404(Module, id=module_id)
        self.model = self.get_model(model_name)
        if content_id:
            self.content_obj = get_object_or_404(self.model, id=content_id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['created', 'updated', 'owner'], widgets={
            'title': TextInput(attrs={'placeholder': "Content Title", 'class': 'form-control'}),
            'url' : URLInput(attrs={'placeholder': 'Video URL', 'class': 'form-control'}),
            'image': FileInput(attrs={'class': 'form-control'}),
            'file': FileInput(attrs={'class': 'form-control'}),
            'content': Textarea(attrs={'placeholder':'Text Content', 'class': 'form-control'})
        })
        return Form(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.get_form(self.model, instance=self.content_obj)
        context = {'form': form, 'content_obj': self.content_obj}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.model, instance=self.content_obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            if not self.content_obj:
                Content.objects.create(module=self.module, content=instance)
            return redirect('courses:module_list_content', self.module.id)
        return self.render_to_response({'form': form, 'content_obj': self.content_obj})

class ContentDeleteView(View):

    def post(self, request, content_id):
        content = get_object_or_404(Content, id=content_id)
        module = content.module
        content.content.delete()
        content.delete()
        return redirect('module_list_content', module.id)

class ModuleListView(TemplateResponseMixin, View):
    template_name = 'courses/module_list_view.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module.objects.select_related('course').prefetch_related('contents', 'course__modules'), id=module_id, course__owner=request.user)
        context = {'module': module}
        return self.render_to_response(context)

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': "ok"})

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        print(self.request_json)
        for id, o in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=o)
        return self.render_json_response({'saved': 'ok'})

class CourseListView(TemplateResponseMixin, View):
    template_name = 'courses/courses_list.html'
    model = Course
    
    def get(self, request, subject=None):
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(courses_count=Count('courses'))
            cache.set('all_subjects', subjects)
        all_courses = Course.objects.annotate(module_count=Count('modules'))
        
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = f"subject_{subject.id}_courses"
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        return self.render_to_response({'subject': subject, 'subjects': subjects, 'courses': courses})

class CourseDetail(DetailView):
    template_name = 'courses/course_detail.html'
    model = Course

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['enrollment_form'] = EnrollmentForm(initial={'course': self.object})
        return context


def home(request):
    return HttpResponse("Home")


class LoginView(FormView):
    template_name = 'authentication/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        cd = form.cleaned_data
        username = cd['username']
        password = cd['password']
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        instructor_group = cache.get('instructor_group')
        if not instructor_group:
            instructor_group = Group.objects.get(name='instructor')
            cache.set('instructor_group', instructor_group)
        if instructor_group in user.groups.all():
            return redirect('courses:manage_course_list')
        else:
            return redirect('courses:course_list')
            






