from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from ..views import signup
from django.contrib.auth.models import User
from ..forms import SignUpForm

class Sign_Up_Tests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
    def test_signup_status_code(self):

        self.assertEqual(self.response.status_code,200)

    def test_signup_url_resolves_signup_view(self):
        view=resolve('/signup/')
        self.assertEqual(view.func,signup)

    def csrf_test(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_creation_form(self):
        form=self.response.context.get('form')
        self.assertIsInstance(form,SignUpForm)

    def test_form_inputs(self):
        self.assertContains(self.response,'<input',5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class SuccessfulSignUpTests(TestCase):
        def setUp(self):
            url=reverse('signup')
            data={
                'username':'hritesh',
                'email':'hritesh2727@gmail.com',
                'password1':'abcdef123456',
                'password2':'abcdef123456'
            }
            self.response=self.client.get(url,data)
            self.home_url=reverse('home')

        def test_redirection(self):
            self.assertRedirects(self.response,self.home_url)

        def test_user_creation(self):
            self.assertTrue(User.objects.exists())

        def test_user_authentication(self):
            response=self.client.get(self.home_url)
            user=response.context.get('user')
            self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
        def setUp(self):
            url=reverse('signup')
            self.response=self.client.get(url,{})

        def test_signup_status_code(self):
            self.assertEqual(self.response.status_code,200)

        def test_form_errors(self):
            form=self.response.context.get('form')
            self.assertTrue(form.errors)

        def test_dont_create_user(self):
            self.assertFalse(User.objects.exists())

class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form=SignUpForm()
        expected=['username','email','password1','password2',]
        actual=list(form.fields)
        self.assertSequenceEqual(expected,actual)





# Create your tests here.
