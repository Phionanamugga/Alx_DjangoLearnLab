from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'bio', 'followers_count', 'following_count']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture', 'followers')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

