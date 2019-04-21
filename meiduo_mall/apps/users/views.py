import re

from django import http
from django.contrib.auth import login
from django.shortcuts import render
from django_redis import get_redis_connection
# Create your views here.
from django.urls import reverse

from django.views import View
from .models import User



class RegisterView(View):
    def get(self,request):
        return render(request,'register_vue.html')



    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2= request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code = request.POST.get('sms_code')
        allow = request.POST.get('allow')


        # print(username,password,password2,mobile,sms_code,allow)

        if not all([username,password2,password,mobile,sms_code]): #参数校验,如果参数不全则
            return render(request,'register_vue.html',{'register_errmsg':'参数输入不完整,请重新注册!'})
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            return http.HttpResponseForbidden('用户名输入有误')
        if not re.match(r'^[0-9A-Za-z]{8,20}$',password):
            return http.HttpResponseForbidden('密码输入有误')
        if password != password2:
            return http.HttpResponseForbidden('两次输入密码不一样')
        if not re.match(r'^1[345789]\d{9}$',mobile):
            return http.HttpResponseForbidden('手机号输入有误')
        if allow != 'on':
            return http.HttpResponseForbidden('请阅读用户协议')


        coon = get_redis_connection("verify_code")
        cli_mobile = coon.get('sms_{}'.format(mobile)).decode # 取出数据库中根据手机号存放的验证码

        if sms_code != cli_mobile:
            coon.delete('sms_{}'.format(mobile))
            return render(request,'register_vue.html', {'sms_code_errmsg': '输入短信验证码有误'})


        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except:
            return render(request,'register_vue.html',{'register_errmsg':'注册失败'})
        login(request,user) #设置状态保持
        return http.HttpResponseRedirect(reverse('contents:index')) #注册完毕用户重定向首页







class UserView(View): # 用户名 重复 校验
    def get(self,request,username):
        count_username = User.objects.filter(username=username).count()  #统计数据库中是否存在该用户名
        return http.JsonResponse({'code':'OK','errmsg':'成功','count':count_username})

class mobileView(View): # 手机号 重复 校验
    def get(self,request,mobile):
        count_mobile = User.objects.filter(mobile=mobile).count()  #统计数据库中是否存在该用户名
        return http.JsonResponse({'code':'OK','errmsg':'成功','count':count_mobile})


