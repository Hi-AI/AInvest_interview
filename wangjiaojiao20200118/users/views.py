from django.shortcuts import render
from users.models import AuthUser
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, LoginForm, PandasdataForm
import numpy as np
from django_pandas.io import read_frame

# Create your views here.



def Register(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            mobilephone = form.cleaned_data['mobilephone']
            customersource = form.cleaned_data['customersource']
            is_pay = form.cleaned_data['is_pay']
            password = form.cleaned_data['password2']

            AuthUser.objects.create_user(username=username,
                                         password=password,
                                         mobilephone=mobilephone,
                                         customersource=customersource,
                                         is_pay=is_pay)

            return HttpResponseRedirect("/accounts/login/")

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                user.login_num += 1
                user.save()
                return HttpResponseRedirect(reverse('users:profile', args=[user.id]))

            else:
                # 登陆失败
                return render(request, 'login.html', {'form': form,
                'message': 'Wrong password. Please try again.'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



def PandasData(request):
    if request.method == 'POST':
        form = PandasdataForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            df = read_frame(AuthUser.objects.all(), fieldnames=['username', 'login_num',
                                                              'is_pay', 'mobilephone',
                                                              'date_joined', 'last_login'])

            try:
                AuthUser.objects.get(username=username)
            except:
                return render(request, 'pandas_data.html', {'messageerror': 'The username does not exist'})

            df_select = df[df.username == username]

            username = df_select.username.values[0]
            login_num = df_select.login_num.values[0]
            register_time = df_select.date_joined.values[0]
            last_login = df_select.last_login.values[0]
            is_login = not np.isnat(last_login)

            register_time = str(np.datetime_as_string(register_time)).split("T")[0] + " " + \
                            str(np.datetime_as_string(register_time)).split("T")[1].split(".")[0]

            if is_login and last_login > np.datetime64('today'):
                is_today = True
            else:
                is_today = False

            if is_login:
                last_login = str(np.datetime_as_string(last_login)).split("T")[0] + " " + \
                             str(np.datetime_as_string(last_login)).split("T")[1].split(".")[0]

            message = {
                'username': username,
                'login_num': login_num,
                'register_time': register_time,
                'last_login': last_login,
                'is_login': is_login,
                'is_today': is_today
            }
            return render(request, 'pandas_data.html', {'message': message})