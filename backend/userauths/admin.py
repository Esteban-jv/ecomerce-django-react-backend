from django.contrib import admin
from .models import User, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ['email','username','first_name','last_name']
    search_fields = ['email','username','phone','first_name','last_name']
    list_filter = ['is_active','is_staff','is_superuser']

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
