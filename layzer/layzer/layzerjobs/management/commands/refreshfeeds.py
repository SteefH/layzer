from django.core.management.base import BaseCommand

import layzer.startup
from layzer.layzerjobs import UpdateFeedsJob

class Command(BaseCommand):

    args = ""
    help = "Refresh all subscriptions"

    def handle(self, *args, **kwds):
        UpdateFeedsJob().run()
