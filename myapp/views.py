import razorpay
from django.contrib.auth import user_logged_in
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.template.loader import render_to_string

from myproject import settings
from .models import *
from django.contrib import messages
from django.conf import settings

def register(request):
    return render(request,"register.html")

def login(request):
    return render(request,"login.html")

def showproducts(request):
    fetchdata=product.objects.all()
    fetchcatdata=category.objects.all()
    # Pagination
    paginator = Paginator(fetchdata, 6)  # Show 10 products per page
    page_number = request.GET.get('page')  # Get the page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the page object

    context = {
        "data": page_obj,  # Pass the page object to the template
        "paginator": paginator,
        'catdata':fetchcatdata# Optional: pass the paginator for additional info
    }
    return render(request,"showproducts.html",context)

def singleproducts(request,id):
    fetchdata=product.objects.get(id=id)
    fetchproductimage=productimage.objects.filter(productid=id)
    context={
        'data':fetchdata,
        'images':fetchproductimage 
    }
    return render(request,"singleproducts.html",context)

def fetchdata(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    phone=request.POST.get('phone')
    address=request.POST.get('address')
    password=request.POST.get('password')
    gender=request.POST.get('gender')
    role=request.POST.get('role')
    profilepicture=request.FILES['dp']
    # check email in database
    # if available ==> account already exists , please login now
    # else ==> insert query into model , show successs message
    if registermodel.objects.filter(email=email, phone=phone).exists():
        # Email already exists
        messages.error(request, "Account already exists, please login now.")
        return render(request, "login.html")
    else:
        # Email does not exist, create a new user
        registermodel.objects.all()


    insertquery=registermodel(name=name,email=email,phone=phone,address=address,password=password,gender=gender,role=role,profilepicture=profilepicture)
    insertquery.save()
    messages.success(request,"Register successfully")
    return render(request,"login.html")

def catchdata(request):
    useremail=request.POST.get("email")
    userpassword=request.POST.get("password")


    try:
        #userdata=registermodel.objects.get(email=useremail,password=userpassword)
        #print(userdata)
        if '@' in useremail:  # Simple check to see if it's an email
            userdata = registermodel.objects.get(email=useremail, password=userpassword)
        else:  # Otherwise, treat it as a phone number
            userdata = registermodel.objects.get(phone=useremail, password=userpassword)
        print(userdata)
        #session
        request.session["log_id"]=userdata.id
        request.session["log_name"]=userdata.name
        request.session["log_email"]=userdata.email
        request.session["log_role"]=userdata.role


        print("session name:",request.session["log_name"])
        return redirect("/")

    except:
        messages.error(request, "Invalid credential")
        return render(request, "login.html")
       # print("failure")
       # userdata=None

    #if userdata is not None:
      #  return redirect("/showproducts")
    #else:


def logout(request):
    try:
        del request.session["log_id"]
        del request.session["log_name"]
        del request.session["log_email"]
        del request.session["log_role"]
    except:
        pass
    return redirect("/")

def addproduct(request):
    fetchcatdata = category.objects.all()
    context = {
        "catdata": fetchcatdata
    }
    fetchproduct=product.objects.all()
    print(fetchproduct)
    # try:
    #     request.session["log_id"] = fetchproduct.id
    #     request.session["log_name"] = fetchproduct.name
    #     request.session["log_email"] = fetchproduct.email
    #     print("session name:", request.session["log_name"])
    # except:
    #     print("failure")


    return render(request,"addproduct.html",context)

def fetchproduct(request):
    productname=request.POST.get('productname')
    catid=request.POST.get('pcat')
    productimage=request.FILES["img"]
    productprice=request.POST.get('price')
    description=request.POST.get('desc')
    status=request.POST.get('status')


    insertquery=product(product_name=productname,catid=category(id=catid),product_image=productimage,price=productprice,description=description,status=status,seller=registermodel(id=request.session["log_id"]))
    insertquery.save()
    messages.success(request,"Product added Sucessfully!!")
    return redirect("/addproduct")

def Manageproducts(request):
    seller_loggedin = request.session['log_id']
    fetchdata = product.objects.filter(seller=seller_loggedin)
    context={
        'data':fetchdata

    }
    return render(request,"Manageproducts.html",context)

def deleteproduct(request,id):
    product.objects.get(id=id).delete()
    messages.success(request,"Item Deleted")
    redirect('/Manageproducts')

def edit(request, id):
    print(id)
    fetchcategory = category.objects.all()
    fetchdata=product.objects.get(id=id)
    context={
        "data":fetchdata,
        "category":fetchcategory
        }
    return render(request,"edit.html",context)

def updateproductdata(request):
    pname=request.POST.get("pname")
    price = request.POST.get("pprice")
    desc = request.POST.get("pdesc")
    catid = request.POST.get("pcat")
    pid = request.POST.get("pid")


    fetchdata=product.objects.get(id=pid)
    fetchdata.product_name=pname
    fetchdata.price=price
    fetchdata.description=desc
    fetchdata.catid=category(id=catid)
    if 'profilepic' in request.FILES:
            fetchdata.product_image=request.FILES['profilepic']

    # fetchdata.pic_photo = img
    fetchdata.save()
    print("updated successfully!")
    return redirect("/Manageproducts")

def manageinsertproduct(request):
    productid = request.POST.get('productid')
    pimage = request.FILES['pimage']
    insertquery = productimage( productid=product(id=productid),productimg=pimage)
    messages.success(request, "Add Image successfully!")
    insertquery.save()

    return render(request,"showproducts.html")

def showcategory(request,id):
    fetchcatdata=category.objects.all()
    fetchdata=product.objects.filter(catid=id)

    context={
        'data':fetchdata,
        'catdata':fetchcatdata

    }

    return render(request,"showcategory.html",context)

def inquiry(request,id):
    fetchdata=product.objects.get(id=id)
    context={
        'pid':id,
        'data':fetchdata
    }
    return render(request,"inquiry.html",context)

def submitinquiry(request):
    userid=request.session["log_id"]
    pid=request.POST.get("pid")
    phone=request.POST.get("phone")
    address=request.POST.get("address")
    budget=request.POST.get("budget")
    quantity=request.POST.get("quantity")
    msg=request.POST.get("msg")

    # Save data
    storedata = productinquiry(
        userid=registermodel(id=userid),
        productid=product(id=pid),
        phone=phone,
        address=address,
        budget=budget,
        quantity=quantity,
        msg=msg,
    )
    storedata.save()
    messages.success(request, "Inquiry Generated")
    return render(request, "inquiry.html")

def insertintocart(request):
    if "log_id" not in request.session:
        messages.error(request, "please login to add items in cart")
        return redirect("/login")
    userid=request.session["log_id"]
    quantity=request.POST.get("quantity")
    pid=request.POST.get("pid")
    price=request.POST.get("price")
    totalamount=int(quantity)*float(price)

    try:
        fetchdata = cart.objects.get(
    userid=userid,
    productid=pid,
    orderstatus=1
)


    except:
        fetchdata=None

    if fetchdata is not None:
        fetchdata.quantity +=int(quantity)
        fetchdata.totalamount +=float(totalamount)
        fetchdata.save()
        messages.success(request, "Item Updated in Cart")
        return redirect("/")
    else:
        storedata=cart(userid=registermodel(id=userid),productid=product(id=pid),quantity=quantity,totalamount=totalamount,orderid=0,orderstatus=1)
        storedata.save()
        messages.success(request,"Item added to cart")
        return redirect("/")

def showcart(request):
    userid=request.session["log_id"]
    fetchdata=cart.objects.filter(userid=userid,orderstatus=1)
    total = sum(item.totalamount for item in fetchdata)
    context={
        'data':fetchdata,
        "total": total
    }
    return render(request,"cart.html",context)

def removeitem(request,id):
    cart.objects.get(id=id).delete()
    messages.success(request,"Item Deleted")
    return redirect('/showcart')

def increase(request,id):
    fetchdata=cart.objects.get(id=id)
    fetchdata.quantity+=1
    fetchdata.totalamount +=fetchdata.productid.price
    fetchdata.save()
    return redirect("/showcart")

def decrease(request,id):
    fetchdata = cart.objects.get(id=id)
    if fetchdata.quantity == 1:
        fetchdata.delete()
    else:
        fetchdata.quantity-=1
        fetchdata.totalamount-=fetchdata.productid.price
        fetchdata.save()
    return redirect("/showcart")

def send_order_confirmation_email(user, product_list, address, phone, paymode, total):
    user_email = user.email

    email_message = render_to_string('email_of_payment.html', {
        'username': user.name,
        'address': address,
        'phone': phone,
        'payment': paymode,
        'total': total,
        'product': product_list,
    })

    subject = 'Order Confirmation'
    recipient_list = [user_email]

    send_mail(
        subject,
        'This is a fallback message if HTML is not supported.',
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
        html_message=email_message
    )


def placeorder(request):
    userid = request.session["log_id"]
    finaltotal = request.POST.get("total")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    paymode = request.POST.get("payment")

    user = registermodel.objects.get(id=userid)

    if paymode == "Cash on Delivery":
        # Save the order details to the database
        storedata = ordermodel(
            userid=user,
            finaltotal=finaltotal,
            phone=phone,
            address=address,
            paymode=paymode,
            status=True
        )
        storedata.save()

        lastid = storedata.id
        product_list = []
        fetchdata = cart.objects.filter(userid=userid, orderstatus=1)

        # Prepare product list for email and update cart items
        for i in fetchdata:
            product_list.append({
                'name': i.productid.product_name,
                'quantity': i.quantity,
                'price': i.totalamount
            })
            i.orderstatus = 0
            i.orderid = lastid
            i.save()

        # Send the order confirmation email
        send_order_confirmation_email(user, product_list, address, phone, paymode, finaltotal)

        messages.success(request, "Order Placed")
        return redirect("/")

    else:
        # Razorpay Payment Integration
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        order_amount = int(float(finaltotal) * 100)  # Razorpay needs amount in paise
        razorpay_order = client.order.create({
            "amount": order_amount,
            "currency": "INR",
            "receipt": f"order_rcptid_{userid}",
            "payment_capture": "1",
        })

        storedata = ordermodel(
            userid=user,
            finaltotal=finaltotal,
            phone=phone,
            address=address,
            paymode="Online",
            status=True,
            razorpay_order_id=razorpay_order['id'],
        )
        storedata.save()

        lastid = storedata.id

        # Update Cart Items
        cart_items = cart.objects.filter(userid=userid, orderstatus=1)
        product_list = []
        for item in cart_items:
            product_list.append({
                'name': item.productid.product_name,
                'quantity': item.quantity,
                'price': item.totalamount
            })
            item.orderstatus = 0
            item.orderid = lastid
            item.save()

        send_order_confirmation_email(user, product_list, address, phone, paymode, finaltotal)
        return render(request, "payment.html", {
            "razorpay_order_id": razorpay_order['id'],
            "amount": order_amount,
            "key": settings.RAZORPAY_KEY_ID,
            "currency": "INR",
        })

        return redirect("/")

def payment_success(request):
    return redirect("/")