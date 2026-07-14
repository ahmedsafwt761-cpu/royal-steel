import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royal_backend.settings')

application = get_wsgi_application()

# Auto-run migrations and create superuser on startup
from django.core.management import call_command
from django.contrib.auth.models import User

try:
    call_command('migrate', '--run-syncdb')
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@royalsteel.com', 'admin123456')
        print('Superuser created!')
    else:
        print('Superuser already exists!')
except Exception as e:
    print(f'Error: {e}')