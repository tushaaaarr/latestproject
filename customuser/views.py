from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth import authenticate, login
from customuser.models import user_type, User
from django.shortcuts import render,HttpResponse ,redirect
from django.views import generic
from django.contrib import messages 
from geopy.geocoders import Nominatim
from datetime import datetime
from playsound import playsound
import math, random
import time
# from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
from .models import Orders, PersonalDetails, Shop,Image,Prescription,GetDeliveries,Cities
from .models import StoreBill,Profile
# from geopy.geocoders import Nominatim
from math import e, remainder, sin, cos, radians, degrees, acos
import math
from django.http import HttpResponseBadRequest
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from newproject.settings import RAZORPAY_API_KEY
from newproject.settings import RAZORPAY_API_SECRET_KEY
import razorpay
from django.contrib.sites.shortcuts import get_current_site
import razorpay
import os
from twilio.rest import Client
from pytonik_time_ago.timeago import timeago

# import datetime
def home(request): 
    context = {}
    if request.user.is_authenticated and user_type.objects.filter(user=request.user).exists():
        if user_type.objects.get(user=request.user).is_delivery == True:
           return redirect('/app-view/get-delivery-requests')
        elif user_type.objects.get(user=request.user).is_store == True:
            return redirect('/store-notifications')
        else:
            return render(request,'user/home/index.html',context)
    else:
        return render(request,'user/home/index.html',context)

def Appview(request):
    if request.user.is_authenticated and user_type.objects.filter(user=request.user).exists():
        if user_type.objects.get(user=request.user).is_delivery == True:
            return redirect('/app-view/get-delivery-requests')
        elif user_type.objects.get(user=request.user).is_store == True:
            return redirect('/app-view/store-notifications')
        else:
            return render(request,'app-view/user/home/index.html')
    else:
        return render(request,'app-view/user/home/index.html')

def is_appview(myurl):
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        return True
    except:          
        return False

def send_otp(mobile, otp):
    account_sid = "AC8c55da658680546cd2f069c440eb8629"
    auth_token = "ec07b7a628608ff0ce668cdafcb54024"
    client = Client(account_sid, auth_token)
    body = f"Thanks for connecting with us. Your Login OTP is: {otp}"
    # message = client.messages \
    #                 .create(
    #                      body=f"Thanks for connecting with us. Your Login OTP is: {otp}",
    #                      from_='+16513749253',
    #                      to=f'+91{mobile}')
    return None

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        username=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        mobile=request.POST['mobile']
        check_user = User.objects.filter(email = email).first()
        check_profile = Profile.objects.filter(mobile = mobile).first()
        
        if check_user or check_profile:
            context = {'message' : 'User already exists' , 'class' : 'danger' }
            return render(request,'accounts/register.html' , context)

        user = User.objects.create_user(email = email)
        user.first_name= fname
        user.last_name= lname
        user.mobile = mobile
        user.save()
        new_user = PersonalDetails(fname=fname,lname=lname,username=email,email=email,mob=mobile,lat=0,lon=0)
        new_user.save()
        current_user=User.objects.get(email=username)
        user_type(user=current_user,is_user = True).save()
        otp = str(random.randint(1000 , 9999))
        profile = Profile(user = email , mobile=mobile , otp = otp) 
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request,'accounts/register.html')

def otp(request):
    context = {}
    if request.method == 'POST':
        mobile = request.session['mobile']
        context = {'mobile':mobile}
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        if otp == profile.otp:
            user = User.objects.get(email = profile.user)
            login(request , user)
            myuser = User.objects.get(email = profile.user)
            if user_type.objects.get(user=myuser).is_store==True:
                return redirect('/store-notifications')
            else:
                return redirect('/')   
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'accounts/reg_otp.html' , context)
    return render(request,'accounts/reg_otp.html' , context)

