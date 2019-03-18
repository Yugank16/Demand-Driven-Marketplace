from __future__ import unicode_literals

from django.contrib import admin

from apps.users.models import User

admin.site.register(User)
