from django.db import models
from user.models import User
from django.utils import timezone



class Transaction(models.Model):
  
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20)
    otheruser = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    
    
    def __str__(self):
        return f"Transaction {self.id} - {self.transaction_type} by {self.user}"
