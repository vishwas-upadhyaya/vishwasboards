from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='john',email='john@doe.com',password='123')
        self.response=self.client.get(reverse('password_reset'),{'email':'john@doe.com'})
        self.email=mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('[Django Password] Please reset your password',self.email.subject)

