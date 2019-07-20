from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

#django user form
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
class editForm(forms.ModelForm):
    class Meta():
            model = User
            fields = ('first_name', )



#extra field of django user form
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('address',)


#feedback form
class PostsForm(forms.ModelForm):

    class Meta:
        model = posts
        fields = ['name','phone','describe']

#product detail
class info(forms.ModelForm):

    class Meta:
        model = data
        fields = ['name','price','img']

#add to cart
class joinForm(forms.ModelForm):
    class Meta:
        model = cart
        exclude = ('name','item','status','quantity')


#buy now
class buyForm(forms.ModelForm):
    class Meta:
        model = buynow
        exclude = ('buyer_name','buyer_item','delieve')
#delievery
class mydel(forms.ModelForm):
    class Meta:
        model = deliever
        exclude = ('delieve','Total_price','item')
#order detail
class order(forms.ModelForm):
    class Meta:
        model = Orderdetail
        fields = ('name','address','state','phone')