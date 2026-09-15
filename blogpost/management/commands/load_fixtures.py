import time
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        time.sleep(1)
        print("fixture 1 loaded")
        time.sleep(1)
        print("fixture 2 loaded")
        time.sleep(3)
        print("fixture 3 loaded")
