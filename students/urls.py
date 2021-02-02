from django.urls import path
from .views import StudentRegistration, StudentEnrollment, StudentCourseDetail, StudentCoursesListView
app_name = 'student'

urlpatterns = [
    path('students/registration/', StudentRegistration.as_view(), name='student_registration'),
    path('students/enroll', StudentEnrollment.as_view(), name='enroll'),
    path('enrolled/', StudentCoursesListView.as_view(), name='student_course_list'),
    path('enrolled/detail/<pk>/', StudentCourseDetail.as_view(), name="student_course_detail"),
    path('enrolled/detail/<pk>/<int:module_id>/', StudentCourseDetail.as_view(), name="student_course_detail_module"),
]