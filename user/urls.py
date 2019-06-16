from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^post/$', views.post_list, name='post'),
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^success/$', views.success, name='success'),
    url(r'^show/$', views.show, name='show'),
    url(r'^cart/(?P<pk>\d+)$', views.add_cart, name='add_cart'),
    url(r'^show_cart/$', views.show_cart, name='show_cart'),
    url(r'^register/$', views.register, name='register'),
    url(r'^show_vendor_detail/$', views.show_vendor_detail, name='show_vendor_detail'),

    url(r'^vendor_register/$',views.vendor_register,name='vendor_register'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^$', views.index, name='index'),

    url(r'^feed/$', views.feed, name='feed'),

    url(r'^login/$', views.user_login, name='user_login'),

]

