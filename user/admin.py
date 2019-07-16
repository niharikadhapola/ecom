from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(posts)
admin.site.register(data)
admin.site.register(cart)
admin.site.register(buynow)
admin.site.register(Orderdetail)
admin.site.register(deliever)

