from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission
from cloudinary.models import CloudinaryField
from django.contrib.auth.hashers import make_password
class User(AbstractUser):

    id = models.AutoField(primary_key=True)
    cnic = models.CharField(max_length=16)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    profileImage = CloudinaryField('image')
    amount = models.CharField(max_length=16, default=0)
    attempts = models.CharField(max_length=16,default=0)

    groups = models.ForeignKey(Group, related_name='custom_users',on_delete=models.CASCADE)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users',blank=True)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password for new instances
            self.password = make_password(self.password)
            # Add the default group to the user
            default_group_name = 'AppUser'  # Replace with the actual group name
            default_group = Group.objects.get(name=default_group_name)
            self.groups = default_group
        super().save(*args, **kwargs)
    