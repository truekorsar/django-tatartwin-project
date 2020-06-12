"""Form for validating the input on the main page"""

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class WordFieldValidator:
    """
    Validator for the form

    Checks if the input matches the following patterns:
        '^[А-Яа-яЁёӘәҖҗӨөһҺҢңҮү\s]+$'
                    OR
        '^[А-Яа-яЁё\s]+$'

    The validator's result depends on whether the authenticated user is looking for a word or not (AnonymousUser).
    """

    def __init__(self, is_authenticated, *args, **kwargs):
        self.is_authenticated = is_authenticated

    def __call__(self, val):
        if self.is_authenticated:
            RegexValidator(regex='^[А-Яа-яЁёӘәҖҗӨөһҺҢңҮү\s]+$',
                           message="Допустимы только буквы татарского алфавита и пробел!")(val)
        elif not set(val).isdisjoint(set("ӘәҖҗӨөһҺҢңҮү")):
            raise ValidationError("Ввод специальных татарских символов станет доступен только после входа на сайт!")
        else:
            RegexValidator(regex='^[А-Яа-яЁё\s]+$',
                           message="Допустимы только буквы татарского алфавита и пробел!\n"
                                   "P.S. После входа на сайт станут доступны специальные татарские символы.")(val)


class WordForm(forms.Form):
    """The form itself"""

    def __init__(self, *args, is_authenticated=False, **kwargs):
        super().__init__(*args, **kwargs)
        word = forms.CharField(label=False, max_length=50, validators=[WordFieldValidator(is_authenticated)])
        word.widget.attrs.update({'class': 'form-control', 'placeholder': f'Максимум {word.max_length} символов'})
        word.error_messages = {'required': 'Введите хотя бы 1 букву'}
        self.fields['word'] = word

