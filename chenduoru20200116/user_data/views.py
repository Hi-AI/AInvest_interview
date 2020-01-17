from django.shortcuts import render
from user_data.models import Client
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django_pandas.io import read_frame
import numpy as np

# Create your views here.


def register_render(request, error=None):
    if error:
        return render(request, 'register.html', {'err': error})
    else:
        return render(request, 'register.html')


def login_render(request, error=None):
    if error:
        return render(request, 'login.html', {'err': error})
    else:
        return render(request, 'login.html')


def pandas_request_render(request, res=None, error=None):
    if res:
        return render(request, 'pandas_request.html', {'res': res})
    elif error:
        return render(request, 'pandas_request.html', {'err': error})
    else:
        return render(request, 'pandas_request.html')


class Register(View):
    def get(self, request):
        return register_render(request)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        telephone = request.POST.get('telephone')
        originate = request.POST.get('originate')
        is_pay = request.POST.get('is_pay')
        if is_pay == "on":
            is_pay = True
        else:
            is_pay = False

        if not username:
            return register_render(request, "Please enter username")
        elif not password:
            return register_render(request, "Please enter password")
        elif not originate:
            return register_render(request, "Please enter originate")

        try:
            Client.objects.get(username=username) and Client.objects.get(telephone=telephone)
        except Client.DoesNotExist:
            pass
        else:
            return login_render(request, "User exist, please login")

        Client.objects.create_user(username=username, password=password, telephone=telephone,
                                          originate=originate, is_pay=is_pay)

        return login_render(request)


class Login(View):
    def get(self, request):
        return login_render(request)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username:
            return login_render(request, "Please enter username")
        elif not password:
            return login_render(request, "Please enter password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            user.login_num += 1
            user.save()
            return login_render(request, 'Login successfully')
        else:
            return login_render(request, 'Username and password does not match')


class PandasResult(View):
    def get(self, request):
        return pandas_request_render(request)

    def post(self, request):
        username = request.POST.get('username')

        df = read_frame(Client.objects.all(), fieldnames=['username', 'login_num',
                                                          'is_pay', 'telephone',
                                                          'register_time', 'last_login'])

        try:
            Client.objects.get(username=username)
        except Client.DoesNotExist:
            return pandas_request_render(request, error="User not exist")

        df_select = df[df.username == username]

        username = df_select.username.values[0]
        login_num = df_select.login_num.values[0]
        register_time = df_select.register_time.values[0]
        last_login = df_select.last_login.values[0]
        have_login = not np.isnat(last_login)

        register_time = str(np.datetime_as_string(register_time)).split("T")[0] + " " + \
                        str(np.datetime_as_string(register_time)).split("T")[1].split(".")[0]

        if have_login and last_login > np.datetime64('today'):
            is_today = True
        else:
            is_today = False

        if have_login:
            last_login = str(np.datetime_as_string(last_login)).split("T")[0] + " " + \
                         str(np.datetime_as_string(last_login)).split("T")[1].split(".")[0]

        res = {
            'username': username,
            'login_num': login_num,
            'register_time': register_time,
            'last_login': last_login,
            'have_login': have_login,
            'is_today': is_today
        }

        return pandas_request_render(request, res=res)
