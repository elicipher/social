from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class UserRegistrationForm(forms.Form):
    username = forms.CharField(required=False,widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "UserName"}))
    email = forms.EmailField(required=False,widget=forms.EmailInput(attrs={"class": "single-field","placeholder": "Email" }))
    password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={"class": "single-field","placeholder": "Password"}))
    confirm_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={"class": "single-field","placeholder": "ConfirmPassword"}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email = email).exists()
        if user :
            raise ValidationError("This email is already exists")
        return email
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username = username).exists()
        if user :
            raise ValidationError("This User is already exists")
        return username
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get("password")
        p2 = cd.get("confirm_password")
        if p1 and p2 and p1 != p2 :
            raise ValidationError("The password must be match")
    

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
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('age','bio',)