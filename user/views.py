# delivery address,product_id,

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from .forms import *
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import stripe
from django.views.generic.base import TemplateView
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request,template_name='user/home.html'):

    request.session['first'] = " hello niharika. This is session"
    item = data.objects.all()[1:5]
    next = data.objects.all()[6:10]
    # post_count = cart.objects.filter(name=request.user, status='int').count()
    list = {}
    if request.user.is_authenticated:
        post_count = cart.objects.filter(name=request.user, status='int')
        a=0

        list['a_count'] = post_count
        for post in list['a_count']:
            a = a + post.quantity
        print(a)
        list['count']=a

    list['item'] = item
    list['next'] = next
    # list['count']=post_count
    return render(request, template_name, list)


#checkout
class HomePageView(TemplateView):
    template_name = 'user/pay.html'

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY


        return context


def charge(request): # new
    post = cart.objects.filter(name=request.user, status='int')
    list = {}
    list['object_list'] = post
    a = 0
    for post in list['object_list']:
        a = a + post.item.price * post.quantity
    list['value'] = a*100
    post_count = 0


    if request.method == 'POST':
        charge = stripe.Charge.create(

            amount=a*100,
            currency='inr',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        post = cart.objects.filter(name=request.user, status='int')
        list = {}
        list['object_list'] = post
        myform = mydel(request.POST)
        tot=request.session.get("instat")
        pk=request.session.get("insta")
        print(request.session.get("instat"))
        print(request.session.get("insta"))
        instance = myform.save(commit=False)
        id = Orderdetail.objects.get(id=pk)
        instance.delieve = id
        instance.Total_price = a
        instance.save()
        for post in list['object_list']:
            instance.item.add(post.item)
            print(post.item)
        cart.objects.filter(name=request.user, status='int').delete()
        return render(request, 'user/charge.html',{'count':post_count})
    return render(request, 'user/pay.html',{'count':post_count})


class buy_HomePageView(TemplateView):
    template_name = 'user/buypay.html'

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

#buynow
def buy_charge(request): # new

    pk = request.session.get("pk")
    id = data.objects.get(id=pk)
    print(id.price)
    post_count = 0
    if request.method == 'POST':
        charge = stripe.Charge.create(

            amount=id.price*100,
            currency='inr',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        form = buyForm(request.POST)
       # name = request.session.get("name")
        address = request.session.get("address")

        instance = form.save(commit=False)
        addres = Orderdetail.objects.get(id=address)
        #buyer=User.objects.get(username=name)
        id = data.objects.get(id=pk)
        instance.buyer_name = request.user
        instance.buyer_item = id
        instance.delieve=addres
        instance.save()

        return render(request, 'user/buycharge.html',{'count':post_count})
    return render(request, 'user/buypay.html', {'count':post_count})


#feedback form
def feed(request, template_name='user/feedback.html'):
    form = PostsForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'ur feedback is sent')
        return render(request, 'user/feedback.html', {})
    else:
        form=PostsForm()

    return render(request, template_name, {'form': form})

#upload details of item by vendor
@login_required(login_url='user_login')
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
@login_required(login_url='user_login')
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
            user = user_form.save(commit=False)
            user.is_active = False
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)


            profile.user = user
            profile.category='user'
            profile.save()
            registered = True
            current_site = get_current_site(request)
            mail_subject = 'Activate your ecomwebsite account.'
            message = render_to_string('user/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Email has been sent, Please confirm your email address to complete the registration')

            return render(request, 'user/registration.html', {})
            # return HttpResponseRedirect(reverse('user_login'))

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'user/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
@login_required(login_url='user_login')
def list(request, template_name='user/my_list.html'):
    h=User.objects.get(username=request.user)

    host=User.objects.filter(username=request.user)
    posts = UserProfile.objects.filter(user_id=h)
    data = {}
    post_count = cart.objects.filter(name=request.user, status='int')
    a = 0

    data['a_count'] = post_count
    for value in data['a_count']:
        a = a + value.quantity
    print(a)
    data['count'] = a


    data['object_list'] = posts

    data['list'] = host
    return render(request, template_name, data)
#update user fistname
@login_required(login_url='user_login')
def update_User(request, pk, template_name='user/edituser.html'):
    host = get_object_or_404(User, pk=pk)
    data = {}
    post_count = cart.objects.filter(name=request.user, status='int')
    a = 0

    data['a_count'] = post_count
    for value in data['a_count']:
        a = a + value.quantity
    print(a)

    form =editForm(request.POST or None, instance=host)
    if form.is_valid():

        form.save()
        return redirect('list')
    return render(request, template_name, {'form': form,'count':a})
