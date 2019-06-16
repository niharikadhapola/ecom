from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from .forms import UserForm,UserProfileInfoForm,PostsForm,info,joinForm
from django.contrib.auth.models import User
from .models import UserProfile,posts,data,cart
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

#render home.html
def index(request):
    return render(request,'user/home.html')


#feedback form
def feed(request, template_name='user/feedback.html'):
    form = PostsForm(request.POST or None)
    if form.is_valid():

        return HttpResponse("posted")
    return render(request, template_name, {'form': form})

#upload details of item by vendor
def detail(request, template_name='user/website.html'):
    if request.method == 'POST':
        form = info(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.vendor_name = request.user
            instance.save()
            messages.success(request,'uploaded successfully')
            return redirect('show_vendor_detail')
    else:
        form = info()
    return render(request, template_name, {'form': form})

#show vendor details as per requested vendor
def show_vendor_detail(request, template_name='user/show_vendor_detail.html'):
    post = data.objects.filter(vendor_name=request.user)
    list = {}
    list['object_list'] = post
    return render(request, template_name, list)

def success(request):
    return HttpResponse('successfuly uploaded')

def special(request):
    return HttpResponse("You are logged in !")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.category='user'
            profile.save()
            registered = True
            return HttpResponseRedirect(reverse('user_login'))

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'user/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def vendor_register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.category='vendor'
            profile.save()
            registered = True
            return HttpResponseRedirect(reverse('user_login'))

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'user/vendor_registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        x = User.objects.get(username=username)
        y = UserProfile.objects.get(user=x)


        user = authenticate(username=username, password=password,)

        if user:
            if user.is_active :
                if  y.category=='user':
                    login(request, user)
                elif y.category=='vendor':
                    login(request,user)
                    return HttpResponseRedirect(reverse('detail'))
                else:
                    return HttpResponse("not valid.")

                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'user/login.html', {})



#show list of all feedback
def post_list(request, template_name='user/post_list.html'):
    post = posts.objects.all()
    data = {}
    data['object_list'] = post
    return render(request, template_name, data)

#show all uploaded items
def show(request, template_name='user/index.html'):
    post = data.objects.all()
    list = {}
    list['object_list'] = post
    return render(request, template_name, list)

#add items to cart
def add_cart(request, pk,template_name='user/cart.html'):

    form = joinForm(request.POST )

    if form.is_valid():
        instance=form.save(commit=False)
        instance.name=request.user
        id = data.objects.get(id=pk)
        instance.item=id
        instance.save()
        return HttpResponse("added")
        #cart.objects.get(item=id,name=request.user)
        #instance.save()

    return render(request, template_name,{'form':form})

#show items to cart as per the user, who added it to cart
def show_cart(request, template_name='user/list.html'):
    post = cart.objects.filter(name=request.user)
    list = {}
    list['object_list'] = post
    return render(request, template_name, list)

# Create your views here.

