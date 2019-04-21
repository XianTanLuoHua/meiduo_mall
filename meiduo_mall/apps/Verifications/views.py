import random

from django import http
from django.shortcuts import render
from meiduo_mall.libs.response_code import RET
from django_redis import get_redis_connection

# Create your views here.
from django.views import View
from django_redis import get_redis_connection
from meiduo_mall.libs.captcha.captcha import captcha

class ImgView(View):  #生成图形验证码
    def get(self,request,uuid):
        text,image = captcha.generate_captcha() #生成图片验证码

        conn = get_redis_connection('verify_code') # 得到redis数据库进行缓存  的对象
        conn.setex('img_{}'.format(uuid),300,text)
        return http.HttpResponse(content_type='image/jpg',content=image)

class smsView(View):
    def get(self,request,mobile):
        coon = get_redis_connection("verify_code")  # 得到数据库对象

        try:  #对频繁发送短信的用户进行校验
            text1 = coon.get('flag_{}'.format(mobile))
            if str(text1.decode()) == str(mobile):
                return http.JsonResponse({'code':4001,'errmsg':'短信发送频繁'})
        except:
            pass  #没有得到说明数据库内是空的

        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        if not all([mobile,uuid,image_code]): # 校验数据完整性
            return http.JsonResponse({'code':4001,'errmsg':'参数不完整'})
        print(1)
        img_text_ser = coon.get('img_{}'.format(uuid))    #  得到数据库中对应 uuid 的图形验证码的内容
        print(2)
        if img_text_ser == None:  #如果数据库中得不到图形验证吗 则不让用户进行发送操作
            return http.JsonResponse({'code':4001,'errmsg':'图形验证码已无效'})
        print(3)
        try:   #验证后立即删除数据库中的数据
            coon.delete('img_{}'.format(uuid))
        except:
            pass

        img_text_ser = img_text_ser.decode()        # 对redis数据库中保存的二进制格式数据进行解码
        if img_text_ser.lower() != image_code.lower():
            return http.JsonResponse({'code': 4001, 'errmsg': '图形验证码输入有误'})

        sms_code = random.randint(100000,999999)   #生成一个短信验证码

        #TODO 发送短信
        p = coon.pipline() #设置一个队列 将redis请求变成队列
        p.setex('sms_{}'.format(mobile),180,sms_code)  # 对刚生成的验证码进行保存 有效时间三分钟
        p.setex('flag_{0}'.format(mobile),60,mobile)       # 发送成功之后 进行标记一分钟之内不能再次发送
        p.excute() # 执行队列内的命令

        return http.JsonResponse({'code':0, 'errmsg': 'OK'})
