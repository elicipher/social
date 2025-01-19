from django.urls import path
from . views import RegisterView , LoginView , LogoutView , ProfileView

app_name = 'account'
urlpatterns =[
    
    path("register/" , RegisterView.as_view() , name= "user_register" ),
    path("login/" , LoginView.as_view() , name= "user_login" ),
    path("logout/" , LogoutView.as_view() , name= "user_logout" ),
    path("profile/<int:id_user>" , ProfileView.as_view() , name= "user_profile" ),

]