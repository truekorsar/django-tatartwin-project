from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('tatar_word_ajax', tatar_word_ajax, name='tatar_word_ajax'),
    path('history/', show_history, name='show_history'),
    path('top/', TopTatarListView.as_view(), name='show_top'),
    path('detail/<int:pk>', TatarDetailView.as_view(), name='show_detail'),

]