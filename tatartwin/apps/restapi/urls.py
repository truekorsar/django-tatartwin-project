
from django.urls import path
from .views import *


urlpatterns = [
    path('spec', api_spec, name='spec'),
    path('twin/<str:word>', TatarRetrieveAPI.as_view(), name='twin'),
    path('twin_full/<str:word>', TatarFullRetrieveAPI.as_view(), name='twin_full'),
    path('top/<int:number>', TatarTopAPI.as_view(), name='top'),

]