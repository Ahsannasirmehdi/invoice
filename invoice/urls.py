from django.shortcuts import redirect
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('base/', views.base, name='base'),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('mainpage/', views.adin, name='adin'),
    path('profile/', views.addata, name='addata'),
    path('schedule/', views.schedule, name='schedule'),


    path('logout_view', views.logout_view,name='logout_view'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('view_invoice/', views.view_invoice, name='view_invoice'),
    path('registerusers/', views.registerusers, name='registerusers'),
    path('delete_invoice/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('delete_all_invoice/', views.delete_all_invoice,name='delete_all_invoice'),
    path('template/', views.template,name='template'),
    path('subscribe/', views.sub, name='sub'),
    path('checkpdf/<int:pk>', views.checkpdf, name='checkpdf'),
    path('signin/', views.sign, name='sign'),
    path('purchasesignin/', views.sign1, name='sign1'),
    path('signup/', views.signup, name='signup'),
    # path('subscribe/invoice/charge/', views.charge, name='charge'),
    path('charge/', views.charge, name='charge'),
    path('edit_invoice/<int:pk>/',views.edit_invoice, name='edit_invoice'),
    path('complete/', views.resetpasswordcomplete , name='ResetPasswordcomplete'),
    path('password-reset/', views.resetpasswordview , name='password_reset'),


]
