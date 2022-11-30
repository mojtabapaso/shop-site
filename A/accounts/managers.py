from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, first_name, last_name, date_of_birth, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not phone_number:
            raise ValueError('User must have an phone number')
        if not first_name:
            raise ValueError('User must have an first name')
        if not last_name:
            raise ValueError('User must have an last name')
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, last_name, email, date_of_birth, password=None):
        user = self.create_user(
            first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, password=password,
            date_of_birth=date_of_birth,)

        user.is_admin = True
        # user.is_superuser = True
        user.save(using=self._db)
        return user