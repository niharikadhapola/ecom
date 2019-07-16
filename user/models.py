from django.db import models

from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True


# Create your models here.
class UserProfile(models.Model):
    CHOICES = (('vendor', 'vendor'), ('user', 'user'))
    category = models.CharField(max_length=100, choices=CHOICES, default='individual')

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)

    def __str__(self):
      return self.user.username


#feedback form
class posts(models.Model):
    name = models.CharField(max_length=400)
    phone = models.IntegerField()

    describe = models.TextField(blank=True, null=True)

    def __str__(self):
      return self.name

#items data
class data(models.Model):
    vendor_name = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    price = models.IntegerField()
    img = models.ImageField(upload_to='images/')


    def __str__(self):
      return self.name

#cart data of user
class cart(models.Model):
    CHOICES = (('initial', 'int'), ('cod', 'cod'), ('payment_done', 'payment_done'),('delievered', 'delieverd'))
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(data, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status=models.CharField(max_length=100, choices=CHOICES, default='int')

    def __str__(self):

        return '%s' % (self.name)
#order detail
class Orderdetail(models.Model):
    name = models.CharField(max_length=400)
    buyername = models.CharField(max_length=400)
    address = models.CharField(max_length=400)
    state = models.CharField(max_length=400)
    phone = models.IntegerField()
    def __str__(self):

        return '%s' % (self.name)
#buy now
class buynow(models.Model):
    buyer_name=models.ForeignKey(User, on_delete=models.CASCADE)
    buyer_item = models.ForeignKey(data, on_delete=models.CASCADE)
    delieve=models.ForeignKey(Orderdetail, on_delete=models.CASCADE, default='')

    def __str__(self):
        return '%s' % (self.buyer_name)

#deliever
class deliever(models.Model):
    delieve=models.ForeignKey(Orderdetail, on_delete=models.CASCADE)

    Total_price = models.IntegerField()
    item = models.ManyToManyField(data)

    def __str__(self):
        return '%s' % (self.delieve)

