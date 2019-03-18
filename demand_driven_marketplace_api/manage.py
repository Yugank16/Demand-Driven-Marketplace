import django
from django.core.management import execute_from_command_line
import os
import sys

if __name__ == "__main__":
    exists = os.path.exists('demand_driven_marketplace_api/local_settings.py')
    if exists:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demand_driven_marketplace_api.local_settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demand_driven_marketplace_api.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                    "Couldn't import Django. Are you sure it's installed and "
                    "available on your PYTHONPATH environment variable? Did you "
                    "forget to activate a virtual environment?"
                )
            raise
    execute_from_command_line(sys.argv)