url_list1 = []
def login_attempt(request):
    if request.GET.get('next') != None:
        next_url = request.GET.get('next')
    else:
        if is_appview(request.path) == True:
            next_url = '/app-view/home'
        else:
            next_url = '/'

    url_list1.append(next_url)
    if len(url_list1) > 10:
        url_list1.pop(0)
    
    if request.method == 'POST':
        mobile = request.POST.get('mobile')  
        user = Profile.objects.filter(mobile = mobile).first()
        if user is None:
            context = {'message' : 'User not found' , 'class' : 'danger' }
            return render(request,'accounts/login.html' , context)
        otp = str(random.randint(1000 , 9999))
        user.otp = otp
        user.save()
        send_otp(mobile , otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')      
    return render(request,'accounts/login.html')

def login_otp(request):
    last_url = url_list1[-1]
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        if otp == profile.otp:
            user = User.objects.get(email = profile.user)
            login(request , user)
            return redirect(last_url)
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile}
            return render(request,'accounts//login_otp.html' , context)
    return render(request,'accounts/login_otp.html' , context)

# Common-Data Sharing
def common(request):
    context = {}
    context['notification_url'] = '/'    
    if request.user.is_authenticated and user_type.objects.exists():
        username = request.user
        try:
            context['prof_fname'] = PersonalDetails.objects.filter(username=str(username))[0].fname
            context['prof_lname'] = PersonalDetails.objects.filter(username=str(username))[0].lname
        except:
            pass
    if request.user.is_authenticated and user_type.objects.filter(user=request.user).exists():
        if user_type.objects.get(user=request.user).is_delivery==True:
            context['noti_len'] = Orders.objects.filter(deliver_status = False).count()
            context['app_user_type'] = 'deliver'
            context['user'] = request.user
            myname = PersonalDetails.objects.filter(username = request.user)
            context['fname'] = myname[0].fname
            context['lname'] = myname[0].lname
            context['usermail'] = str(request.user)
            context['name'] = str(context['fname']) + str(' ') + str(context['lname'])

    if request.user.is_authenticated and user_type.objects.filter(user=request.user).exists():
        if request.user.is_authenticated and user_type.objects.get(user=request.user).is_user==True:
            context['notification_url'] = 'users-notifications'
            context['noti_len'] = Orders.objects.filter(order_completed = False).filter(c_username=str(request.user)).count()
            context['app_user_type'] = 'customer'
            myname = PersonalDetails.objects.filter(username = request.user)
            context['fname'] = myname[0].fname
            context['lname'] = myname[0].lname
            context['usermail'] = str(request.user)
            context['name'] = str(context['fname']) + str(' ') + str(context['lname'])
            if request.POST.get('input_city_name'):
                context['current_city'] = request.POST.get('input_city_name')
            else:
                current_user = PersonalDetails.objects.filter(username= request.user)
                context['current_city'] = str(current_user[0].city)
        else:
            if request.POST.get('input_city_name'):
                current_city = request.POST.get('input_city_name')
            else:
                current_city = "Search Location"

    if request.user.is_authenticated and user_type.objects.filter(user=request.user).exists():
        if request.user.is_authenticated and user_type.objects.get(user=request.user).is_store==True:
            context['notification_url'] = 'store-notifications'
            context['noti_len'] = Orders.objects.filter(order_accept_status = 'not_responded').count()
            context['usermail'] = str(request.user)
            context['app_user_type'] = 'store_owner'
    return {'context':context}
          
url_list = [] 
def handeLogin(request):
    next_url = request.GET.get('next')
    url_list.append(next_url)
    if len(url_list) > 10:
        url_list.pop(0)
    last_url = url_list[-1]
    if request.method=="POST":   
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            return redirect(last_url)
        else:
            messages.error(request, "Invalid credentials! Please try again")

    return render(request,'user/home/sign-in.html')
    return HttpResponse("login")

def handelLogout(request):
    print(request.path)
    logout(request)
    if is_appview(request.path) == True:
        return redirect('/app-view/home/login')
    else:
        return redirect('/login')
   
