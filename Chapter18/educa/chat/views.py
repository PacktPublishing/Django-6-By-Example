from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from courses.models import Course


@login_required
def course_chat_room(request, course_id):
    # retrieve course with given id owned or joined by the current user, or 404 if neither
    course = get_object_or_404(
        Course.objects.filter(
            Q(owner=request.user) | Q(students=request.user)
        ).distinct(),
        id=course_id,
    )
    # retrieve chat history
    latest_messages = course.chat_messages.select_related("user").order_by("-id")[:5]
    latest_messages = reversed(latest_messages)
    return render(
        request,
        "chat/room.html",
        {"course": course, "latest_messages": latest_messages},
    )
