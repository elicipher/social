from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from post.models import Post

# Create your views here.
class HomeView(View):
    
    def get(self , request):
        posts = Post.objects.all()
        return render(request , "home/index.html" , {'Posts' : posts})
    
    def post(self , request):
        return render(request , "home/index.html" ,)