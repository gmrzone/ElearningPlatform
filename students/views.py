from django.shortcuts import render, redirect
from .forms import RegistrationForm, EnrollmentForm
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView




class StudentRegistration(CreateView):
    template_name = "registration/student.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('courses:course_list')

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        cd = form.cleaned_data
        username = cd['username']
        password = cd['password1']
        user = authenticate(request=self.request, username=username, password=password)
        login(self.request, user)
        return valid_form

class StudentEnrollment(LoginRequiredMixin, FormView):
    form_class = EnrollmentForm
    course = None

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.student.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student:student_course_list', args=[self.course.id])

class StudentCoursesListView(ListView):
    model = Course
    template_name = "afzal/enrolled_courses.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(student__in=[self.request.user])

class StudentCourseDetail(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "afzal/enrolled_course_detail.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(student__in=[self.request.user])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs.get('module_id'))
        else:
            context['module'] = course.modules.all()[0]
        return context
