from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BidConfig(AppConfig):
    name = 'apps.bids'

    def ready(self):
        import apps.bids.signals
