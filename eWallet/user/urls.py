from django.urls import path
from user.views import RegistrationView,Login,Logout,ConfirmEmailView
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('confirm/<str:uid>/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
]
