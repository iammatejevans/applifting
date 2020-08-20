import subprocess

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Test some code"

    def handle(self, *args, **options):
        subprocess.Popen(["python", "manage.py", "check_offers"])
        subprocess.Popen(["python", "manage.py", "runserver", "0.0.0.0:8000"])
