import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_course_list_view_returns_courses(client, settings, course):
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "test-course-list-view",
        }
    }
    response = client.get(reverse("course_list"))
    assert response.status_code == 200
    assert "Testing with pytest" in response.content.decode()
