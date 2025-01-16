from django.urls import path
from . views import RegisterView , LoginView

app_name = 'account'
urlpatterns =[
    
    path("register/" , RegisterView.as_view() , name= "user_register" ),
    path("login/" , LoginView.as_view() , name= "user_login" ),

]