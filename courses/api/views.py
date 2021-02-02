from rest_framework import generics
from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer, CourseSerializerWithmoduleAndContent
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes, api_view, action
from io import BytesIO
from rest_framework import viewsets
from .permissions import IsEnrolled

class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all().prefetch_related('modules')
    serializer_class = CourseSerializer

class CourseEnrollment(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        course.student.add(request.user)
        return Response({'enrolled': True})



# Viewsets
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all().prefetch_related('modules', 'modules__contents', 'modules__contents__content').select_related('owner', 'subject')
    serializer_class = CourseSerializer

    @action(methods=['POST'], detail=True, authentication_classes=[BasicAuthentication], permission_classes=[IsAuthenticated])
    def enroll_course(self, request, *args, **kwargs):
        course = self.get_object()
        course.student.add(request.user)
        return Response({'enrolled': True})

    @action(methods=['GET'], detail=True, authentication_classes=[BasicAuthentication], permission_classes=[IsAuthenticated, IsEnrolled], serializer_class=CourseSerializerWithmoduleAndContent)
    def content(self, request, *args, **kwargs):
        return self.retrieve(request, *args, *kwargs)

    @action(methods=["GET"], detail=False, authentication_classes=[BasicAuthentication], permission_classes=[IsAuthenticated], serializer_class=CourseSerializerWithmoduleAndContent)
    def course_list_with_content(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# Function Based API Views
@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def course_enrollment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.student.add(request.user)
    return Response({'enrolled': True})


@api_view(['GET', "HEAD"])
@permission_classes([AllowAny])
def subject_list_view(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def subject_detail_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    serialzer = SubjectSerializer(subject)
    return Response(data=serialzer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def course_list(request):
    courses = Course.objects.all().prefetch_related('modules')
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)



