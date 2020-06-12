
from django.contrib import admin
from django.urls import path,include
from apps.core.views import *


urlpatterns = [
    path('', include('apps.core.urls')),
    path('social/', include('social_django.urls', namespace='social')),
    path('users/', include('apps.users.urls')),
    path('api/', include('apps.restapi.urls')),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),

]

