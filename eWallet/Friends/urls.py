from django.urls import path
from Friends.views import Pals,AddPals

urlpatterns = [
    path('see/', Pals.as_view(), name='pals'),
    path('add/',AddPals.as_view(),name='AddPals')
     
]
