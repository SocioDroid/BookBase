from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import datetime
class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    year = models.CharField(max_length=2)
    phoneNo = models.CharField(max_length=10,blank=False,default="9075673327")

    def __str__(self):
        return self.user.username

class Sell(models.Model):
    add_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80, blank=False, null=False)
    author = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False )
    datetime = models.DateTimeField(default=datetime.datetime.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bookImage = models.ImageField(upload_to="images/", default="images/noBook.png",blank=True, null=True)

    def __str__(self):
        return str(self.add_id)


class Notify(models.Model):
    notify_id = models.AutoField(primary_key=True)
    add_id = models.ForeignKey(Sell, on_delete=models.CASCADE,related_name="addNotify")
    buyer_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="buyerNotify")
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sellerNotify")
    datetime = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return str(self.add_id)


class Sold(models.Model):
    sold_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False )
    datetime = models.DateField(default=datetime.date.today)
