from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth import authenticate, login
from customuser.deliver import is_appview
from customuser.models import user_type
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
import requests
from .models import Orders, PersonalDetails, Shop,Image,Prescription,Cities
from .models import StoreBill,NotificationReminder,SavedAddress
# from geopy.geocoders import Nominatim
from math import e, remainder, sin, cos, radians, degrees, acos
import math
import json
from django.http import JsonResponse
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from newproject.settings import RAZORPAY_API_KEY
from newproject.settings import RAZORPAY_API_SECRET_KEY
import razorpay
from django.contrib.sites.shortcuts import get_current_site
import razorpay
from pytonik_time_ago.timeago import timeago
import string    
import random
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
razorpay_client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))

def is_appview(myurl):
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        return True
    except:          
        return False

def Select_Location_Store(request):
    context = {}
    if request.POST.get('input_city_name'):
        city_input = request.POST.get('input_city_name')
        ob = Cities.objects.all()
        current_city_dict = {}
        current_city = list()
        for j in ob:
            if j.city_name.lower() == city_input.lower():
                current_city_dict = {
                'city_name':j.city_name,
                'state':j.state,
                }
                current_city.append(current_city_dict)  
        geolocator = Nominatim(user_agent="my_user_agent")
        country = 'india'
        city = city_input
        state = current_city[0]['state']
        placeholder_city = f'{city}, {state}'
        loc = geolocator.geocode(city+','+ country + ',' + state)
        lat1 = loc.latitude
        lon1 = loc.longitude        
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
        context = {'new_list':new_list}

    if is_appview(request.path) == True:
        templates = 'app-view/user/home/select-location.html'
    else:          
        templates = 'user/home/select-location.html'
    return render(request,templates,context)

@login_required(redirect_field_name='next',login_url = '/login')
def medical_store_view(request,myid,st_name,st_dist):
    data = Shop.objects.filter(id = myid)
    distance = st_dist
    name = data[0].name
    store_user = data[0].store_user
    city_name = data[0].city
    address = data[0].address 
    coord = {'lat':data[0].lat,'lon':data[0].lon}
    id_ = myid
    if request.method == 'POST':
        display_type = request.POST.get('is_conditions' or None)    
        myfile = request.FILES["image_file"] 
        user_id = request.user
        saved = Image(image=myfile,user=request.user,store_user=store_user)
        saved.save()
    else:
        pass
    context =  {'name':name,'city_name':city_name,'address':address,'distance':distance,'myid':myid,'id_':id_,'coord':json.dumps(coord)}
    myurl = request.path
    obj = myurl.split('/')
    if is_appview(request.path) == True:
        templates = 'app-view/user/home/store-view.html'
    else:          
        templates = 'user/home/store-view.html'
    return render(request,templates,context)
 
