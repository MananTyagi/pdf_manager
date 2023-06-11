from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm ,EmailForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm 
from .models import CustomUser 
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from .jwt_token import generate_jwt_token , verify_jwt_token
from django.core import serializers
import json


def get_user_obj_id_from_memory(request):
    return request.session.get('user_obj')

def save_user_obj_id_in_memory(request, user_obj):

    request.session['user_obj'] = user_obj.id
    
def remove_user_obj_id_from_session(request):
    if 'user_obj' in request.session:
        del request.session['user_obj']
        print("user_obj removed from session")
    else:
        print("user_obj is not present in session")
        
        
        

def send_mail_for_reset( email, token):
    subject = 'Password reset link'
    message = f'Hi! click on the following link to reset password http://127.0.0.1:8000/password_reset_link/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
    

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"New account created: {user.username}")
            return redirect('/')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name = "users/register.html",
        context={"form": form}
    )
    
    
    
    
@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("homepage")

def custom_login(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("homepage")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error) 

    form = AuthenticationForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={"form": form}
        )
    
    
    
def forgot_password(request):
    print("entered_user")
    if request.method =="POST":
        print("mana")
        form = EmailForm(request.POST)

        print("password")
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                user=CustomUser.objects.get(email=email)
                auth_token= generate_jwt_token(user.username)
                user.token= str(auth_token)
                user.save()
                send_mail_for_reset(email, auth_token)
                messages.success(request, "A unique URL has been sent to given Email ID to reset password.Please dont share with anyone")
                return redirect("homepage")
                
            except Exception as e:
                print("Error")
                print(e)
                messages.error(request, "The email you entered does not exist.Please enter a valid email address associted with account")
                return redirect("forgotpassword")
        else:
            return redirect("forgotpassword")
            
    else:
        print("else")
        form = EmailForm()   
    return render(request=request, template_name="users/forgot_password.html", context={'form': form} )

def password_reset_link(request, token):
    if request.method == "POST":
        form=PasswordResetForm(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data["password1"]
            user_obj_id=get_user_obj_id_from_memory(request)
            user_obj=CustomUser.objects.get(id=user_obj_id)
            user_obj.set_password(password)
            user_obj.token=None
            user_obj.save()
            remove_user_obj_id_from_session(request)
            messages.success(request, "password has been changed successfully,please login now with your new password")
            return redirect("login")
            
    else:
        try:
            user_name=verify_jwt_token(token)
            user_obj=CustomUser.objects.get(username=user_name)
            if user_obj is None:
                return JsonResponse({"messaage":"Bad request"},status=404)
            else:
                print("come till here")
                form=PasswordResetForm()
                save_user_obj_id_in_memory(request, user_obj)
                return render(request=request, template_name="users/reset_password.html" , context={'form': form} )
        except Exception as e:
            print(e)
            return JsonResponse({"messaage":"Bad request"},status=404)

            

    

            

