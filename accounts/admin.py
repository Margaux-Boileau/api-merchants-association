from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
     exclude = ('is_staff', 'last_login')

admin.site.register(Account, AccountAdmin)