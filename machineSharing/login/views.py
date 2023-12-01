import calendar
from collections import defaultdict
from datetime import datetime, timedelta

import requests
from _decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import SignUpForm, EditUserForm, ContributionForm
from .models import *


def send_message(message):
    url = 'http://16.171.134.101:3000/send-message'
    message_content = message

    # Create a dictionary with the message content
    payload = {'message': message_content}

    try:
        response = requests.post(url, json=payload)

        # Check the response status code
        if response.status_code == 200:
            print("Request successful!")
            print("Server response:", response.text)
        else:
            print(f"Request failed with status code {response.status_code}")
            print("Server response:", response.text)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


# Create your views here.

def landing(request):
    return render(request, 'index.html')


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            admin = Account.objects.get(name=username)
            if not admin.status:
                messages.success(request, "You have successfully signed in")
                activity_log = ActivityLog(user=request.user.username, action='Logging in',
                                           details='User Logged in into there account')
                activity_log.save()

                return redirect('dashboard')
            else:
                messages.success(request, "You have successfully signed in")
                activity_log = ActivityLog(user=request.user.username, action='Logging in',
                                           details='User Logged in into there account')
                activity_log.save()

                return redirect('dashboard')
        else:
            messages.error(request, "There was an error while signing in")
            return redirect('home')
    else:
        return render(request, 'home.html')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Information saved successfully! Welcome to AgriLeaseTech")
            activity_log = ActivityLog(user=request.user, action='Account creation',
                                       details='User created account')
            activity_log.save()

            acc_ = Account(user_id=request.user.id, name=request.user.username)
            acc_.save()
            monthly = MonthlyActivity(member=request.user.username)
            monthly.save()
            number = Account.objects.all().count() + 1

            turn = Turn(member=request.user.username, number=number)
            turn.save()

            
            admin = Account.objects.get(name=request.user.username)
            if not admin.status:
               return redirect('dashboard')
            else:
                return redirect('dashboard')


    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def forgot_password(request):
    pass
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        url = 'http://13.51.196.90:3000/trigger-function'
        payload = {'phone_number': phone}
        user_id = request.user.id
        verified = False

        # Check if the phone number is already associated with another user
        try:
            account = Account.objects.get(phone_number=phone)
            if account.user_id != user_id:
                messages.error(request,
                               'The phone number is already in use by another user. Please try another number.')
                return render(request, 'mobile.html', {'verification_code_sent': False})
        except Account.DoesNotExist:
            # If the phone number is not associated with any user, create a new account
            account = Account.objects.get(user_id=request.user.id)
            account.phone_number = phone
            account.save()

        # If the phone number is associated with the current user or not associated with any user, continue with
        # sending the verification code
        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()
            code = response.text.replace('Message successfully sent. Verification code is: ', '')

            # Store the code in the session
            request.session['verification_code'] = code

            return render(request, 'mobile.html', {'verification_code_sent': True})

        except requests.exceptions.RequestException as e:
            messages.error(request, 'Error while sending the verification code.')
            print(f"Error: {e}")
            return render(request, 'mobile.html', {'verification_code_sent': False})

    else:
        return render(request, 'mobile.html', {'verification_code_sent': False})



def dashboard(request):
    if request.method == 'POST' and request.FILES:
        user_id = request.user.id
        name = request.POST.get('name')
        type = request.POST.get('type')
        location = request.POST.get('location')
        rates = request.POST.get('rates')
        condition = request.POST.get('condition')
        image = request.FILES.get('img')
        desc = request.POST.get('desc')
        add = AddEquipment(user_id=user_id, name=name, type=type, location=location, rental_rate=rates,
                           condition=condition, img=image, Desc=desc)
        add.save()
        messages.success(request, 'Equipments Added Successfully')
        return redirect('dashboard')
    else:
        eq = AddEquipment.objects.filter(user_id=request.user.id)
        acc_ = Account.objects.get(user_id=request.user.id)
        return render(request, 'dashboard.html',
                      {'equipments': eq, 'account': acc_,})


def loans(request):
    eq = AddEquipment.objects.filter(user_id=request.user.id)
    acc_ = Account.objects.get(user_id=request.user.id)
    notification = Notification.objects.filter(username=request.user.username).order_by('-id')[:3]

    return render(request, 'loan.html',
                  {'equipments': eq, 'account': acc_, })




def logs(request):
    loan = Loan.objects.get(id=1)
    acc_ = Account.objects.get(user_id=request.user.id)
    monthly = MonthlyActivity.objects.get(member=request.user.username)
    turn = Turn.objects.get(member=request.user.username)
    applies = Apply.objects.filter(member=request.user.username).order_by('-id')
    logs = ActivityLog.objects.filter(user=request.user.username).order_by('-id')
    notification = Notification.objects.filter(username=request.user.username).order_by('-id')[:3]
    return render(request, 'activityLog.html',
                  {'loan': loan, 'account': acc_, 'monthly': monthly, 'turn': turn, 'apply': applies, 'logs': logs,
                   'notification': notification})


def logout_user(request):
    messages.success(request, "You have been logged out")
    activity_log = ActivityLog(user=request.user.username, action='Logging out',
                               details='User Logged out of there account')
    activity_log.save()
    logout(request)
    return redirect('home')


def notification(request, sender, id):
    _notify = Notification.objects.get(id=id)
    _notify.read = 1
    _notify.save()
    notify = Notification.objects.filter(sender=sender, username=request.user.username).order_by('-id')
    loan = Loan.objects.get(id=1)
    acc_ = Account.objects.get(user_id=request.user.id)
    monthly = MonthlyActivity.objects.get(member=request.user.username)
    turn = Turn.objects.get(member=request.user.username)
    applies = Apply.objects.filter(member=request.user.username).order_by('-id')
    logs = ActivityLog.objects.filter(user=request.user.username).order_by('-id')
    return render(request, 'notification.html',
                  {'loan': loan, 'account': acc_, 'monthly': monthly, 'turn': turn, 'apply': applies, 'logs': logs,
                   'notification': notify})


# admin


def delete(request, id):
    deletedEQ = AddEquipment.objects.get(id=id)
    deletedEQ.delete()
    messages.success(request, 'You have successfully deleted the equipment!')
    return redirect('dashboard')


def rent(request, id):
    deletedEQ = AddEquipment.objects.get(id=id)
    deletedEQ.available = 0 
    deletedEQ.save()
    messages.success(request, 'You have successfully rented the equipment!')
    return redirect('loans')
