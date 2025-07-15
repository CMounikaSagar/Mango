from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'username', 'email', 'first_name', 'last_name', 'is_admin')
    search_fields = ('phone_number', 'username', 'email')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','last_login','date_joined','is_active')
    list_display_links = ('email','first_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileadmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="()" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = "Profile Picture"
    list_display = ('thumbnail','user','city','state')
    
admin.site.register(Account,AccountAdmin)
# admin.site.register( UserProfileadmin)
admin.site.register( User_Profile_Model)