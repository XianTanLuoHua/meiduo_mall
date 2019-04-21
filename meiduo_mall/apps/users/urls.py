from django.conf.urls import url, include
from django.contrib import admin

# from meiduo_mall.apps.users import views   # 不能这样导入!!因为我们在dev文件中已经定义了搜索路径为apps下面了
from . import views

urlpatterns = [
    url(r'^register/$',views.RegisterView.as_view(),name='register'),
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',views.UserView.as_view(),name='username'),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$',views.mobileView.as_view(),name='mobile'),



]