from django.contrib import admin

# Register your models here.
from .models import UserProfile, posts,data,cart

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(posts)
admin.site.register(data)
admin.site.register(cart)
