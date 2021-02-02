from django.urls import path
from .views import home, CreateCourse, UpdateCourse, DeleteCourse, ListCourse, ModuleUpdateView, ContentCreateUpdateView, ContentDeleteView, ModuleListView
from .views import ModuleOrderView, ContentOrderView, CourseListView, CourseDetail
from django.views.decorators.cache import cache_page
app_name = "courses"

urlpatterns = [
    path('', CourseListView.as_view(), name="course_list"),
    path('<slug:subject>/', CourseListView.as_view(), name='course_list_subject'),
    path('detail/<slug:slug>/', cache_page(60 * 5)(CourseDetail.as_view()), name='course_detail'),
    path('courses/my-courses/', ListCourse.as_view(), name="manage_course_list"),
    path('courses/create/', CreateCourse.as_view(), name="create_course"),
    path('courses/<pk>/edit/', UpdateCourse.as_view(), name="update_course"),
    path('courses/<pk>/delete/', DeleteCourse.as_view(), name="delete_course"),
    path('courses/<course_id>/modules/', ModuleUpdateView.as_view(), name='update_module'),
    path('courses/modules/<int:module_id>/contents/<model_name>/', ContentCreateUpdateView.as_view(), name='module_content_create'),
    path('courses/modules/<int:module_id>/contents/<model_name>/<int:content_id>/', ContentCreateUpdateView.as_view(), name='module_content_update'),
    path('courses/modules/contents/<int:content_id>/', ContentDeleteView.as_view(), name='module_content_delete'),
    path('courses/modules/<int:module_id>/', ModuleListView.as_view(), name='module_list_content'),
    path('reorder/m/', ModuleOrderView.as_view(), name='module_reorder'),
    path('reorder/c/', ContentOrderView.as_view(), name='content_reorder'),
]

