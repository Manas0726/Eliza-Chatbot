from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
# class User(AbstractUser):
#     is_admin=models.BooleanField('IS ADMIN',default=False)
#     is_user=models.BooleanField('IS USER',default=False)

