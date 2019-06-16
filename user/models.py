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

class cart(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(data, on_delete=models.CASCADE)



    def __str__(self):
        return '%s' % (self.name)