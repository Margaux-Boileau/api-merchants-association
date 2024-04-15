from django.contrib import admin
from .models import Shop

# Register your models here.
#admin.site.register(Shop)

class ShopAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Shop, ShopAdmin)