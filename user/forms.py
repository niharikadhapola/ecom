from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile,posts,data,cart
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())


    class Meta():
        model = User
        fields = ('username','first_name','last_name', 'password', 'email')



    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )





class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('address',)



class PostsForm(forms.ModelForm):

    class Meta:
        model = posts
        fields = ['name','phone','describe']

class info(forms.ModelForm):

    class Meta:
        model = data
        fields = ['name','price','img']

class joinForm(forms.ModelForm):
    class Meta:
        model = cart
        exclude = ('name','item')