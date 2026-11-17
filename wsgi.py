import os
import sys
from pathlib import Path

# Add informatikalab to sys.path
root_dir = Path(__file__).resolve().parent
app_dir = root_dir / 'informatikalab'
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
