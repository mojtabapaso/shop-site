from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from .forms import UserRegisterForm, UserLoginForm
from .views import RegisterView, LoginView, LogoutView
import pdb; pdb.set_trace()

#
# class UserTests(TestCase):
#     def test_create_user(self):
#         User = get_user_model()
#         user = User.objects.create_user(email='mojtabaataei@email.com', phone_number='09335215295',
#                                         first_name='mojtaba',
#                                         last_name='ataei', date_of_birth='1379-12-28', password='test')
#
#         self.assertEqual(user.email, 'mojtabaataei@email.com')
#         self.assertEqual(user.first_name, 'mojtaba')
#         self.assertEqual(user.last_name, 'ataei')
#         self.assertEqual(user.date_of_birth, '1379-12-28')
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_admin)
#         self.assertFalse(user.is_staff)


# class UserLoginTest(TestCase):
#     def setUp(self):
#         url = reverse('accounts:login')
#         self.response = self.client.get(url)
#
#     def test_user_login_templates(self):
#         self.assertEqual(self.response.status_code, 200)
#         self.assertTemplateUsed(self.response, 'accounts/login.html')
#
#     def test_user_login_form(self):
#         form = self.response.context.get('form')
#         # self.assertIsInstance(form, UserLoginForm)
#         self.assertContains(self.response, 'csrfmiddlewaretoken')


# class UserLogoutTest(TestCase):
#     def setUp(self):
#         url = reverse('accounts:logout')
#         self.response = self.client.get(url)
#
#     # def test_user_logout_templates(self):
#     # self.assertEqual(self.response.status_code, 200) why 302 != 200
#     def test_user_logout_view(self):
#         view = resolve('/accounts/logout/')
#         self.assertEqual(view.func.__name__, LogoutView.as_view().__name__)
#

class UserRegisterTEst(TestCase):
    def setUp(self):
        url = reverse('accounts:register')
        self.response = self.client.get(url)

    def test_register_templates(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/register.html')

    def test_register_from(self):
        z = self.response.context.get('form')
        # print(form.errors)

        # self.assertIsInstance(form, UserRegisterForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_register_view(self):
        pass
