from django.contrib import admin
from .models import Post , Comment , Like
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('user','slug' , 'updated',)
    search_fields = ('slug','caption')
    list_filter = ('user',)
    prepopulated_fields = {'slug' :('caption',)}
    raw_id_fields = ('user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post' , 'created' , 'is_reply' ,)
    raw_id_fields = ('user','post', 'reply',)
admin.site.register(Like)