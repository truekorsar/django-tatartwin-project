from django.views.generic.base import TemplateView
from django.urls import path
from .views import *


urlpatterns = [
    path('spec', TemplateView.as_view(template_name='users/auth/specification.html'), name='auth_spec'),
    path('login', TatarLoginView.as_view(), name='login'),
    path('logout', TatarLogoutView.as_view(), name='logout'),
    path('register', register, name='register'),
    path('activate/<str:uid>/<str:token>', activate, name='activate'),
    path('password_reset', TatarPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<str:uidb64>/<str:token>', TatarPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]