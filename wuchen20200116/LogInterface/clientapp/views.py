from datetime import time, datetime

import pymysql
import pandas as pd
from django.contrib import auth

from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth.decorators import login_required

# Create your views here.
from clientapp.models import Log, AuthUser


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            # 更新最后一次登录时间
            auth.login(request, user)
            # 将登录信息保存到 log 表中
            time  = datetime.now().strftime('%Y%m%d%H%M%S')
            log = Log.objects.create(client=username,time=time)
            log.save()

            return redirect('/index/')
        else:
            return render(request, 'login.html', {'errormsg': '用户名或密码错'})
    return render(request, 'login.html')


@login_required
def index(request):
    return render(request, 'index.html', {'user': request.user.username})


def logout(request):
    auth.logout(request)
    return redirect('/login/')

#获取客户登录信息
def getInfo(request):
    if request.method=='GET':
        return render(request, 'getinfo.html')
    else:
        client_name = request.POST.get('client','')
        conn = pymysql.connect('localhost', 'root', 'root', 'django_auth')
        df = pd.read_sql('select * from log', conn)
        #统计登录次数
        login_count = df[df['client']==client_name].shape[0]
        #判断该用户今天是否登陆过
        if client_name!='':
            auth = AuthUser.objects.filter(username=client_name)[0]
            print(auth.last_login)
            if df[df['client'] == 'admin3']['time'].str.contains(datetime.now().strftime('%Y%m%d')).iloc[0]:
                flag = 1
            else:
                flag = 0
            return render(request, 'getinfo.html', {'login_count':login_count,'flag':flag,'client':client_name,'auth':auth})
        return render(request, 'getinfo.html', {'msg':'未输入查询姓名'})
