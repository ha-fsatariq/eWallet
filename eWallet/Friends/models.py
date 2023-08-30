from django.db import models
from user.models import User
# Create your models here.
class Friend(models.Model):
  
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=100,blank=True, null=True)
    contact = models.CharField(max_length=50,blank=True, null=True)
   
    
    
    def __str__(self):
        return f"Friends nickname is {self.nickname}"