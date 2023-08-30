from django.urls import path
from Transactions.views import *

urlpatterns = [
    path('transferFund/', fundsTransfer.as_view(), name='transferFund'),
    path('accountStatement/', accountStatement.as_view(), name='accountStatement'),
     
]
