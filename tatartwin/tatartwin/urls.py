
from django.contrib import admin
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from apps.graphapi.schema import schema
from apps.core.views import *


urlpatterns = [
    path('', include('apps.core.urls')),
    path('social/', include('social_django.urls', namespace='social')),
    path('users/', include('apps.users.urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)), name='spec'),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),

]

