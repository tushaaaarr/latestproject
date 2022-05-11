from django.shortcuts import render, redirect ,HttpResponse
from customuser.models import user_type,Prescription,Image,StoreBill
from django.shortcuts import render,HttpResponse ,redirect
from datetime import datetime
from .models import Orders, PersonalDetails,Shop
from .models import ParselImage,DeliveryPartner
import json
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required
from pytonik_time_ago.timeago import timeago

def is_appview(myurl):
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        return True
    except:          
        return False


@login_required(redirect_field_name='next',login_url = '/login')
def StoreNotifications(request):
    type_obj = user_type.objects.get(user=request.user)
    if request.user.is_authenticated and type_obj.is_store==True:
        is_store = True
        allObj = Orders.objects.filter(s_username=request.user)
        latestObj = allObj.order_by('-date')[:5]
        messages1 = []
        my_dict = {}
        items = []
        for i in latestObj:  
            sendername = str(PersonalDetails.objects.filter(username=i.c_username)[0].fname) + str(' ') + str(PersonalDetails.objects.filter(username=i.c_username)[0].lname)
            shopob = Shop.objects.filter(store_user=request.user)
            photo = shopob[0].storephoto 
            if i.order_accept_status == 'not_responded':
                which_color = '#C0C0C0;'
            else:
                which_color = '#F5F5F5;'
            # Time Ago 
            time = i.date.strftime('%H:%M:%S')
            date = i.date.date()
            mixed = str(date) + str(time)
            time_ago = timeago(f"{str(date)} {str(time)}").ago
            # create dictionary
            my_dict = {
                'senderId':i.c_username,
                'sender':sendername,
                'reciver':i.s_username,
                'id':i.id,
                'date':time_ago,
                'message':i.store_notification_1,
                 'photo':str(photo),
                'which_color':which_color,
            }
            messages1.append(my_dict)

    if is_appview(request.path) == True: 
        templates = 'app-view/store/home/request.html'
    else:          
        templates = 'store/home/request.html'
    context = {'messages_list':messages1} 
    return render(request,templates,context)

@login_required(redirect_field_name='next',login_url = '/login')
def StoreNotificationDetails(request,current_user,myid):
    type_obj = user_type.objects.get(user=request.user)
    context = {}
    if request.user.is_authenticated and type_obj.is_store==True:
        order_details = Orders.objects.filter(id=myid)
        images_id = order_details[0].images_id
        inbox_items = order_details[0].inbox_items
        inbox_items = json.loads(inbox_items)
        items_dict = {}
        items_list = []
        if len(inbox_items) >= 1:
            for i in inbox_items:
                prod_name=inbox_items[i][0] 
                prod_pack = inbox_items[i][1] 
                qty = inbox_items[i][2] 
                items_dict = {
                    'Product':prod_name,
                    'Pack':prod_pack,
                    'Quantity':qty,
                }
                items_list.append(items_dict)
                context['Items_show'] = True
        else:
             context['Items_show'] = False
           
        context['Is_responsed'] = False
        if order_details[0].order_accept_status == 'accepted':
            context['Is_responsed'] = True
            context['text'] = 'You have accpeted delivery request'
        elif order_details[0].order_accept_status == 'rejected':
            context['Is_responsed'] = True
            context['text'] = 'You have rejected delivery request' 

        data = []
        reqeust_sender = order_details[0].c_username
        images_data = ''
        try:
            all_data = Image.objects.filter(store_user=request.user).filter(user=current_user).order_by('-date')
            last_item = Image.objects.filter(user=reqeust_sender).filter(store_user=request.user).last()
            last_time = last_item.date
            last_time = last_time.strftime('%H:%M:%S')
            for i in all_data:
                if i.date.strftime('%H:%M:%S')[:5] == last_time[:5]:
                    if len(i.desc) < 2:
                        i.desc = ""
                        data.append(i)
                    else:
                        data.append(i)
            pres_data = Prescription.objects.filter(id=images_id)
            context['IsIns'] = False
            context['instructions'] = pres_data[0].desc
            if len(context['instructions']) > 5:
                context['IsIns'] = True    
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
        IsAccepted = order_details[0]
    params = {
        'data':data,'type_obj':type_obj,'myid':myid,
       'items_list':items_list,
        'IsAccepted':IsAccepted, 'images_data':images_data,
        'context':context}
        
    if is_appview(request.path) == True:
        url_path = 'app-view/store/home/notification-view.html'
    else:          
        url_path = 'store/home/notification-view.html'
    return render(request,url_path,params)

