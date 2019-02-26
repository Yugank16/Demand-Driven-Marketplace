

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demand_driven_marketplace_api.settings")

application = get_wsgi_application()

