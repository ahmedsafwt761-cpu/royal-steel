from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Migrations applied!'))