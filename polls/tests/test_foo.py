
import pytest

from polls.models import Question


@pytest.mark.django_db
class TestSomething:
    def test_id(self):
        questions = Question.objects.all()
        assert len(questions) == 1
