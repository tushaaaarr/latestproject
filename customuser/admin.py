# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User,user_type,Shop,PersonalDetails,Image,Prescription,GetDeliveries,Cities
from .models import Orders,StoreBill,ParselImage,NotificationReminder,DeliveryPartner,Profile,SavedAddress

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'name', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)

# We can register our models like before
# This was the model we commented in the previous snippet.

admin.site.register(user_type)
admin.site.register(Shop)
admin.site.register(Cities)
admin.site.register(Image)
admin.site.register(PersonalDetails)
admin.site.register(Prescription)
admin.site.register(GetDeliveries) 
admin.site.register(Orders)
admin.site.register(StoreBill)
admin.site.register(ParselImage)
admin.site.register(NotificationReminder)
admin.site.register(DeliveryPartner)
admin.site.register(Profile)
admin.site.register(SavedAddress)