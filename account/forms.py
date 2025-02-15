from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError 
from .models import Profile

class UserRegistrationForm(forms.Form):
    username = forms.CharField(required=False,widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "UserName"}))
    email = forms.EmailField(required=False,widget=forms.EmailInput(attrs={"class": "single-field","placeholder": "Email" }))
    password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={"class": "single-field","placeholder": "Password"}))
    confirmpassword = forms.CharField(required=False,widget=forms.PasswordInput(attrs={"class": "single-field","placeholder": "ConfirmPassword"}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email = email).exists()
        if user :
            raise ValidationError("This email is already exists")
        elif not email :
            raise ValidationError("The email is empty")
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username = username).exists()
        if user :
            raise ValidationError("This User is already exists")
        elif not username :
             raise ValidationError("The username is empty")

        return username
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('confirmpassword')
        if not p1:
            self.add_error('password', "The password is empty")
        if not p2:
            self.add_error('confirmpassword', "The confirmation password is empty")
        if p1 and p2 and p1 != p2:
            self.add_error('confirmpassword', "The passwords must match")
    
    

class UserLoginForm(forms.Form):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "single-field",
            "placeholder": "Username or Email"
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "single-field",
            "placeholder": "Password",

        })
    )

class EditUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150 , widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style' : 'width : 300px; color : black;'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style' : 'width : 300px; height: 50px; color : black;'}))
   
    class Meta:
        model = Profile
        fields = ('img_user','age','bio','banner',)
        widgets={
            'profile' : forms.ImageField(required=False),
            'bio' : forms.Textarea(attrs={'class': 'form-control','style': 'color : black;'})
        }

        
       
    

