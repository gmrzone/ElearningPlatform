from django.urls import path, include
from .views import SubjectListView, SubjectDetailView, CourseEnrollment, CourseListView
from .views import subject_list_view, subject_detail_view, course_enrollment, course_list
from rest_framework import routers
from .views import CourseViewSet, SubjectViewSet


router = routers.DefaultRouter()
router.register(r'subject_viewset', SubjectViewSet)
router.register(r"course_viewset", CourseViewSet)

app_name = 'courses'

urlpatterns = [
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/<int:pk>/', SubjectDetailView.as_view(), name="subject_detail"),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('course/enroll/<int:course_id>/', CourseEnrollment.as_view(), name='course_enrollment'),
    path('', include(router.urls))
]


# Function based Views
function_paths = [
    path('subjects/function/', subject_list_view, name='subject_list_function'),
    path('subjects/function/<int:subject_id>/', subject_detail_view, name='subject_detail_function'),
    path('course/enroll/<int:course_id>/function/', course_enrollment, name='course_enrollment_function'),
    path('course/function/', course_list, name='course_list_function')
]
urlpatterns.extend(function_paths)
