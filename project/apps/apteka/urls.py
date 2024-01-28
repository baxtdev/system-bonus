app_name = "main"   
from struct import pack
from django.urls import path

from . import views

    # login requred urls
urlpatterns = [
    path('', views.index, name='homepage'),
    # path("customerhtml", views.customerhtml, name="customerhtml"),
    path("cash_temp",views.cash_temp, name="cash_temp"),
    path('bonus_temp',views.bonus_temp,name='bonus_temp'),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("customer", views.find_customer, name="find_customer"),
    path("bonus_take", views.bonus_take, name="bonus_take"),
    path("add_cash", views.add_cash, name="add_cash"),
    path("register", views.add_user, name="register")
]
