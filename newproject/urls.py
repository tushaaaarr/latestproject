
from os import name
from django.contrib import admin
from django.urls import path
from customuser import views,customers,deliver,store
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # for store owner
    path('users-notifications',customers.UsersNotifications,name='users-notifications'),
    path('users-notification/details/<str:current_user>/<int:myid>',views.UsersNotificationDetails,name="UsersNotificationDetails"),
    path('admin/', admin.site.urls), 
    path("",views.home,name='home'),
    path('medical_store_view/<int:myid>',customers.medical_store_view, name = 'medical_store_view'),
    path('store-view/<int:myid>/<str:st_name>/<str:st_dist>',customers.medical_store_view, name='medical_store_view'),
    path('medical-store-view/<int:myid>/upload-prescriptions',customers.upload, name = 'medical_store_view'),
    path('upload',customers.upload,name='upload'),      
    path('logout', views.handelLogout, name="handleLogout"),
    path('app-view/logout',views.handelLogout,name='handelLogout'),
    path('login', views.login_attempt, name="handleLogin"),
    path('app-view/home/login',views.login_attempt, name='handleLogin'),
    path('checkout',customers.CheckOut,name='checkout'),
    path('myorders',customers.MyOrders,name='myorders'),
    path('order-tracker/<int:myid>',customers.OrderTracker,name='order-tracker'),
    path('customers-billing-page/<str:user_name>/<int:myid>',customers.CustomerBilling,name='CustomerBilling'),
    path('add-your-chemiest',views.AddYourChemist,name='add-your-chemiest'),
    path('make-payment',views.Payment,name='make-payment'),
    path('paymenthandler/',views.handlerequest,name='handlerequest'),
    path('payment-success',views.PaymentSuccess,name='payment-success'),
    # Profile ---   
    path('my-addresses',customers.MyAddresses,name='app-view/my-addresses'),
    path('users/<str:fname>-<str:lname>/profile/my-addresses',customers.MyAddress,name='MyAddress'),
    # path('sample',views.sample,name='sample'),
    path('new-login',views.login_attempt , name="login"),
    path('register' , views.register , name="register"),
    path('otp' , views.otp , name="otp"),
    path('login-otp',views.login_otp , name="login_otp") ,
    path("logout/", views.handelLogout, name="logout"),
    # New Urls
    path('home/select-location',customers.Select_Location_Store,name='Select_Location_Store'),
    path('detect-users-location',views.DetectCurrentLocation,name='DetectCurrentLocation'),

    # Application View 
    # For User
    path('app-view/home',views.Appview,name='app-view/home'),
    path('app-view/home/select-location',customers.Select_Location_Store,name='Select_Location_Store'),
    path('app-view/store-view/<int:myid>/<str:st_name>/<str:st_dist>',customers.medical_store_view, name='medical_store_view'),
    path('app-view/medical-store-view/<int:myid>/upload-prescriptions',customers.upload, name = 'medical_store_view'),
    path('app-view/checkout',customers.CheckOut,name='checkout'),
    path('app-view/users-notifications',customers.UsersNotifications,name='app-view/notifications'),
    path('app-view/users-notification/details/<str:current_user>/<int:myid>',views.UsersNotificationDetails,name="UsersNotificationDetails"),
    path('app-view/myorders',customers.MyOrders,name='app-view/myorders'),
    path('app-view/order-tracker/<int:myid>',customers.OrderTracker,name='app-view/order-tracker'),
    path('app-view/user/profile',views.AppMyProfile,name='MyProfile'),
    path('app-view/my-addresses',customers.MyAddresses,name='app-view/my-addresses'),
    path('app-view/add-your-chemiest',views.AddYourChemist,name='add-your-chemiest'),
    path('app-view/customers-billing-page/<str:user_name>/<int:myid>',customers.CustomerBilling,name='CustomerBilling'),

    #For Store
    path('store-notifications',store.StoreNotifications,name='store-notifications'),
    path('app-view/store-notifications',store.StoreNotifications,name='store-notifications'),
    path('store-notification/details/<str:current_user>/<int:myid>',store.StoreNotificationDetails,name="notification_view_details"),
    path('app-view/store-notification/details/<str:current_user>/<int:myid>',store.StoreNotificationDetails,name="notification_view_details"),
    path('notification_view',store.AcceptCustomerOrder,name='notification_view'),
    path('store-order-response/<int:myid>',store.StoreResponse,name='store-order-response'), 
    path('app-view/store-order-response/<int:myid>',store.StoreResponse,name='store-order-response'),
        
    #For Delivery-Partner
    path('app-view/get-delivery-requests',deliver.GetDeliveryRequests,name='get-delivery-requests'),
    path('delivery-accepted',deliver.DeliveryAccepted,name='delivery-accepted'),    
    path('register-delivery-partner',deliver.RegisterDeliveryPartner, name='register-delivery-partner'),
    path('delivery-partner-response/<int:myid>',deliver.DeliveryPartnerResponse,name='DeliveryPartnerResponse'),
    path('get-new-delivery',deliver.GetDeliveryRequests,name='get-new-delivery'),
    path('app-view/register-delivery-partner',deliver.RegisterDeliveryPartner, name='register-delivery-partner'),


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
