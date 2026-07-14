import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royal_backend.settings')

application = get_wsgi_application()

# Auto-run migrations and create superuser on startup
# Only run once, not on every worker spawn
import threading
_run_once = threading.Lock()

with _run_once:
    try:
        from django.core.management import call_command
        from django.contrib.auth.models import User
        call_command('migrate', verbosity=0)
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@royalsteel.com', 'admin123456')
            print('Superuser created!')
        else:
            print('Superuser already exists!')
    except Exception as e:
        print(f'Error during startup: {e}')