from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import LoginForm, RegisterForm, CheckForm
from django.contrib.auth import  login, authenticate
import ghasedakpack
from random import randint
from uuid import uuid4
from .models import Otp, User
from django.utils.crypto import get_random_string

SMS = ghasedakpack.Ghasedak('b20b10b9913ea0b44dfa530b5169b9c0a4d26930c081205ef3e45b51c6609a86')




class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error('phone', 'Invalid user data')

        else:
            form.add_error('phone', 'Invalid user data')

        return render(request, 'account/login.html', {'form': form})



class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            shahabcode = randint(1000, 9999)
            SMS.verification(
                {'receptor': cd["phone"], 'type': '1', 'template': 'shahabcode', 'param1': shahabcode})
            Otp.objects.create(phone=cd["phone"], code=shahabcode)
            print(shahabcode)
            return redirect(reverse('account:checkotp') + f'?phone={cd["phone"]}')



        else:
            form.add_error('phone', 'Invalid user data')

        return render(request, 'account/register.html', {'form': form})




class CheckView(View):
    def get(self, request):
        form = CheckForm()
        return render(request, 'account/check_otp.html', {'form': form})

    def post(self, request):
        phone = request.GET.get('phone')
        form = CheckForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(phone=phone, code=cd["code"]).exists():
                user = User.objects.create_user(phone=phone)

                login(request, user)
                return redirect('home:home')



        else:
            form.add_error('phone', 'Invalid user data')

        return render(request, 'account/check_otp.html', {'form': form})

