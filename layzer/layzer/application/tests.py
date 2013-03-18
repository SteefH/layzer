"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.exceptions import MiddlewareNotUsed

class AddSubscriptionTest(TestCase):

    def setUp(self):
        import logging
        logging.disable(logging.DEBUG)
        from django.contrib.auth.models import User
        self.user_1 = User(username="user 1")
        self.user_1.save()
        self.user_2 = User(username="user 2")
        self.user_2.save()

        from layzer.application.middleware import DependencyInjectionMiddleware as di
        import beject
        try:
            di()
        except MiddlewareNotUsed:
            pass
        self.subscriptions_service = beject.get('SubscriptionService')
        self.subscription_model = beject.get('subscription_model')

    def test_add_subscription(self):

        self.subscriptions_service.add_subscription('http://steeffie.net', self.user_1)

        self.assertRaises(
            self.subscriptions_service.AlreadySubscribedException,
            self.subscriptions_service.add_subscription,
                'http://steeffie.net', self.user_1
        )


        self.assertRaises(
            self.subscriptions_service.AlreadySubscribedException,
            self.subscriptions_service.add_subscription,
                'http://fotolog.steeffie.net/', self.user_1
        )

        self.subscriptions_service.add_subscription('http://steeffie.net', self.user_2)


        self.assertEqual(len(self.subscription_model.objects.all()), 2)
