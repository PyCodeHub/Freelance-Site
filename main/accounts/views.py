from django.shortcuts import render , redirect
from django.urls import reverse_lazy

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)

from django.contrib.auth import authenticate , login , logout
from django.views import View

from .forms import *
from .models import OTP

from sms import send_otp

import random


# User Register Views
class UserRegisterView(View):
    template_name = 'accounts/userRegister.html'
    form_class = UserRegisterForm

    def get(self , request):
        return render(request , self.template_name , {'form':self.form_class})

    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            create_code = random.randint(1000,9999)
            send_otp(cd['phone'],create_code)
            OTP.objects.create(phone=cd['phone'] , code = create_code)
            
            request.session['page_one'] = {
                'status':cd['status'],
                'phone':cd['phone']
            }
            return redirect('veryfy')
        return render(request,self.template_name,{'form':form})
    
class UserVeryfyCodeView(View):
    template_name = 'accounts/userVeryfyCode.html'
    form_class = UserVeryfyCodeForm
    
    def get(self , request):
        return render(request, self.template_name,{'form':self.form_class})
    
    def post(self , request):
        data_sissinon = request.session['page_one']
        get_phone = OTP.objects.get(phone = data_sissinon['phone'])
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            if cd['code'] == get_phone.code:
                if data_sissinon['status'] == 'Freelancer':
                    get_phone.delete()
                    return redirect('freelancer')
                else:
                    get_phone.delete()
                    return redirect('employer')
            return redirect('veryfy')
        return render(request,self.template_name,{'form':form})

    
class EmployerRegisterView(View):
    template_name = 'accounts/employerRegister.html'
    form_class = EmployerRegisterForm

    def get(self , request):
        return render(request,self.template_name,{'form':self.template_name}) 
    
    def post(self , request):
        data_session = request.session['page_one']
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                phone = data_session['phone'],
                username = cd['username'],
                email = cd['email'],
                status = data_session['status'],
                password = cd['password']
            )
            return redirect('login')
        return render(request,self.template_name,{'form':form})
    
class FreelancerRegisterView(View):
    template_name= 'accounts/freelancerRegister.html'
    form_class = FreelancerRegisterForm

    def get(self , request):
        return render(request,self.template_name,{'form':self.form_class})

    def post(self , request):
        data_session = request.session['page_one']
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                phone = data_session['phone'],
                username = cd['username'],
                email = cd['email'],
                status = data_session['status'],
                password = cd['password'],
            )
            user.skills.set(cd['skills'])
            return redirect('login')
        return render(request,self.template_name,{'form':form})
    
# User Login Views
class UserLoginView(View):
    template_name = 'accounts/userLogin.html'
    form_class = UserLoginForm

    def get(self, request):
        return render(request,self.template_name,{'form':self.form_class})

    def post(self ,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            create_code = random.randint(1000,9999)
            send_otp(cd['phone'],create_code)
            OTP.objects.create(phone = cd['phone'] , code = create_code)
            request.session['login_info'] = {
                'phone':cd['phone'],
                'password':cd['password'],
            } 
            return redirect('login_veryfy')  
        return render(request,self.template_name,{'form':form})

class LoginVeryfyCodeView(View):
    template_name = 'accounts/loginVeryfyVode.html'
    form_class = UserLoginVeryfyCodeForm

    def get(self , request):
        return render(request,self.template_name,{'form':self.form_class})

    def post(self ,request):
        data_session = request.session['login_info']
        get_phone = OTP.objects.get(phone = data_session['phone'])
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == get_phone.code:
                user = authenticate(phone = data_session['phone'] , password = data_session['password'])
                if user is not None:
                    login(request,user)
                    get_phone.delete()
                    return redirect('home')
            return redirect('login_veryfy')
        return render(request,self.template_name,{'form':form})

# User Logout Views
class UserLogoutView(View):
    def get(self , request):
        logout(request)
        return redirect('login')


# Reset Password Accounts Views
class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('login')

    
    

    
        



        
                



    

    


    


    


            
    



            


