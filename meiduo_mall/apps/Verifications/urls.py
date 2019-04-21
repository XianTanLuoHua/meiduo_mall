from django.conf.urls import url, include
from django.contrib import admin

# from meiduo_mall.apps.users import views
from . import views

urlpatterns = [
    url(r'^image_codes/(?P<uuid>[\w-]+)/$',views.ImgView.as_view()),
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.smsView.as_view(), name='smsView'),
]