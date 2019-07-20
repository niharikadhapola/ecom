from django.conf.urls import url
from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    url(r'^post/$', views.post_list, name='post'),
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^success/$', views.success, name='success'),
    url(r'^show/$', views.show, name='show'),
    url(r'^cart/(?P<pk>\d+)$', views.add_cart, name='add_cart'),
    path('', views.HomePageView.as_view(), name='home'),
    path('buy', views.buy_HomePageView.as_view(), name='buy_home'),
    url(r'^buy_charge/$', views.buy_charge, name='buy_charge'),

    url(r'^buyordered/(?P<pk>\d+)$', views.buyordered, name='buyorder'),
    url(r'^buy/(?P<pk>\d+)$', views.buy_now, name='buy_now'),
    url(r'^delete/(?P<pk>\d+)$', views.delete_cart, name='delete_cart'),
    url(r'^delete_address/(?P<pk>\d+)$', views.delete_address, name='delete_address'),
    url(r'^all/(?P<pk>\d+)$', views.all, name='all'),
    url(r'^update_cart/(?P<pk>\d+)$', views.update_cart, name='update_cart'),
url(r'^decrease_cart/(?P<pk>\d+)$', views.decrease_cart, name='decrease_cart'),
    url(r'^charge/$', views.charge, name='charge'),
    url(r'^show_cart/$', views.show_cart, name='show_cart'),
url(r'^show_order/$', views.show_order, name='show_order'),
    url(r'^register/$', views.register, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^order/$', views.ordered, name='order'),
    url(r'^place/(?P<pk>\d+)$', views.place, name='place'),

    url(r'^h$', views.list, name='list'),
    url(r'^edituser/(?P<pk>\d+)$', views.update_User, name='update_User'),
    url(r'^edit/(?P<pk>\d+)$', views.post_update, name='post_edit'),

    url(r'^show_vendor_detail/$', views.show_vendor_detail, name='show_vendor_detail'),
    url(r'^vendor_register/$',views.vendor_register,name='vendor_register'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^home/$', views.index, name='index'),
    url(r'^feed/$', views.feed, name='feed'),
    url(r'^login/$', views.user_login, name='user_login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    re_path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = 'user/login.html'), name='password_reset_complete'),
]

