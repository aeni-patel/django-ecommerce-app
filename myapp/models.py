from django.db import models
from django.utils.safestring import mark_safe


class registermodel(models.Model):
    name = models.CharField(max_length=60)
    email=models.EmailField()
    password=models.CharField(max_length=250)
    phone=models.BigIntegerField()
    address=models.TextField()
    profilepicture=models.ImageField(upload_to='photos')
    gender=models.CharField(max_length=40)
    role=models.CharField(max_length=40)

    def profile_pic(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.profilepicture.url))

    profile_pic.allow_tags = True
    def __str__(self):
        return self.name

class category(models.Model):
    catname=models.CharField(max_length=90)


    def __str__(self):
        return self.catname

class product(models.Model):
    product_name=models.CharField(max_length=50)
    catid=models.ForeignKey(category,on_delete=models.CASCADE)
    product_image=models.ImageField(upload_to='photos')
    price=models.FloatField(max_length=100)
    description=models.TextField()
    status=models.CharField(max_length=60)
    seller=models.ForeignKey(registermodel,on_delete=models.CASCADE)
    def __str__(self):
        return self.product_name

    def product_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.product_image.url))

    product_photo.allow_tags = True

class productimage(models.Model):
    productid=models.ForeignKey(product,on_delete=models.CASCADE)
    productimg=models.ImageField(upload_to='photos')

    def product_image(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.productimg.url))

    product_image.allow_tags = True

status_list=[
    ("pending",'pending'),
    ("resolve",'resolve'),
]
class productinquiry(models.Model):
    userid=models.ForeignKey(registermodel,on_delete=models.CASCADE)
    productid=models.ForeignKey(product,on_delete=models.CASCADE)
    phone=models.BigIntegerField()
    address=models.TextField()
    budget=models.IntegerField()
    quantity=models.IntegerField()
    msg=models.TextField()
    timestamp=models.TimeField(auto_now=True)
    status=models.CharField(max_length=40,choices=status_list,default="pending")

class cart(models.Model):
    userid=models.ForeignKey(registermodel,on_delete=models.CASCADE)
    productid=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalamount=models.FloatField()
    orderstatus=models.IntegerField() #1-item added , 0-item remove
    orderid=models.BigIntegerField() #0-default

# userid , finalbill , phone , address , paymode , timestamp , status , razor_pay_id
class ordermodel(models.Model):
   userid = models.ForeignKey(registermodel, on_delete=models.CASCADE)
   finaltotal = models.FloatField()
   phone = models.BigIntegerField()
   address = models.TextField()
   paymode = models.CharField(max_length=40)
   timestamp = models.DateTimeField(auto_now_add=True)
   status = models.BooleanField(default=False)
   razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
