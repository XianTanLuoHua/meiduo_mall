from django.conf.urls import url, include
from django.contrib import admin

# from meiduo_mall.apps.users import views
from . import views

urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),

]