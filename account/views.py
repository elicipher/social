from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from .forms import UserRegistrationForm , UserLoginForm , EditUserForm
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import Post 
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation , Profile
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

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

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
                if self.next :
                    return redirect(self.next)
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
        is_following = False
        user = get_object_or_404(User ,pk = id_user)
        #posts = Post.objects.filter(user=user)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user = request.user , to_user=user)
        if relation.exists():
            is_following = True
        return render(request , 'account/profile.html' , {'user':user , 'posts': posts , 'is_following':is_following})
    
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

class FollowUserView(LoginRequiredMixin , View):

    def get(self , request , id_user):
        #اون کاربری که میخواییم فالو بکنیم رو میریزیم تو متغیر یوزر 
        user = User.objects.get(id = id_user)
        relate = Relation.objects.filter(from_user = request.user , to_user=user)
        #بررسی وجود رابطه 
        if relate.exists():
            messages.error(request , 'you already following this user' , 'danger')
        else:
         
            Relation(from_user = request.user , to_user=user).save()
            messages.success(request , 'you are following this user' , 'success')
        return redirect('account:user_profile' , user.id)
    
class UnFollowUserView(LoginRequiredMixin , View):

    def get(self , request , id_user):
        user = User.objects.get(id = id_user)
        relate = Relation.objects.filter(from_user = request.user , to_user=user)
        if relate.exists():
            relate.delete()
            messages.success(request , 'your unfollowed user successfuly' , 'success')
        else :
            messages.error(request , 'your not following this user ' , 'danger')
        return redirect('account:user_profile' , user.id)

class EditUserView(LoginRequiredMixin,View):
    form_class = EditUserForm
    def get(self , request):
        form = self.form_class(instance=request.user.profile , initial={'email':request.user.email})
        return render(request , "account/edit_profile.html" , {"form":form})

    def post(self , request):
        form = self.form_class(request.POST , instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request , "Profile changed successfuly " , 'success')
        return redirect("account:user_profile" , request.user.id)
