



from argparse import _MutuallyExclusiveGroup
from ast import Pass
from typing import Text
from django.db.models import indexes
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth import authenticate, login
from stripe import Order
from customuser.models import user_type, User
from django.shortcuts import render,HttpResponse ,redirect
from django.views import generic
from django.contrib import messages 
from geopy.geocoders import Nominatim
from datetime import datetime
from playsound import playsound
import time

# from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
from .models import Orders, PersonalDetails,Shop
from .models import ParselImage,DeliveryPartner
# from geopy.geocoders import Nominatim
import json
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required
from pytonik_time_ago.timeago import timeago
import string    
import random

def is_appview(myurl):
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        return True
    except:          
        return False

#Delivery Requests for Delivery boy
@login_required(redirect_field_name='next',login_url = '/login')
def GetDeliveryRequests(request):
    store_dict = {}
    storelist = []
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_delivery==True:
        filterd_orders = Orders.objects.filter(payment_status ='cod').filter(deliver_status = False)
        for order in filterd_orders:
            shop_ob = Shop.objects.filter(store_user = str(order.s_username))
            storename = shop_ob[0].name 
            storeaddress = shop_ob[0].address
            id = order.id
            time = order.date.strftime('%H:%M:%S')
            date = order.date.date()
            mixed = str(date) + str(time)
            time_ago = timeago(f"{str(date)} {str(time)}").ago
            store_dict = {
                'storename': storename,
                'storeaddress':storeaddress,
                'id':id,
                'time':time_ago
            }
            storelist.append(store_dict)
        context = {'storelist':storelist}
        return render(request,'deliver/home/index.html',context)
    else:
        return HttpResponse('Page Not Found..')

@login_required(redirect_field_name='next',login_url = '/login')
def DeliveryAccepted(request):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_delivery==True:
        if request.POST.get('accept_btn'):
            del_response = request.POST.get('accept_btn')
            deliver = PersonalDetails.objects.filter(username = request.user)[0]
            delivername = str(deliver.fname) + str(deliver.lname)
            delivermobile = deliver.mob
            Orders.objects.filter(id=int(del_response)).update(deliver_status = True,is_timeup = True,
            d_username=str(request.user))
            return redirect(f'/delivery-partner-response/{del_response}')
    return render(request,'deliver/home/index.html')

@login_required(redirect_field_name='next',login_url = '/login')
def DeliveryPartnerResponse(request,myid):
    is_parsel_uploaded = ''
    is_order_confirmed = ''
    CurrrentOrder = Orders.objects.filter(id = myid)
    # Store details 
    store_details = {}
    store_username = Shop.objects.get(store_user=CurrrentOrder[0].s_username)
    store_details['name'] = store_username.name
    store_details['address'] = store_username.address
    store_details['lat'] = store_username.lat
    store_details['lon'] = store_username.lon

    if request.POST.get('customer_otp'):
        customer_otp = request.POST.get('customer_otp')
        if customer_otp != CurrrentOrder[0].customer_otp:
            pass
        else:
            CurrrentOrder.update(filled_otp=True,is_reached_store=True)
            
    if request.FILES.get("parsel_image"):
            image_path = request.FILES.get("parsel_image")
            is_parsel_uploaded = 'active'
            is_order_confirmed = 'active'
            ParselImage(image = image_path,order_id = myid).save()
            CurrrentOrder.update(order_picked_status = True ,on_way_status = True,is_parsel_uploaded = True)
    
    if CurrrentOrder[0].order_picked_status == True:
        is_parsel_uploaded = 'active'
        is_order_confirmed = 'active'
    if request.POST.get('order_picked'):
        CurrrentOrder.update(order_picked_status = True ,on_way_status = True,is_parsel_uploaded = True,order_picked = True)

    if request.POST.get('reached_customer_location'):
        CurrrentOrder.update(reached_location_status = True)
    
    if request.POST.get('collected_cash'):
        CurrrentOrder.update(order_completed = True)
        return redirect('/')    

    if PersonalDetails.objects.filter(username = CurrrentOrder[0].c_username).exists():
        Obj = PersonalDetails.objects.filter(username = CurrrentOrder[0].c_username)[0]
        CustomerrName = str(Obj.fname) + str(" ") + str(Obj.lname)
        customer_details = {}
        store_username = Shop.objects.get(store_user=CurrrentOrder[0].s_username)
        customer_details['lat'] = Obj.lat
        customer_details['lon'] = Obj.lon

    time = datetime.now()
    picked_time = time.strftime('%H:%M:%S')[:5]
    context = {'CurrrentOrder':CurrrentOrder[0],'is_order_confirmed':is_order_confirmed,'is_parsel_uploaded':is_parsel_uploaded,
    'CustomerrName':CustomerrName,'picked_time':picked_time,
    'store_data':store_details,
    'store_details':json.dumps(store_details),
    'customer_details':json.dumps(customer_details)}
    return render(request,'app-view/deliver/home/delivery-partner-response.html',context) 

@login_required(redirect_field_name='next',login_url = '/login')
def RegisterDeliveryPartner(request):
    if request.method == 'POST':
        if request.POST.get('select_city'):
            select_city = request.POST.get('select_city')
        if request.FILES.get("adhar_doc"):
            adhar_doc = request.FILES.get("adhar_doc")  
        if request.POST["src"]:
            image_path = request.POST["src"]  # src is the name of input attribute in your html file, this src value is set in javascript code
            image = NamedTemporaryFile()
            image.write(urlopen(image_path).read())
            image.flush()
            image = File(image)
            name = str(image.name).split('\\')[-1]
            name += '.jpg'  # store image in jpeg format
            image.name = name
        if request.POST.get('agree_conditions'):
            is_agree = request.POST.get('agree_conditions')
        DeliveryPartner(username=str(request.user),city=select_city,selfie = image,adhar =adhar_doc).save()  
        if is_appview(request.path) == True:
            return redirect('/app-view/home')  
        else:     
            return redirect('/')  

    if is_appview(request.path) == True:
        url_path = 'app-view/user/home/register-delivery-partner.html'
    else:          
        url_path = 'user/home/register-delivery-partner.html'
    return render(request,url_path)

