from django import forms
from .models import Post ,Comment

class PostCreateUpdateForms(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption','photo',)
        
        widgets ={
            'caption' : forms.Textarea(attrs={'class':'form-control',"placeholder": "Say somethig ... "}),
            'photo' : forms.ClearableFileInput()

        }
    

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets ={
            'body': forms.Textarea(attrs={'class':'form-control'})
        } 

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class SearchForm(forms.Form):
    Search = forms.CharField()