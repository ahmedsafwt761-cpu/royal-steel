from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # 1. Apply migrations
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Migrations applied!'))
        
        # 2. Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin', 
                'admin@royalsteel.com', 
                'admin123456'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created!'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists!'))
# test