@login_required(redirect_field_name='next',login_url = '/login')                
def upload(request,myid):
    product = ''
    previus_10 = []
    history = Image.objects.filter(user = request.user)[:10]
    for j in history:
        j.date = j.date.strftime("%b-%d-%Y") 
        previus_10.append(j)
    current_data=Shop.objects.filter(id = myid)
    id_ = myid
    name = current_data[0].name
    store_user = current_data[0].store_user
    city_name = current_data[0].city
    address = current_data[0].address 
    
    if request.POST.get('PresItems'):
        list_id = list()
        images_list = list()
        item_list = list()
        PresItems = json.loads(request.POST.get('PresItems', False))
        for i in PresItems:
            list_id.append(int(i))
        imgs_data = Image.objects.all()
        for img in imgs_data:
            if img.id in list_id:
                item_list.append(img)
                images_list.append(str(img.image))
        user=item_list[0].user
        store_user = item_list[0].store_user
        current_data=Shop.objects.filter(store_user = store_user)
        name = current_data[0].name
        store_user = current_data[0].store_user
        city_name = current_data[0].city
        address = current_data[0].address 
        list_img = list()
        item = images_list 
        message = 'You have got request for medicines'
        if len(item) == 5:          
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=item[0],image2=item[1],image3=item[2],
            image4=item[3],image5=item[4],message=message)
            new_data.save()
        elif len(item) == 4:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=item[0],image2=item[1],image3=item[2],
            image4=item[3],message = message)
            new_data.save()
        elif len(item) == 3:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=item[0],image2=item[1],image3=item[2],message =message)
            new_data.save()
        elif len(item) == 2:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=item[0],image2=item[1],message = message)
            new_data.save()
        elif len(item) == 1:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=item[0],message = message)
            new_data.save()

        if is_appview(request.path) == True:
            return redirect('/app-view/checkout')
        else:          
            return redirect('/checkout')

    # Upload images from gallary--
    elif request.method == 'POST':
        data = request.FILES.getlist("images")
        desc = request.POST.get('instructions')
        message = 'You have got request for medicines'
        for i in data:
            new_image = Image(image = i,user = request.user,store_user = store_user)
            new_image.save()
        if len(data) == 5:          
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=data[0],image2=data[1],image3=data[2],
            image4=data[3],image5=data[4],desc = desc,message=message)
            new_data.save()
        elif len(data) == 4:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=data[0],image2=data[1],image3=data[2],
            image4=data[3],desc = desc,message = message)
            new_data.save()
        elif len(data) == 3:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=data[0],image2=data[1],image3=data[2],desc = desc,message =message)
            new_data.save()
        elif len(data) == 2:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=data[0],image2=data[1],desc = desc,message =message)
            new_data.save()
        elif len(data) == 1:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=data[0],desc = desc,message = message)
            new_data.save()
       
        if is_appview(request.path) == True:
            return redirect('/app-view/checkout')
        else:          
            return redirect('/checkout')

    context = {'id_':id_,'product':product,'previus_10':previus_10,'CurrentId':myid}

    if is_appview(request.path) == True: 
        templates = 'app-view/user/home/upload-prescription.html'
    else:          
        templates = 'user/home/upload-prescription.html'
    return render(request,templates,context)

item_list = []
pres_list = []
@login_required(redirect_field_name='next',login_url = '/login')
def CheckOut(request):
    myurl = request.path
    data = None
    if request.is_ajax() and request.POST.get('data'):
        inputdata = request.POST.get('data')
        data = json.loads(inputdata)
        item_list.append(data)
        return JsonResponse({'data':data,'item_list':item_list})

    if request.is_ajax() and request.POST.get('newaddress'):
        if request.POST.get('newaddress'):
            inputdata = request.POST.get('newaddress')
            inputdata = json.loads(inputdata)
            SavedAddress(username = str(request.user),room_no = inputdata[0], landmark = inputdata[1]).save()
            new_add_data = {'floor':inputdata[0],'landmark':inputdata[1]}
        return JsonResponse({'inputdata':new_add_data})

    if request.is_ajax():
        saved_address = SavedAddress.objects.filter(username=str(request.user))
        item = {}
        saved_address_list= []
        for add in saved_address:
            item = {
            'floor_no':add.room_no,
            'landmark':add.landmark.capitalize()
            }
            saved_address_list.append(item)
        return JsonResponse({'addresslist':saved_address_list})
    
    IsPrescription = None
    username = request.user
    IsOldCustomer = None
    OldCheckout = None
    pres_data = None
    pred_id = ''
    images_data = None
    
    # Without Prescription
    if request.POST.get('selected_store'):
        storeid = request.POST.get('selected_store')
        current_data=Shop.objects.filter(id = int(storeid))
        store_user = current_data[0].store_user
        reciver = store_user
        pres_list.append(reciver)

    try: 
        reciver = pres_list[-1]
        if len(pres_list) > 5:
            pres_list.pop(0)
    except:
        reciver = pres_list
   
    try:
        last_id = Prescription.objects.filter(sender = request.user).last().id
        pres_data = Prescription.objects.filter(id=last_id)
        pers_dict = {}  
        for pers in pres_data:
            if pers.image1 != 'default.jpg':
                pers_dict[0] = pers.image1            
            if pers.image2 != 'default.jpg':
                pers_dict[1] = pers.image2 
            if pers.image3 != 'default.jpg':           
                pers_dict[2] = pers.image3 
            if pers.image4 != 'default.jpg':
                pers_dict[3] = pers.image4 
            if pers.image5 != 'default.jpg':
                pers_dict[4] = pers.image5
        images_data = []
        for img in range(len(pers_dict)):
            images_data.append(pers_dict[img])
        pred_id = pres_data[0].id
        reciver = Prescription.objects.filter(id= pred_id)[0].reciver
    except:
        pass
    FullName = ''
    if Orders.objects.filter(c_username = request.user).exists():
        PersName = PersonalDetails.objects.filter(username = request.user)[0]
        FullName = str(PersName.fname) + str(' ') + str(PersName.lname) 
        PersonalDetails.objects.filter(username = request.user)[0].fname 
        IsOldCustomer = True
        OldCheckout = Orders.objects.filter(c_username = request.user).last()
    else:
        IsOldCustomer = False

    if request.POST.get('selected_address'):
        selected_address = request.POST.get('selected_address')
        selected_products = request.POST.get('selected_products')   
        ob = SavedAddress.objects.filter(username=str(request.user))[int(selected_address)]
        Address = str(ob.landmark) + str(',') + str(ob.room_no)
        customername = request.POST.get('inputname')
        address = Address
        city = ''
        flat_no = ob.room_no
        pincode = '416101'
        items = ''
        new_inbox_items = json.loads(selected_products)
        # Creating new_inbox_items 
        store_noti_1 = 'You have got request for medicines'
        if customername == '':   
            if Orders.objects.filter(c_username=username).exists():
                PrevOrder = Orders.objects.filter(c_username=str(request.user)).last()
                new_order = Orders(c_username = username,s_username = reciver,images_id = pred_id,
                            items=items,inbox_items=new_inbox_items,city=PrevOrder.city,
                            address =PrevOrder.address,
                            phone=PrevOrder.phone,pincode=PrevOrder.pincode,
                            store_notification_1 = store_noti_1)
                new_order.save()
        else:
            new_order = Orders(c_username = username,s_username = reciver,images_id = pred_id,
                                items=items,inbox_items=new_inbox_items,city=city,flat_no = flat_no,
                                address =address,pincode=pincode,store_notification_1 = store_noti_1)
            new_order.save()
        last_order = Orders.objects.filter(c_username=str(request.user)).last().id
        new_id = Orders.objects.filter(images_id = pred_id)[0].id
        new_id = str(GenerateOrderId()) + str(new_id)
        Orders.objects.filter(images_id = pred_id).update(orderid = new_id)
        NotificationReminder(order_id = last_order).save()
        myurl = request.path
        obj = myurl.split('/')
        try:
            obj.index('app-view') 
            return redirect('/app-view/home')
        except:        
            return redirect('/')

    context = {'OldCheckout':OldCheckout,'IsOldCustomer':IsOldCustomer,'pres_data':pres_data,'images_data':images_data,
        IsPrescription:'IsPrescription','pred_id':pred_id,'FullName':FullName,
        'data':data}
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/user/home/checkout.html'
    except:          
        templates = 'user/home/checkout.html'
    return render(request,templates,context)

