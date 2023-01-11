from ..models import User, OtpCode, Profile
from django.test import TestCase


class UserModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(phone_number='09335215295', password='123456')
        admin = User.objects.create_superuser(phone_number='09331111111', password='123456')

    def test_user(self):
        user = User.objects.get(id=1)
        phone_number = f'{user.phone_number}'
        password = f'{user.password}'
        self.assertFalse(password == '123456')
        self.assertEqual(phone_number, '09335215295')
        self.assertFalse(user.is_admin)
        self.assertTrue(user.is_active)

    def test_user_admin(self):
        admin = User.objects.get(id=2)
        phone_number = f'{admin.phone_number}'
        password = f'{admin.password}'
        self.assertFalse(password == '123456')
        self.assertEqual(phone_number, '09331111111')
        self.assertTrue(admin.is_admin)
        self.assertTrue(admin.is_active)

    def test_str_user(self):
        """ test __str__ """
        user = User(phone_number='09331111111')
        self.assertEqual(str(user), user.phone_number)


class OtpCodeTest(TestCase):
    def setUp(self):
        otp_code = OtpCode.objects.create(phone_number='09331111111', code=11111)

    def test_str_otp(self):
        otp = OtpCode(phone_number='09331111111', code=11111)
        self.assertEqual(str(otp), f'{otp.phone_number} - {otp.code} ')

    def test_otp(self):
        otp = OtpCode.objects.get(id=1)
        phone_number = f"{otp.phone_number}"
        code = otp.code
        self.assertEqual(phone_number, '09331111111')
        self.assertEqual(code, 11111)


class ProfileModelTest(TestCase):
    def setUp(self):
        user=User.objects.create_user(phone_number='09335215295', password='123456')
        # user = User.objects.get(id=1)

        profile = Profile.objects.create(user=user, date_of_berth='1379-12-28', first_name='mojtaba', last_name='ataei',
                                         email='mojtabapaso@gmail.com')

    def test_str_profile(self):
        pass

    def test_profile(self):
        profile = Profile.objects.get(id=1)
        user = User.objects.last()
        first_name = profile.first_name
        last_name = profile.last_name
        date_of_berth = profile.date_of_berth
        user_profile = profile.user
        email = profile.email
        self.assertEqual(user_profile, user)
