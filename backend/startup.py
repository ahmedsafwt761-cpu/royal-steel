import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royal_backend.settings')

import django
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

print("Running migrations...")
call_command('migrate', verbosity=0)
print("Migrations done!")

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@royalsteel.com', 'admin123456')
    print('Superuser created!')
else:
    print('Superuser already exists!')