def GenerateOrderId():
    S = 10   
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
    order_id =str(ran)
    return order_id

@login_required(redirect_field_name='next',login_url = '/login')
def UsersNotifications(request):
    # Notifications for users
    type_obj = user_type.objects.get(user=request.user)
    if request.user.is_authenticated and type_obj.is_user==True:
        is_user = True
        objs =  my_notif = Orders.objects.filter(c_username=request.user).order_by('-date')
        messages1 = []
        my_dict = {}
        items = []
        new_data = None
        for i in objs: 
            try:
                sendername = str(PersonalDetails.objects.filter(username=i.s_username)[0].fname) + str(' ') + str(PersonalDetails.objects.filter(username=i.s_username)[0].lname)
            except:
                sendername = ''
            if i.order_completed == False:
                which_color = '#C0C0C0;'
            else:
                which_color = '#F5F5F5;'
            shopob = Shop.objects.filter(store_user=i.s_username)
            photo = shopob[0].storephoto
             # Time Ago 
            time = i.date.strftime('%H:%M:%S')
            date = i.date.date()
            mixed = str(date) + str(time)
            time_ago = timeago(f"{str(date)} {str(time)}").ago
            my_dict = {
                'sender':sendername,
                'senderId':i.s_username,
                'reciver':i.c_username,
                'id':i.id,
                'date':time_ago,
                'message':f'You have recied notification for order id DH231K{i.id}',
                'which_color':which_color,
                'photo':str(photo),
            }
            messages1.append(my_dict)
        myurl = request.path
        obj = myurl.split('/')
        try:
            obj.index('app-view') 
            templates = 'app-view/user/home/notifications.html'
        except:          
            templates = 'user/home/notifications.html'

        context = {'messages_list':messages1}
        return render(request,templates,context)
    else:
        return HttpResponse('Please Login as a Store.. ')

