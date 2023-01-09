from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import jdatetime

def validate_password(value):
    '''
   validate the password for security
    '''
    capital, small, digi = 0, 0, 0
    capital_alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    small_alphabets = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"

    for i in value:
        if i in capital_alphabets:
            capital += 1
        if i in small_alphabets:
            small += 1
        if i in digits:
            digi += 1

    if capital < 1 or small < 1 or digi < 1:
        raise ValidationError(_('password is very short or very simple'))


def validate_year(value):
    if value < 1300:
        raise ValidationError(_('year is very small'))
    if value > jdatetime.date.today().year:
        raise ValidationError(_('this time not exist'))