#update user address or extrafield
@login_required(login_url='user_login')
def post_update(request, pk, template_name='user/edit.html'):
    post = get_object_or_404(UserProfile, pk=pk)

    form =UserProfileInfoForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('list')
    return render(request, template_name, {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        messages.success(request, 'Thank you for your email confirmation. Now you have logged in to your account.')
        return render(request, 'user/index.html', {})

    else:
        return HttpResponse('Activation link is invalid!')

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
        try:
            x = User.objects.get(username=username)
            y = UserProfile.objects.get(user=x)
            user = authenticate(username=username, password=password,)
        except ObjectDoesNotExist:
            messages.success(request, 'user doesnot exsist')
            return render(request, 'user/login.html', {})


        if user:
            if user.is_active :
                if  y.category=='user':
                    login(request, user)
                elif y.category=='vendor':
                    login(request,user)
                    return HttpResponseRedirect(reverse('detail'))
                else:
                    messages.success(request, 'not valid.')
                    return render(request, 'user/login.html', {})

                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            messages.success(request, 'wrong password or userid')
            return render(request, 'user/login.html', {})
            #return HttpResponse("Invalid login details given")
    else:
        return render(request, 'user/login.html', {})



#show list of all feedback
@login_required(login_url='user_login')
def post_list(request, template_name='user/post_list.html'):
    post = posts.objects.all()
    data = {}
    data['object_list'] = post
    return render(request, template_name, data)

#show all uploaded items
def show(request, template_name='user/index.html'):
    print(request.session.get("first"))
    post = data.objects.all()
    list = {}
    if request.user.is_authenticated:
        post_count = cart.objects.filter(name=request.user, status='int')
        a = 0

        list['a_count'] = post_count
        for value in list['a_count']:
            a = a + value.quantity
        print(a)
        list['count'] = a

    list['object_list'] = post

    return render(request, template_name, list)
#show order list to vendor
def show_order(request, template_name='user/showorder.html'):

    post = deliever.objects.filter(item__vendor_name=request.user).distinct()
    list = {}
    list['object_list'] = post
    tost = buynow.objects.filter(buyer_item__vendor_name=request.user)
    list['object'] = tost

    return render(request, template_name, list)

#show individual item
@login_required(login_url='user_login')
def all(request, pk,template_name='user/all.html'):
    Product = data.objects.get(id=pk)
    list = {}
    a=0
    post_count = cart.objects.filter(name=request.user, status='int')
    list['a_count'] = post_count
    for value in list['a_count']:
        a = a + value.quantity

    return render(request, template_name, {'object': Product,'count':a})

#add items to cart
@login_required(login_url='user_login')
def add_cart(request, pk,template_name='user/cart.html'):
    try:
        post = cart.objects.get(item_id=pk ,name=request.user)
        post.quantity = post.quantity + 1
        post.save()
        return redirect('show_cart')

    except ObjectDoesNotExist:
        form = joinForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = request.user
            id = data.objects.get(id=pk)
            instance.item = id
            instance.save()

            messages.success(request, 'item is added to cart')
            return redirect('show_cart')
        return render(request, template_name, {'form': form})


        #cart.objects.get(item=id,name=request.user)
        #instance.save()




#buy now to address
@login_required(login_url='user_login')
def buyordered(request,pk, template_name='user/buyorder.html'):
    form = order(request.POST or None)
    request.session['pk'] = pk
    Product = Orderdetail.objects.filter(buyername=request.user.username)

    if form.is_valid():
        instance=form.save(commit=False)
        instance.buyername =request.user
        instance.save()

        return redirect('buyordered')
    return render(request, template_name, {'form': form,'object':Product})

#buy now
def buy_now(request, pk,template_name='user/buy.html'):


    form = buyForm(request.POST )

    if form.is_valid():
        instance=form.save(commit=False)
        instance.buyer_name=request.user
        request.session['address'] = pk
        request.session['name'] = request.user.username

        return redirect('buy_home')
        #cart.objects.get(item=id,name=request.user)
        #instance.save()


    return render(request, template_name,{'form':form})


#show items to cart as per the user, who added it to cart
@login_required(login_url='user_login')
def show_cart(request, template_name='user/list.html'):

    post = cart.objects.filter(name=request.user,status='int')

    list = {}
    post_count = cart.objects.filter(name=request.user, status='int')
    a = 0

    list['a_count'] = post_count
    for value in list['a_count']:
        a = a + value.quantity
    list['count'] = a

    list['object_list'] = post
    a=0

    for post in list['object_list']:
        a=a+post.item.price*post.quantity
        print(post.id)
    print(a)
    list['total']=a
    return render(request, template_name, list)

#increse 1
def update_cart(request, pk):
    #host = get_object_or_404(cart, pk=pk)
    post=cart.objects.get(id=pk)
    post.quantity=post.quantity+1
    post.save()

    return redirect('show_cart')
#decrease 1
def decrease_cart(request, pk):
    #host = get_object_or_404(cart, pk=pk)
    post=cart.objects.get(id=pk)
    if post.quantity==1:
        post.delete()
    else:
        post.quantity=post.quantity-1
        post.save()

    return redirect('show_cart')

#delete cart
def delete_cart(request, pk, template_name='user/delete.html'):
    post = get_object_or_404(cart, pk=pk)
    if request.method=='POST':
        post.delete()
        return redirect('show_cart')
    return render(request, template_name, {'object': post})

#save address and show address

def ordered(request, template_name='user/order.html'):
    form = order(request.POST or None)
    Product = Orderdetail.objects.filter(buyername=request.user.username)
    post_count = cart.objects.filter(name=request.user, status='int')
    a = 0
    list={}
    list['a_count'] = post_count
    for value in list['a_count']:
        a = a + value.quantity



    request.session['count'] =  a
    if form.is_valid():
        instance=form.save(commit=False)
        instance.buyername =request.user

        instance.save()

        return redirect('order')
    return render(request, template_name, {'form': form,'object':Product,'count':a})

#delete address
def delete_address(request, pk, template_name='user/delete.html'):
    post = get_object_or_404(Orderdetail, pk=pk)
    if request.method=='POST':
        post.delete()
        return redirect('order')
    return render(request, template_name, {'object': post})


#deliver to this address
def place(request,pk, template_name='user/place.html'):
    myform = mydel(request.POST)
    post = cart.objects.filter(name=request.user, status='int')
    list = {}
    list['object_list'] = post


    a = 0
    b = 0
    for post in list['object_list']:
        a = a + post.item.price
    print(a)

    if myform.is_valid():
        instance = myform.save(commit=False)

        request.session['insta'] =pk
        request.session['instat'] =a

        return redirect('home')

    return render(request, template_name, {'myform': myform})


