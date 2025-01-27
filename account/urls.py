from django.urls import path
from . views import RegisterView , LoginView , LogoutView , ProfileView , PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView,FollowUserView,UnFollowUserView
app_name = 'account'
urlpatterns =[
    
    path("register/" , RegisterView.as_view() , name= "user_register" ),
    path("login/" , LoginView.as_view() , name= "user_login" ),
    path("logout/" , LogoutView.as_view() , name= "user_logout" ),
    path("profile/<int:id_user>" , ProfileView.as_view() , name= "user_profile" ),
    path("reset/" , PasswordResetView.as_view() , name= "reset_password" ),
    path("reset/done/" , PasswordResetDoneView.as_view() , name= "password_reset_done" ),
    path("confirm/<uidb64>/<token>" , PasswordResetConfirmView.as_view() , name= "password_reset_confirm" ),
    path("compelet/" , PasswordResetCompleteView.as_view() , name= "password_reset_compelet" ),
    path('follow/<int:id_user>',FollowUserView.as_view(), name='user_follow'),
    path('unfollow/<int:id_user>',UnFollowUserView.as_view(), name='user_unfollow'),
]