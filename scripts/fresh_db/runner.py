# pylint: disable=import-error,fixme,unspecified-encoding,subprocess-run-check
import subprocess
from polls.models import Question
from django.utils import timezone

PYTHON_EXEC = '/opt/venv/bin/python'
MANAGE_EXEC = f'{PYTHON_EXEC} manage.py'


class FreshDbRunner:
    funder_user_email = 'eg-funder@gmail.com'
    funder_pass = 'Trellis@123'

    def __init__(self):
        self.interactive = False

    @staticmethod
    def make_migrations():
        FreshDbRunner._run_process(f"{MANAGE_EXEC} makemigrations")

    @staticmethod
    def migrate():
        FreshDbRunner._run_process(f"{MANAGE_EXEC} migrate")

    @staticmethod
    def show_migrations():
        FreshDbRunner._run_process(f"{MANAGE_EXEC} showmigrations")

    @staticmethod
    def add_question():
        question = Question()
        question.id = 1
        question.question_text = "What's new?"
        question.pub_date = timezone.now()
        question.save()
        print("Created question") 

    @staticmethod
    def _run_process(command, capture=False):
        print(f"Running: {command}")
        if capture:
            result = subprocess.run(command,
                                    shell=True, stderr=subprocess.PIPE,
                                    stdout=subprocess.PIPE, text=True)
        else:
            result = subprocess.run(command,
                                    shell=True, text=True)
        if result.returncode != 0:
            print(f"Error running command {command}")
            raise Exception(result)

        return result

    def _run_next(self, runner):
        print('\n\n--------------------------------------------------------------------------------')
        if not self.interactive:
            print(f"Running {runner.__name__} without interaction")
            runner()
            return
        response = input(f"About to run '{runner.__name__}'.  Type 'n' to skip or enter to run:  ")
        if response.lower() == 'n':
            print("Skipping...")
            return
        runner()

    @staticmethod
    def _find_fixture_json():
        from pathlib import Path
        paths = []
        for path in Path('fixtures').rglob('*.json'):
            paths.append(str(path))

        return paths

    def run_for_test(self, call_command):
        """Intended to be run from the conftest fixture.
        Handles the cases where the data may already be in the database,
        so we're just ignoring exceptions
        """
        self.interactive = False

        def run_ignore_raised(function):
            try:
                function()
            except Exception as _:
                pass

        run_ignore_raised(FreshDbRunner.add_question)

    def run(self, interactive=False):
        self.interactive = interactive
        run_order = [
            FreshDbRunner.make_migrations,
            FreshDbRunner.migrate,
            FreshDbRunner.show_migrations,
        ]

        for func in run_order:
            self._run_next(func)

        print("\n\nCompleted Runner")


fresh_db_runner = FreshDbRunner()