@login_required(redirect_field_name='next',login_url = '/login')
def MyOrders(request):
    myorders = []
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_user==True:
        if request.method == 'POST':
            input_id = request.POST.get('inputid')
            ord = Orders.objects.filter(id =input_id)
            time = ord[0].date.strftime('%H:%M:%S')
            date = ord[0].date.date()
            mixed = str(date) + str(time)
            time_ago = timeago(f"{str(date)} {str(time)}").ago
            try:
                if time_ago.split(' ')[1] == 'minutes':
                    if int(time_ago.split(' ')[0]) > 5:
                        pass
                    else: 
                        ord.update(is_cancelled = True)
            except:
                pass
        data = Orders.objects.filter(c_username = str(request.user)).order_by('-date')[:5]
        for i in data:
            ShopOb = Shop.objects.get(store_user = i.s_username)
            i.date = i.date.strftime("%b-%d-%Y") 
            newdict = {
                's_name':ShopOb.name,
                's_photo':ShopOb.storephoto,
                'date':i.date,
                'id':i.id,
                'order_completed':i.order_completed,
                'is_cancelled':i.is_cancelled,
            }
            myorders.append(newdict)
    if is_appview(request.path) == True:
        url_path = 'app-view/user/home/myorder.html'
    else:          
        url_path = 'user/home/myorder.html'
    return render(request,url_path,{ 'myorders':myorders})

@login_required(redirect_field_name='next',login_url = '/login')
def OrderTracker(request,myid):
    context = {}
    # order cancellation 
    if request.POST:
        if request.POST.get('cancel_ord'):
            Orders.objects.filter(id = myid).update(is_cancelled = True)
            return redirect(request.path)

    data = Orders.objects.filter(id=myid)
    data = data[0]
    context['order_id'] = data.orderid
    context['ShopName'] = Shop.objects.filter(store_user=data.s_username)[0].name
    DeliveryDate = data.date.strftime("%b-%d-%Y") 
    if len(data.d_username) > 1:
        context['is_accepted_delivery'] = True
        Obj = PersonalDetails.objects.filter(username = data.d_username)[0]
        context['DeliverName']=str(Obj.fname) + str(" ") + str(Obj.lname)
        context['DeliverMobile'] = Obj.mob
        context['DeliveryDate'] = data.date.strftime("%b-%d-%Y") 
    else:
        context['is_accepted_delivery'] = False
    images_data = ''        
    try:
        pres_id = data.images_id
        pres_data = Prescription.objects.filter(id=pres_id)
        pers_dict = {}
        for pers in pres_data:
            if pers.image1 != 'default.jpg':
                pers_dict[0] = pers.image1            
            if pers.image2 != 'default.jpg':
                pers_dict[1] = pers.image2 
            if pers.image3 != 'default.jpg':           
                pers_dict[2] = pers.image3 
            if pers.image4 != 'default.jpg':
                pers_dict[3] = pers.image4 
            if pers.image5 != 'default.jpg':
                pers_dict[4] = pers.image5
        images_data = []
        for img in range(len(pers_dict)):
            images_data.append(pers_dict[img])
    except:
        pass

    if data.order_accept_status == 'accepted':
        context['order_status'] = 'completed'

    if data.order_picked == True:
        context['picked_order'] = 'completed'
        
    if data.order_picked == True:
        context['picked_order'] = 'completed'
        context['order_on_way'] = 'completed'
    
    if data.reached_location_status == True:
        context['order_reached'] = 'completed'
    
    if data.order_completed == True:
        context['order_completed'] = 'completed'
        
    # num_of_pers = len(pers_dict)
    inbox_items = data.inbox_items
    prod_dict = {}
    prod_list = []
    if len(data.items) > 1:
        product_list = json.loads(data.items)
        for i in product_list:
            product_name = product_list[i][1]
            product_qty = product_list[i][0]
            prod_dict = {
                'prod_name':product_name,
                'prod_qty':product_qty,
            }
            prod_list.append(prod_dict)
    Items_show = False
    items_dict = {}
    items_list = []
    inbox_items = json.loads(inbox_items)
    if len(inbox_items) >= 1:
        Items_show = True
        prod_len = 0
        for item in inbox_items:
            prod_name=inbox_items[item][0] 
            prod_pack = inbox_items[item][1]
            qty = inbox_items[item][2]
            items_dict = {
                'Product':prod_name,
                'Pack':prod_pack,
                'Quantity':qty,
            }
            prod_len = prod_len + len(prod_name)
            items_list.append(items_dict)
    # Payment mode
    if data.payment_status=='cod':
        context['pay_mode'] = 'Pay on Delivery'
    elif data.payment_status == 'card':
        context['pay_mode'] = 'Online'
    else:
        context['pay_mode'] = 'Incomplete'  
    params = {'context':context,
    'data':data,'prod_list':prod_list,'inbox_items':inbox_items,'myid':myid,'items_list':items_list, 
   'images_data':images_data,'Items_show':Items_show}
    if is_appview(request.path) == True:
        url_path = 'app-view/user/home/order-tracker.html'
    else:          
        url_path = 'user/home/order-tracker.html'
    return render(request,url_path,params)

