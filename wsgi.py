"""
WSGI config for InformatikaLab project (Root wrapper).
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Avtomatik migratsiya va boshlang'ich ma'lumotlarni tekshirish (Render kabi hostinglar uchun)
try:
    import django
    django.setup()
    from django.core.management import call_command
    call_command('migrate', interactive=False)
    
    from projects.models import ProjectTemplate
    if not ProjectTemplate.objects.exists():
        call_command('seed_data')
except Exception as e:
    print(f"Startup database initialization error or notice: {e}")

application = get_wsgi_application()
