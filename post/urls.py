from django.urls import path 
from .views import PostDetailView , PostDeleteView , PostUpdateView , PostCreateView
app_name = 'post'
urlpatterns = [
    path('details/<int:post_id>/<slug:post_slug>/' , PostDetailView.as_view(),name="post_detail"),
    path('delete/<int:post_id>' , PostDeleteView.as_view(),name="post_delete"),
    path('update/<int:post_id>' , PostUpdateView.as_view(),name="post_update"),
    path('create/' , PostCreateView.as_view(),name="post_create"),
]