from django.core.management.base import BaseCommand, CommandError

import layzer.startup


class Command(BaseCommand):

    args = ""
    help = "Refresh all subscriptions"

    def handle(self, *args, **kwds):
        print 'ok'