@login_required(redirect_field_name='next',login_url = '/login')
def AcceptCustomerOrder(request):
    type_obj = user_type.objects.get(user=request.user)
    if request.user.is_authenticated and type_obj.is_store==True:  
        user_noti_1 = 'Thanks for ordering.. Your delivery request has been accepted choose your payment method and go ahed'
        if request.POST.get('store_response'):
            store_response = request.POST.get('store_response')
            DataId = request.POST.get('data_id')
            is_accepted = store_response[:8]
            which_user = store_response[9:]
            if str(is_accepted) == 'accpeted':
                Orders.objects.filter(id=DataId).update(user_notification_1 = user_noti_1,order_accept_status='accepted')
                # Update Prescrition Status -- Accpted
                Prescription.objects.filter(id = DataId).update(responed_status='accepted')
                return redirect(f"/app-view/store-order-response/{DataId}")
            else:
                user_noti_1 = 'We are not able to accept your request.  '
                Orders.objects.filter(id=DataId).update(user_notification_1 = user_noti_1,order_accept_status='rejected')
                return redirect(f"/store-order-response/{DataId}")

@login_required(redirect_field_name='next',login_url = '/login')
def StoreResponse(request,myid):
    OrdersObj1 = Orders.objects.filter(id=myid)
    OrdersObj = OrdersObj1[0]  
    if request.FILES.get("inputbillimage"):
        image_path = request.FILES.get("inputbillimage") 
        OrdersObj1.update(is_bill_uploaded=True)
        StoreBill(image = image_path,order_id = myid).save()
        bill_uploaded = 'active'
        if is_appview(request.path) == True:
            return redirect(f'/app-view/store-order-response/{myid}')
        else:
            return redirect(f'/store-order-response/{myid}')

    if request.POST.get('rejection_reason'):
        enteramount = request.POST.get('rejection_reason')
        if enteramount == '1':
            reason = 'Out of Stock'
        elif enteramount == '2':
            reason = 'Prescription is not clear'
        elif enteramount == '3':
            reason = 'Required doctors prescription'
        OrdersObj1.update(rejection_reason=reason)
        if is_appview(request.path) == True:
            return redirect('/app-view/store-notifications')
        else:
            return redirect('/store-notifications')

    if request.POST.get('enteramount'):
        enteramount = request.POST.get('enteramount')
        OrdersObj1.update(store_amount=enteramount)
        AmountFilled = True
        filled_amount = 'active'
        if is_appview(request.path) == True:
            return redirect(f'/app-view/store-order-response/{myid}')
        else:
            return redirect(f'/store-order-response/{myid}')

    if OrdersObj.store_amount == "":
        AmountFilled = False
        filled_amount = ''        
    else:
        AmountFilled = True
        filled_amount = 'active'

    if request.POST.get('process_completed'):
        if AmountFilled == True and OrdersObj.is_bill_uploaded == True:
            if is_appview(request.path) == True:
                return redirect('/app-view/store-notifications')
            else:
                return redirect('/store-notifications')
    else:
        pass
    OrdersObj1 = Orders.objects.filter(id=myid)
    OrdersObj = OrdersObj1[0]

    if OrdersObj.is_bill_uploaded == True:
        bill_uploaded = 'active'
    else:
        bill_uploaded = ''

    params = {
        'OrdersObj':OrdersObj,'AmountFilled':AmountFilled,'bill_uploaded':bill_uploaded,
        'filled_amount':filled_amount,
        }
    if is_appview(request.path) == True:  
        url_path = 'app-view/store/home/response.html'
    else:          
        url_path = 'store/home/response.html'
    return render(request,url_path,params)












