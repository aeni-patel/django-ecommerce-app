"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from myapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("register",views.register),
    path("login",views.login),
    path("",views.showproducts),
    path("singleproducts/<int:id>",views.singleproducts),
    path("fetchdata",views.fetchdata),
    path("catchdata",views.catchdata),
    path("logout",views.logout),
    path("addproduct",views.addproduct),
    path("fetchproduct",views.fetchproduct),
    path("Manageproducts",views.Manageproducts),
    path("deleteproduct/<int:id>",views.deleteproduct),
    path("edit/<int:id>",views.edit),
    path("updateproductdata",views.updateproductdata),
    path("manageinsertproduct",views.manageinsertproduct),
    path("showcategory/<int:id>",views.showcategory),
    path("inquiry/<int:id>",views.inquiry),
    path('submitinquiry',views.submitinquiry),
    path('insertintocart/',views.insertintocart),
    path('showcart',views.showcart),
    path('removeitem/<int:id>',views.removeitem),
    path("decrease/<int:id>", views.decrease),
    path("increase/<int:id>", views.increase),
    path("placeorder",views.placeorder),
    path('payment-success', views.payment_success),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
