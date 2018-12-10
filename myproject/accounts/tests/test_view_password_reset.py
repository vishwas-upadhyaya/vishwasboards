from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from django.urls import resolve
from django.test import TestCase


class PasswordResetTests(TestCase):
    def setUp(self):
        url=reverse('password_reset')
        self.response=self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_view_function(self):
        view=resolve('/reset/')
        self.assertEqual(view.func.view_class,auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_contains_form(self):
        form=self.response.context.get('form')
        self.assertIsInstance(form,PasswordResetForm)

    def test_form_input(self):
        self.assertContains(self.response,'<input',2)
        self.assertContains(self.response,'type="email"',1)

class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email='hritesh2727@gmail.com'
        User.objects.create_user(username='hritesh',email=email,password='123abcdef')
        url=reverse('password_reset')
        self.response=self.client.post(url,{'email':email})

    def test_redirection(self):
        url=reverse('password_reset_done')
        self.assertRedirects(self.response,url)

    def test_send_password_reset_email(self):
        self.assertEqual(1,len(mail.outbox))

class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url=reverse('password_reset')
        self.response=self.client.post(url,{'email':'doesnotexist@gmail.com'})

    def test_redirection(self):
        url=reverse('password_reset_done')
        self.assertRedirects(self.response,url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0,len(mail.outbox))


