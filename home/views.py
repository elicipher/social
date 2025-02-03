from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from post.models import Post
from post.forms import SearchForm
# Create your views here.
class HomeView(View):
    form_class = SearchForm
    def get(self , request):
        posts = Post.objects.all()
        if request.GET.get('Search'):
            posts = posts.filter(caption__contains = request.GET["Search"])
        return render(request , "home/index.html" , {'Posts' : posts , 'Search' : self.form_class})
    
    def post(self , request):
        return render(request , "home/index.html" ,)