from django.shortcuts import render
from django.http import HttpResponseForbidden
from courses.models import Course
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def course_chat_room(request, course_id):
    try:
        course = request.user.enrolled_courses.get(id=course_id)
    except Course.DoesNotExist:
        return HttpResponseForbidden()
    else:
        context = {'course': course}
        return render(request, 'chat_room/chat.html', context)


