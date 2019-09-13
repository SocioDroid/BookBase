from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    year = models.CharField(max_length=2)

    def __str__(self):
        return self.user.username
class Sell(models.Model):

    title = models.CharField(max_length=80, blank=False, null=False)
    author = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=150, blank=False, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
