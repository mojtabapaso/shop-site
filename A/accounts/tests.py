from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='mojtaba@email.com', phone_number='09335215295', first_name='mojtaba',
                                        last_name='ataei', date_of_birth='1379-12-28', password='test')

        self.assertEqual(user.email, 'mojtaba@email.com')
        self.assertEqual(user.first_name, 'mojtaba')
        self.assertEqual(user.last_name, 'ataei')
        self.assertEqual(user.date_of_birth, '1379-12-28')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        # self.assertFalse(user.is_superuser)
