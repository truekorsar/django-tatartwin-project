from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
from .models import TatarUser
from captcha.fields import CaptchaField
from django import forms


class TatarSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': 'Пароли не совпадают',
    }


class TatarLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class TatarRegisterForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'Пароли не совпадают',
    }

    captcha = CaptchaField(label='Введите текст с картинки',
                           error_messages={'invalid': 'Неправильный текст'})
    captcha.widget.attrs.update({'class': 'form-control'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if TatarUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    def save(self, commit=False):
        user = super().save(commit=commit)
        user.is_active = False
        user.save()
        return user

    class Meta:
        model = TatarUser
        fields = ("username", "email", "password1", "password2")



