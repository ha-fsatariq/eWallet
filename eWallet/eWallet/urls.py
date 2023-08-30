
from django.contrib import admin
from django.urls import path,include
from user.views import Login,handler404
# Configure the 404 error handler
handler404 = 'user.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('', Login.as_view(), name='login'),
    path('transactions/', include('Transactions.urls')),
    path('friends/', include('Friends.urls')),
    
]
