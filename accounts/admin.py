from django.contrib import admin
from . models import User

class UserAdmin(admin.ModelAdmin):
    list_display=("username",'password','is_superuser','is_staff','user_type','added_by','date_joined','is_active','last_login')


admin.site.register(User,UserAdmin)