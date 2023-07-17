from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register,name='register'),
    path('login/', views.login,name='login'),
    path('logout', views.logout,name='logout'),
    path('dashbord', views.dashbord,name='dashbord'),
    path('', views.dashbord,name='dashbord'),

    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),

    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword',views.resetpassword,name='resetpassword'),

    path('my_order/',views.my_order,name='my_order'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('order_detail/<int:order_id>/',views.order_detail,name='order_detail'),


]
