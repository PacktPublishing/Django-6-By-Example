import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_enroll_course_view_enrolls_auth_user(client, course):
    student = User.objects.create_user(username="student", password="password123")
    client.force_login(student)
    response = client.post(reverse("student_enroll_course"), {"course": course.id})
    assert response.status_code == 302
    assert student in course.students.all()
