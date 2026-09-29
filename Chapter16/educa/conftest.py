import pytest
from django.contrib.auth import get_user_model

from courses.models import Course, Module, Subject

User = get_user_model()


@pytest.fixture
def owner():
    return User.objects.create_user(username="instructor", password="password123")


@pytest.fixture
def subject():
    return Subject.objects.create(title="Programming", slug="programming")


@pytest.fixture
def course(owner, subject):
    return Course.objects.create(
        owner=owner,
        subject=subject,
        title="Testing with pytest",
        slug="testing-with-pytest",
        overview="Write and run tests with pytest.",
    )


@pytest.fixture
def course_with_modules(course):
    Module.objects.create(course=course, title="Introduction to pytest")
    Module.objects.create(course=course, title="Fixtures and test data")
    return course
