from django.urls import path
from django.conf.urls import handler404
from user.views import RegistrationView,Logout,ConfirmEmailView,homepage,StatementHistory,loadBalance,profile,ForgotPassword,handler404
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('homepage/', homepage.as_view(), name='homepage'),
    path('confirm/<str:uid>/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('StatementHistory/', StatementHistory.as_view(), name='StatementHistory'),
    path('loadBalance/', loadBalance.as_view(), name='loadBalance'),
    path('profile/', profile.as_view(), name='profile'),
    path('forgotPassword/', ForgotPassword.as_view(), name='forgotPassword'),
    
    

]
