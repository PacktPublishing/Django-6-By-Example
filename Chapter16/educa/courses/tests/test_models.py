import pytest

from courses.models import Content, File, Image, Subject, Text, Video


def test_subject_str_returns_title():
    subject = Subject(title="Programming")
    assert str(subject) == subject.title


@pytest.mark.django_db
def test_course_is_linked_to_subject(subject, course):
    assert course.subject == subject
    assert course in subject.courses.all()


@pytest.mark.django_db
def test_module_belongs_to_course(course_with_modules):
    module = course_with_modules.modules.first()
    assert module.course == course_with_modules


@pytest.mark.django_db
def test_modules_get_sequential_order(course_with_modules):
    first_module = course_with_modules.modules.first()
    second_module = course_with_modules.modules.last()
    assert first_module.order == 0
    assert second_module.order == 1


@pytest.mark.django_db
@pytest.mark.parametrize("item_model", [Text, Video, Image, File])
def test_content_links_to_its_item(item_model, course_with_modules):
    module = course_with_modules.modules.first()
    item = item_model.objects.create(owner=course_with_modules.owner, title="Sample")
    content = Content.objects.create(module=module, item=item)
    assert content.item == item
    assert content in module.contents.all()
