from time import sleep
from django.core.management import call_command
import pytest

from polls.models import Question

from scripts.fresh_db.runner import FreshDbRunner


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # see if we have any data
        question = Question.objects.filter(id=1).last()
        if not question:
            # doesn't exist.   run through the new db setup
            print("######################### Database doesn't exist creating data #########################")
            runner = FreshDbRunner()
            runner.run_for_test(call_command)
            print('sleeping 30 seconds... painful')
            sleep(30)
