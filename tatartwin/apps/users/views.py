import logging
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView,
)
from django.contrib.messages import success, warning
from django.template.loader import render_to_string
from django.utils.http import (
    urlsafe_base64_encode as b64encode,
    urlsafe_base64_decode as b64decode
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator as TokenGenerator
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .models import TatarUser

activation_logger = logging.getLogger('activation')


class TatarPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset/password_reset_form.html'
    subject_template_name = 'users/password_reset/subject.txt'
    email_template_name = 'users/password_reset/password_reset_email.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if TatarUser.objects.filter(email=form.cleaned_data['email']).exists():
            success(self.request, 'Письмо с ссылкой на изменение пароля отправлено!')
            super().form_valid(form)
        else:
            warning(self.request, 'Письмо по указанному адресу не отправлено! Попробуйте еще раз.')
            super().form_invalid(form)

        return redirect(self.success_url)


class TatarPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset/password_change.html'
    success_url = reverse_lazy('home')
    form_class = TatarSetPasswordForm

    def form_valid(self, form):
        success(self.request, 'Пароль изменен!')
        return super().form_valid(form)


class TatarLoginView(LoginView):
    template_name = 'users/auth/login.html'
    authentication_form = TatarLoginForm

    def form_valid(self, form):
        success(self.request, 'Вы вошли!')
        return super().form_valid(form)


class TatarLogoutView(LogoutView):
    pass


def register(request):
    if request.method == 'GET':
        form = TatarRegisterForm()
    else:
        form = TatarRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = TokenGenerator().make_token(user)
            current_site = get_current_site(request)
            email_subject = 'Активация аккаунта'
            activation_context = {
                'user': user,
                'domain': current_site.domain,
                'uid': b64encode(str(user.pk).encode()),
                'token': token
            }
            message = render_to_string('users/auth/activation_message.html', activation_context)
            send_mail(email_subject, message, settings.EMAIL_HOST_USER, [user.email])
            success(request, "Письмо отправлено, проверьте вашу почту.")
            return redirect('home')

    return render(request, 'users/auth/register.html', {'form': form})


def activate(request, uid, token):
    try:
        pk = b64decode(uid).decode()
        user = TatarUser.objects.get(pk=int(pk))
        if TokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            success(request, "Теперь вы можете войти в свой аккаунт!")
            activation_logger.info('Registered!')
        else:
            warning(request, "Ссылка не валидна!")
            activation_logger.warning('Link invalid!')
    except (UnicodeDecodeError, ObjectDoesNotExist, ValueError, TypeError):
        warning(request, "Активация не удалась! Попробуйте зарегистрироваться снова.")
        activation_logger.exception('Activation failed!')
    finally:
        return redirect('home')



