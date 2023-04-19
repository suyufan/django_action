from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from utils.tencent.msg import send_message
import re
from api import models
import uuid
from api.serializer.account import MessageSerializer,LoginSerializer

class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        """
        1. 校验手机号是否合法
        2. 校验验证码，redis
            - 无验证码
            - 有验证码，输入错误
            - 有验证码，成功

        4. 将一些信息返回给小程序
        """
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'status': False,'message': '验证码错误'})
        phone = ser.validated_data.get('phone')

        user_object,flag = models.UserInfo.objects.get_or_create(phone=phone)
        user_object.token = str(uuid.uuid4())
        user_object.save()

        return Response({'status': True,"data":{"token":user_object.token,"phone":phone}})

class MessageView(APIView):
    def get(self,request,*args,**kwargs):
        # 1.获取手机号
        # 2.手机号格式校验
        ser = MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({'status':False,'message':'手机号格式错误'})
        phone = ser.validated_data.get('phone')
        print("手机号：", phone)
        # phone = request.query_params.get('phone')

        # 3.生成随机验证码
        import random
        random_code = random.randint(1000,9999)
        print("验证码：",random_code)
        # 4.验证码发送到手机,购买服务器进行短息发送：腾讯云
        # result = send_message(phone, random_code)
        # if not result:
        #     return Response({"status": False, "message": '短信发送失败'})

        # 5.将验证码+手机号保留（30s过期）
        #   5.1 搭建redis服务器（云redis)
        #   5.2 django中方便使用redis的模块 django-redis
        #       配置 settings
        from django_redis import get_redis_connection
        conn = get_redis_connection()
        conn.set(phone,random_code,ex=60)
        return Response({"status": True,'message':'发送成功',"data":{"phone":phone,"code":random_code}})