@login_required(redirect_field_name='next',login_url = '/login')
def MyAddresses(request):
    sel_add_list = []
    if request.POST.get('confirmed_delete'):
        myid = request.POST.get('confirmed_delete')
        SavedAddress.objects.filter(id=myid).delete()
    if request.POST.get('addressvalue'):
        sel_id = request.POST.get('addressvalue')
        floorno = request.POST.get('floorno')
        landmark = request.POST.get('landmark')
        SavedAddress.objects.filter(id=sel_id).update(landmark = landmark, room_no = floorno)
    
    if request.is_ajax():
        sel_id = request.POST.get('data')
        selected_address = SavedAddress.objects.filter(id=sel_id)
        sel_add_dict = {'lm': selected_address[0].landmark,
        'rn': selected_address[0].room_no,
        }
        sel_add_list.append(sel_add_dict)
        return JsonResponse({'selected_address':sel_add_list})
    
    try:
        addresses = SavedAddress.objects.filter(username = str(request.user))
    except:
        pass
        addresses = ''
    context = {'items':'item','addresses':addresses}
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/user/home/my-addresses.html'
    except:          
        templates = 'user/home/my-addresses.html'
    return render(request,templates,context)

@login_required(redirect_field_name='next',login_url = '/login')
def MyAddress(request,fname,lname):
    return render(request,'shops/myaddress.html')

def CustomerBilling(request,user_name,myid):
    ToalAmount = []
    if request.POST.get('payment_method'):
        value = request.POST.get('payment_method')
        customer_otp = GenerateOTP()
        if value == 'cash':
            time = datetime.now()
            Orders.objects.filter(id=myid).update(payment_status='cod',
            order_accept_time=time.strftime('%H:%M:%S'),customer_otp=customer_otp)
            # DeliveryRequests(request,myid)
            return redirect('/')
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_user==True:
        bill_image_store = []
        if StoreBill.objects.filter(order_id=myid).exists():
            item_amount = Orders.objects.filter(id=myid)[0].store_amount
            delivery_charges = 10 
            GST = 5
            ToalAmount = int(item_amount) + delivery_charges + GST
            Orders.objects.filter(id=myid).update(total_amount = ToalAmount)
            bill_image_store1 =StoreBill.objects.filter(order_id=myid)
            for j in bill_image_store1:
                j.date = j.date  = j.date.strftime('%H:%M:%S')
                bill_image_store.append(j)
            bill_image_store = bill_image_store[-1]
            CurrentOrder = Orders.objects.filter(id = myid)
        
        pers_details = PersonalDetails.objects.get(username = str(request.user))
        customer_name = str(pers_details.fname) + str(pers_details.lname) 
        customer_mobile = pers_details.mob
        customer_email = pers_details.email
        order_amount = ToalAmount * 100
        order_currency = "INR"
        payment_order = client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture =1))
        order_id = payment_order['id']
        Ob = Orders.objects.filter(id=myid).update(razorpay_order_id =order_id)
    context = {'api_key':RAZORPAY_API_KEY,'order_id':order_id,'customer_name':customer_name,
    'customer_mobile':customer_mobile,'customer_email':customer_email,
    'bill_image_store':bill_image_store,'ToalAmount':ToalAmount,'delivery_charges':delivery_charges,
    'GST':GST,}
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/user/home/billing_page.html'
    except:          
        templates = 'user/home/billing_page.html'

    return render(request,templates,context)

def GenerateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP
  
def countdown(t):
    time_completed = False
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        t -= 1 
    time_completed = True
    return time_completed



