from django.contrib import admin
from .models import *

class showregister(admin.ModelAdmin):
    list_display = ['id','name','password','email','address','profile_pic']

admin.site.register(registermodel,showregister)
# Register your models here.

class showcategory(admin.ModelAdmin):
    list_display = ['id','catname']
admin.site.register(category,showcategory)

class showproduct(admin.ModelAdmin):
    list_display = ['id','product_name','catid','description','price','product_photo','status',"seller"]
admin.site.register(product,showproduct)

class showproductimage(admin.ModelAdmin):
    list_display = ['productid','product_image','productimg']
admin.site.register(productimage,showproductimage)

class showinquiry(admin.ModelAdmin):
    list_display = ['userid','productid','phone','address','budget','quantity','msg','status','timestamp']
admin.site.register(productinquiry,showinquiry)

class showcart(admin.ModelAdmin):
    list_display = ["id","userid","productid","quantity","totalamount","orderstatus","orderid"]

admin.site.register(cart,showcart)

class showorder(admin.ModelAdmin):
    list_display = ["id","userid","finaltotal","phone","address","paymode","status"]

admin.site.register(ordermodel,showorder)