from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from .models import Post
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateUpdateForms
from django.utils.text import slugify

# Create your views here.
class PostDetailView(View):
    
    def get(self , request , post_id , post_slug):
        post = get_object_or_404(Post , pk = post_id , slug = post_slug)
        return render(request , 'post/details.html' , {"post" : post})


class PostDeleteView(LoginRequiredMixin,View):

    def get(self , request , post_id):
        post = get_object_or_404(Post , pk = post_id)
        if post.user.id == request.user.id :
            post.delete()
            messages.success(request ,"Post deleted successfuly !" , 'success')
        else :
            messages.error(request , 'you can\'t delete this post ' , 'danger')
        return redirect('home:home')

class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForms
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post , pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id :
            messages.error(request , "You can\' update this post" , 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self , request , post_id):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request , 'post/update.html' , {'form' : form })

    def post(self , request , post_id):
        post = self.post_instance
        form = self.form_class(request.POST , instance=post)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['caption'][:20])
            new_post.save()
            messages.success(request , 'Updated successfuly' , 'success')
            return redirect('post:post_detail' , post.id , post.slug)
        
class PostCreateView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForms
    def get(self , request , *args , **kwargs ):
        form = self.form_class
        return render(request , 'post/create.html' , {'form' : form})

    def post(self ,request , *args , **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post =form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['caption'][:20])
            new_post.user = request.user
            new_post.save()
            messages.success(request ,'created post successfully' , 'success')
            return redirect('account:user_profile' , request.user.id)
