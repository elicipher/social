from django.urls import path 
from .views import PostDetailView
app_name = 'post'
urlpatterns = [
    path('details/<int:post_id>/<slug:post_slug>/' , PostDetailView.as_view(),name="post_detail")
]