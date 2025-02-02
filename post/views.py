from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from .models import Post , Comment , Like
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateUpdateForms , CommentCreateForm , CommentReplyForm 
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Create your views here.
class PostDetailView(View):
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post , pk=kwargs['post_id'] , slug =kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    
    form_class_reply = CommentReplyForm
    form_class = CommentCreateForm
    
    def get(self , request , *args , **kwargs):
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        Comments = self.post_instance.pcomments.filter(is_reply = False)
        return render(request , 'post/details.html' , {"post" : self.post_instance , 'form':self.form_class , 'Comments':Comments , 'form_reply':self.form_class_reply , 'can_like':can_like} )
    
    @method_decorator(login_required)
    def post(self , request , *args , **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            New_comment = form.save(commit=False)
            New_comment.user = request.user
            New_comment.post = self.post_instance
            New_comment.save()
            messages.success(request , "your comment submited successfuly !",'success')
            return redirect('post:post_detail',self.post_instance.id , self.post_instance.slug)

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

class ReplyCommentView(View):
    form_class = CommentReplyForm
    def post(self , request , post_id , comment_id):
           post = get_object_or_404(Post , id = post_id)
           comment = get_object_or_404(Comment , id = comment_id)
           form = self.form_class(request.POST)
           if form.is_valid():
            New_reply = form.save(commit=False)
            New_reply.user = request.user
            New_reply.post = post
            New_reply.reply = comment
            New_reply.is_reply = True
            New_reply.save()
            messages.success(request , "Reply sended successfuly " , "success")
            return redirect("post:post_detail" , post.id , post.slug)


class LikePostView(LoginRequiredMixin , View):
    def get(self , request , post_id):
        post = get_object_or_404(Post , id = post_id)
        like = Like.objects.filter(post = post , user = request.user)
        if like.exists():
            messages.error(request , "You already liked this post !" , "danger")
        else :
            Like.objects.create(post=post , user = request.user)
            messages.success(request , "You liked post successfuly !" , "success")

        return redirect('post:post_detail' , post.id , post.slug)

    