@login_required(redirect_field_name='next',login_url = '/login')
def UsersNotificationDetails(request,current_user,myid):
    UsersNotifications1 = Orders.objects.filter(id=myid)
    UsersNotifications = [] 
    context = {}
    for i in UsersNotifications1:
        # Time Ago 
        time = i.date.strftime('%H:%M:%S')
        date = i.date.date()
        mixed = str(date) + str(time)
        time_ago = timeago(f"{str(date)} {str(time)}").ago
        i.date = time_ago
        UsersNotifications.append(i)
    UsersNotifications =UsersNotifications[0]  

    if UsersNotifications.order_accept_status == 'accepted':
        context['message_2'] = 'Thanks for ordering.. Your delivery request has been accepted go to payment details ..'
    elif UsersNotifications.order_accept_status == 'rejected':
        context['message_2'] = 'Your delivery request has been rejected..'
        context['rejection_reason'] = UsersNotifications.rejection_reason
    else:
        context['message_2'] = ''
    if UsersNotifications.images_id != " ":
        context['message_1'] = 'Your Prescription has been uploaded Successfully.'
    else:
        context['message_1'] = 'Your Medicines has been uploaded Successfully.'

    bill_image_store = []
    if StoreBill.objects.filter(order_id=myid).exists():
        bill_image_store1 =StoreBill.objects.filter(order_id=myid)
        for j in bill_image_store1:
            j.date =  j.date.strftime('%H:%M:%S')
            bill_image_store.append(j)
        bill_image_store =bill_image_store[-1]
    
    params = {'UsersNotifications':UsersNotifications,
    'bill_image_store':bill_image_store,
    'myid':myid,
    'context':context,
    }       
    if is_appview(request.path) == True:
        url_path = 'app-view/user/home/notification-view.html'
    else:
        url_path = 'user/home/notification-view.html'
    return render(request,url_path,params)

@login_required(redirect_field_name='next',login_url = '/login')
def AppMyProfile(request):
    type_obj = user_type.objects.get(user=request.user)
    context = {}
    # Logged as a Store 
    if type_obj.is_store==True: 
        if request.method == 'POST':
            store_image = request.FILES.get('inputstoremage')
            store_name = request.POST.get('medical_name')
            address = request.POST.get('address')
            city = request.POST.get('city')
            mobile = request.POST.get('mobile')
            Shop.objects.filter(store_user = str(request.user)
            ).update(name = store_name,mobile= mobile,city = city,address = address,
            storephoto = store_image )
            return redirect(f'/app-view/user/profile')

        user = request.user
        myname = Shop.objects.filter(store_user = user)
        address = myname[0].address
        city = myname[0].city
        usermail = str(request.user)
        name = myname[0].name
        mobile = myname[0].mobile
        store_image = myname[0].storephoto
        context = {'name':name,'usermail':usermail,'city':city,'address':address,
        'mobile':mobile,'store_image':store_image,
        }
        templates = 'app-view/store/home/profile.html'

    elif type_obj.is_delivery==True:  
        templates = 'app-view/deliver/home/profile.html' 
    else:
        if request.method == 'POST':
            fname = request.POST.get('store_image')
            lname = request.POST.get('lname')
            address = request.POST.get('address')
            city = request.POST.get('city')
            mobile = request.POST.get('mobile')
            PersonalDetails.objects.filter(username = str(request.user)).update(fname = fname,lname =lname,
            mob= mobile,city = city,address = address)
            return redirect(f'/app-view/user/profile')
                 
        templates = 'app-view/user/home/profile.html' 
        user = request.user
        myname = PersonalDetails.objects.filter(username = user)
        address = myname[0].address
        city = myname[0].city
        fname = myname[0].fname
        lname = myname[0].lname
        usermail = str(request.user)
        name = str(fname) + str(' ') + str(lname)
        mobile = myname[0].mob
        context = {'name':name,'usermail':usermail,'city':city,'fname':fname,'lname':lname,'address':address,
        'mobile':mobile,
        }
    return render(request,templates,context)


def GenerateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP
     
@login_required(redirect_field_name='next',login_url = '/login')
def AddYourChemist(request):
    if request.method == 'POST':
        select_city = request.POST.get('select_city')
        storeowner = request.POST.get('storeowner')
        storename = request.POST.get('storename')
        storeaddress = request.POST.get('storeaddress')
        storemobile = request.POST.get('storemobile')
        storelicence = request.FILES.get("storelicence")
        storeadhar = request.FILES.get("storeadhar")
        storepan = request.FILES.get("storepan")
        storephoto = request.FILES.get("storephoto")
        Shop(name = storename,store_user=str(request.user),city=select_city,
            mobile=storemobile,address=storeaddress,pay_phone=storemobile,storelicence=storelicence,
            storeadhar=storeadhar,storepan=storepan,storephoto=storephoto).save()
        messages.success(request,'Thanks for joined with us.we will inform you very soon.')

        myurl = request.path
        obj = myurl.split('/')
        try:
            obj.index('app-view') 
            return redirect('/app-view/home')
        except:          
            return redirect('/')
    
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        url_path = 'app-view/user/home/add-chemist.html'
    except:          
        url_path = 'user/home/add-chemist.html'
    return render(request,url_path)

# from . import utility
# class Utility(object):
#     def __init__(self,client = None):
#         self.client = client
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
razorpay_client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))

@login_required(redirect_field_name='next',login_url = '/login')
def Payment(request): 
    order_amount = 30000
    order_currency = "INR"
    payment_order = client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture =1))
    order_id = payment_order['id']
    Ob = Orders.objects.filter(id=71)[0]

    context = {'api_key':RAZORPAY_API_KEY,'order_id':order_id,'customer_name':'Tushar Patil',
    'customer_mobile':9148035748,'customer_email':'tusharspatil@gmail.com'}
    return render(request,'shops/payment.html',context)

@login_required(redirect_field_name='next',login_url = '/login')
def payment(request):
    final_price = 20000  
    amount = final_price
    currency = 'INR'
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZORPAY_API_KEY
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    Orders.objects.filter(id=71).update(razorpay_order_id  = razorpay_order['id'])
    return render(request, 'shops/payment/paymentsummaryrazorpay.html',context=context)

def PaymentSuccess(request):
    return render(request, 'shops/payment/paymentsuccess.html')

@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature}
            # verify the payment signature.
            # result = razorpay_client.utility.verify_payment_signature(params_dict)
            util = razorpay.Utility(client)
            util.verify_payment_signature(params_dict)
            if util is None:
                amount = 20000  # Rs. 200
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    # render success page on successful caputre of payment
                    return render(request, 'shops/payment/paymentsuccess.html')
                except:
                    # if there is an error while capturing payment.
                    return render(request, 'shops/payment/paymentfailed.html')
            else:
 
                # if signature verification fails.
                return render(request, 'shops/payment/paymentfailed.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()


def countdown(t):
    time_completed = False
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        t -= 1 
    time_completed = True
    return time_completed

def DetectCurrentLocation(request):
    if request.POST.get('lon'):
        lon = request.POST.get('lon')
        lat = request.POST.get('lat')
        lat1 = float(lat)
        lon1 = float(lon)
        ob = Shop.objects.all()
        my_list = {}
        new_list = list()
        for i in ob:
            lon2 = float(i.lon)
            lat2 = float(i.lat)
            theta = lon1-lon2
            dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
            dist = math.acos(dist)
            dist = math.degrees(dist)
            miles = dist * 60 * 1.1515
            distance = miles * 1.609344
            distance = round(distance, 1)
            my_list= {
            'name':i.name,
            'city':i.city,
            'distance':distance,
            'address':i.address,
            'id':i.pk,
            }
            new_list.append(my_list)
        new_list.sort(key=lambda x: x["distance"])
        return JsonResponse({'context':new_list})
    return render(request,'user/home/select-location.html')


