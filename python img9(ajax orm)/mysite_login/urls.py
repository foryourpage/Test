"""mysite_login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from login import views
from django.conf.urls import url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^captcha', include('captcha.urls')),
    url(r'^book', views.book, name='book'),
    # 前面是路径,后面是方法
    url(r'^getdata', views.getdata),
    url(r'^img1', views.img1),
    url(r'^home', views.home),
    url(r'^img2', views.img2),
    url(r'^img3', views.img3),
    url(r'^all_table', views.all_table),
    url(r'^add_article', views.add_article),
    url(r'^delete_article', views.delete_article),
    url(r'^upload', views.upload),
    url(r'^all_form', views.all_form),
    url(r'^delete_test', views.delete_test),
    url(r'^img4', views.img4),
    url(r'^statistics', views.statistics),
    url(r'^img5', views.img5),
    url(r'^img6', views.img6),
    url(r'^percentage', views.percentage),
    url(r'^img7', views.img7),
    url(r'^img8', views.img8),
    url(r'^img9', views.img9),
    url(r'^imh', views.imh),
    url(r'^imj', views.imj),
    url(r'^imk', views.imk),
    url(r'imm', views.imm),
    url(r'^imn', views.imn),
    url(r'^imo', views.imo),
    url(r'^imp', views.imp),
    url(r'^imq', views.imq),
    url(r'^imr', views.imr),
    url(r'^ims', views.ims)

]
