from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    year = models.CharField(max_length=2)

    def __str__(self):
        return self.user.username