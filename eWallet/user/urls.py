from django.urls import path
from user.views import RegistrationView,Login,Logout,ConfirmEmailView,homepage,StatementHistory,loadBalance,profile
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('homepage/', homepage.as_view(), name='homepage'),
    path('confirm/<str:uid>/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('StatementHistory/', StatementHistory.as_view(), name='StatementHistory'),
    path('loadBalance/', loadBalance.as_view(), name='loadBalance'),
    path('profile/', profile.as_view(), name='profile'),
]
