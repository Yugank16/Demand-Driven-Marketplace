# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from apps.bids.models import Bid,ItemImage

admin.site.register(Bid)
admin.site.register(ItemImage)
