from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404, HttpResponseRedirect,HttpResponse
from rest_framework.viewsets import ModelViewSet
from user.serializers import *  
from user.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.views.generic import View
from django_pandas.io import read_frame
# Create your views here.
class User_Api(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
class pandas_Api(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PSerializer
def index(request):
    return render(request, 'index.html') 

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        '''登录校验'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg':'数据不完整'})
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user.login_times+=1
            user.save()
            next_url = request.GET.get('next', reverse('user:index'))

            # 跳转到next_url
            response = redirect(next_url) # HttpResponseRedirect
            return response
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg':'用户名或密码错误'})
class LogoutView(View):
    '''退出登录'''
    def get(self, request):
        '''退出登录'''
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('universitylist:index'))


class RegisterView(View):
    '''注册'''
    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html') 

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
      
        if not all([username,password]):
            return render(request,'register.html',{'errmsg':"数据不完整！"})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request,'register.html',{'errmsg':'''用户名已经存在，请直接<a href="/user/login/"  style="margin-top:8px" id="register-button">登录</a>或者更换用户名重新注册'''})
        user = User.objects.create_user(username,"not@email.com", password)
        user.is_active = 1
        user.save()
        return render(request,'login.html')

