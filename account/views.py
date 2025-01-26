from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from .forms import UserRegistrationForm , UserLoginForm
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
# Create your views here.
class RegisterView(View):

    def dispatch(self, request, *args, **kwargs):
        if  request.user.is_authenticated :
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    

    form_class = UserRegistrationForm
    template_name = "account/register.html"

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name , {"form" : form})
    
    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"] , cd["email"], cd["password"])
            messages.success(request , "You login successfully " , "success")
            return redirect('home:home')
        return render(request ,self.template_name , {"form" : form})
    
class LoginView(View):

    def dispatch(self, request, *args, **kwargs):
        if  request.user.is_authenticated :
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    form_class = UserLoginForm
    template_name = "account/login.html"

    def get(self , request):
        form = self.form_class()
        return render(request ,self.template_name , {"form":form})

    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request , username = cd["username"] , password = cd["password"])
            if user is not None :
                login(request , user)
                messages.success(request , "You reqistered successfully " , "success")
                return redirect('home:home')
                
            incorrect_password = True
            messages.error(request , "Your password or username is wrong !", 'danger' )
            return render(request ,self.template_name , {"form":form , 'incorrect_password' : incorrect_password})

class LogoutView(LoginRequiredMixin ,View):

    def get(self,request):
        logout(request)
        messages.success(request , "You logout successfuly " , "success")
        return redirect('home:home')

class ProfileView(LoginRequiredMixin ,View):

    def get(self,request ,id_user):
        user = get_object_or_404(User ,pk = id_user)
        posts = Post.objects.filter(user=user)
        return render(request , 'account/profile.html' , {'user':user , 'posts': posts})
    
class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/reset_password_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_compelet')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_compelet.html'