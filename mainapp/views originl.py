import pytz
import secrets
from datetime import date, time
from django.utils import timezone
from django.utils.timezone import timedelta
from django.db.models.functions import Cast, TruncDate
from django.db.models import DateField, TimeField, CharField, Value
import string
import sys
import math
from .tasks import *
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.contrib import auth, messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
import json
import urllib.request
from .models import *
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import redirect
from django.db import connection
import re
import phonenumbers
from .enanddc import encrypt, decrypt
import pycountry
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
from googleapiclient.discovery import build
from django.core.exceptions import ObjectDoesNotExist
import hashlib
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import logging
from email.mime.image import MIMEImage
import os
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib import messages
from datetime import datetime
from .enanddc import encrypt, decrypt
from .p import *
import requests
from numerize import numerize
from django.urls import reverse
from collections import Counter
import itertools
from django.contrib.sessions.models import Session
from Admin.models import *
from Creator.models import *
from emil_send.views import existing_user,new_user


# For Fetching clientip request location


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    port = request.META['SERVER_PORT']
    # sys.stdout = open("ip.txt", "a")
    print("IP", ip, port)
    return ip+"-"+port


def get_location(request):
    ip_address = get_client_ip(request)
    # sys.stdout = open("country.txt", "a")
    ip = ip_address.split("-")[0]
    # for Iv6 Address
    if ':' in ip:
        print("ip_Address", ip_address)
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            print("Data", data)
            country_code = data["country"]
            country = pycountry.countries.get(alpha_2=country_code)
            # print(f"Country name: {country.name}")
            return country.name
    else:
        # For IpV4
        response = requests.get(
            'https://get.geojs.io/v1/ip/geo/'+ip+'.json').json()
        print("data1", response)
        country = response.get('country')
        # print("country", country)
        return country


def convert_utc_to_current_timezone(time1, timezone):
    # convert string to time object
    utc_time = datetime.strptime(str(time1), '%H:%M:%S.%f').time()
    # create datetime object with today's date
    utc_datetime = datetime.combine(datetime.now().date(), utc_time)
    utc_timezone = pytz.timezone('UTC')  # define UTC timezone
    local_timezone = pytz.timezone(timezone)  # define your local timezone
    local_datetime = utc_timezone.localize(utc_datetime).astimezone(
        local_timezone)  # convert UTC datetime to local datetime
    return local_datetime.time()


def get_timezone(request):
    ip_address = get_client_ip(request)
    # sys.stdout = open("country.txt", "a")
    ip = ip_address.split("-")[0]
    # for Iv6 Address
    if ':' in ip:
        print("ip_Address", ip_address)
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            print("Data", data)
            zone = data["timezone"]
            return zone
    else:
        # For IpV4
        response = requests.get(
            'https://get.geojs.io/v1/ip/geo/'+ip+'.json').json()
        print("data1", response)
        zone = response.get('timezone')
        return zone


# For Fetching Followers from Instagram
URL = "https://www.instagram.com/{}/"


def parse_data(s):
    data = {}
    s = s.split("-")[0]
    s = s.split(" ")
    data['Followers'] = s[0]
    data['Following'] = s[2]
    data['Posts'] = s[4]
    return data


def scrape_data(username):
    sys.stdout = open("intsgram.txt", "a")
    r = requests.get(URL.format(username))
    print("r", r)
    s = BeautifulSoup(r.text, "html.parser")
    print("s", s)
    meta = s.find("meta", property="og:description")
    print("meta", meta)
    return parse_data(meta.attrs['content'])

# #Calling Function for fetching followers
# username = "navirawat28"
# data = scrape_data(username)
# print(data)


'''For Fetching Youtube Channel Details'''

youtube = build('youtube', 'v3',
                developerKey='AIzaSyAvwCEAjlBmrJCaot4IJvc8rSkIcZ05tHk')


def fetchytdetails(channelid, id, platformid):
    ch_request = youtube.channels().list(
        part='statistics',
        id=channelid)

    ch_response = ch_request.execute()

    sub = ch_response['items'][0]['statistics']['subscriberCount']
    vid = ch_response['items'][0]['statistics']['videoCount']
    views = ch_response['items'][0]['statistics']['viewCount']

    print("Total Subscriber:- ", sub)
    print("Total Number of Videos:- ", vid)
    print("Total Views:- ", views)
    pd = PlatformDetails.objects.filter(usersid=id, platformtype=platformid)
    if pd.exists():
        pd = pd[0]
        pd.subscribers_followers = sub
        pd.allviews = views
        pd.save(update_fields=['subscribers_followers', 'allviews'])
        print("function execute")

# for fetching youtube users deatils

# fetchytdetails('UCDvw21Bag-KLYmA6kfEEHWg')

# Youtube Function end


'''For fetching details from tiktok users'''

# \myproject

# def titikusersdet(user,id,platformid):
#     options = Options()
#     options.add_argument('--headless')

#     options.add_argument('--disable-gpu')

#     driver = webdriver.Chrome(
#         ChromeDriverManager().install(), chrome_options=options)
#     username = user
#     link = (f"https://www.tiktok.com/@{username}")
#     driver.get("" + link)
#     time.sleep(2)

#     Followers = driver.find_element(
#         by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div/div[1]/h2[1]/div[2]/strong').text
#     Following = driver.find_element(
#         by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div/div[1]/h2[1]/div[1]/strong').text
#     Likes = driver.find_element(
#         by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div/div[1]/h2[1]/div[3]/strong').text

#     print(Followers)
#     print(Following)
#     print(Likes)
#     pd=PlatformDetails.objects.filter(usersid=id,platformtype=platformid)
#     if pd.exists():
#         pd=pd[0]
#         pd.subscribers_followers=Followers
#         pd.save(update_fields=['subscribers_followers'])
#         print("function execute")


# For calling Tiktok Users details
# titikusersdet("khaby.lame")


# For Verify, email is correct.

def verify_email(s):
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, s):
        return True
    return False

# for validating the username


# def valid_username(username):
#     reason = False
#     if username.isnumeric():
#         return reason
#     if not any(x for x in username):
#         return reason
#     return True


def changetimeaccording_to_country(time, country):
    time_str = time
    original_tz = pytz.timezone('Asia/Kolkata')

    # set the target timezone based on the country
    target_country = country
    iso_code = pycountry.countries.get(name=target_country).alpha_2

    target_tz = pytz.country_timezones.get(iso_code)[0]

    # create a datetime object with the original time and timezone
    original_time = datetime.strptime(time_str, '%H:%M:%S.%f')
    original_time = original_tz.localize(original_time)

    # convert the original time to the target timezone
    target_time = str(original_time.astimezone(pytz.timezone(target_tz)))
    time_obj = datetime.fromisoformat(target_time)

# get the time with AM/PM format
    time_str1 = time_obj.strftime('%I:%M:%S %p')

    print(f'Original Time: {time_str}')
    print(f'{target_country} Time: {time_str1}')
    return time_str1


def next30days():
    current_date = datetime.now().date()

    next_date = current_date + timedelta(days=30)

    # create an empty list to store the next 30 dates
    next_30_dates = []

    # loop 30 times to generate the next 30 dates
    for i in range(30):
        # calculate the next date by adding one day to the previous date
        next_date = next_date + timedelta(days=1)

        # append the next date to the list
        next_30_dates.append(next_date)

    return next_30_dates


def Login(request, infoname=None):
    if infoname is None:
        infoname = ""
    path = request.path
    if (request.method == "POST"):
        ip_add = get_client_ip(request)
        # ip_add="India"
        print("ip", ip_add)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        username = request.POST.get("username")
        passw = request.POST.get("password")
        user = auth.authenticate(username=username, password=passw)
        print("user", user)
        if result['success']:
            if (user is not None):
                auth.login(request, user)
                ln = LoginIP(userid=user.id, username=username, IP_Address=ip_add, location=get_location(
                    request), sessionkey=request.session.session_key, device=request.META.get('HTTP_USER_AGENT', ''))
                ln.save()
                if user.is_superuser == True:
                    messages.success(request, 'Login sucessfully!..')
                    print("admin login")
                    return HttpResponseRedirect("/admin/")
                permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
                    userid=user.id).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
                print("Permission name", permissionname)
                if user.is_active == True and permissionname == 'influencer_permission':
                    if path == '/Service/login/'+infoname+'/':
                        return HttpResponseRedirect("/influencer/"+infoname+"/")
                    else:
                        return HttpResponseRedirect("/")
                if user.is_active == True and permissionname == 'client_permission':
                    if path == '/Service/login/'+infoname+'/':
                        return HttpResponseRedirect("/influencer/"+infoname+"/")
                    else:
                        return HttpResponseRedirect("/")
                if user.is_active == True and permissionname == 'account_permission':
                    print("acount User lgoin")
                    return HttpResponseRedirect("/Account-Dashboard/")
                if user.is_active == True and permissionname == 'admin_permission':
                    print("admin User lgoin")
                    return HttpResponseRedirect("/Admin-Dashboard/")

                # elif ay.exists() and pr.adsagency_permission == True:
                #     # return HttpResponseRedirect("/")

                # # Enter the manager admin path
                # elif user.Role_Type == "Manager" and pr.Manager_permission == True:
                #     return HttpResponseRedirect("/index2/")

                # # Enter the Relationship Manager admin path
                # elif user.Role_Type == "Relationship Manager" and pr.RM_permission == True:
                #     # return HttpResponseRedirect("/")

                # # Enter the Accountant admin path
                # elif user.Role_Type == "Accountant" and pr.Account_permission == True:
                #     # return HttpResponseRedirect("/")

                # # Enter the KYC admin path
                # elif user.Role_Type == "KYC Manager" and pr.KycManager_permission == True:
                #     # return HttpResponseRedirect("/")

                # # Enter the  admin path
                # elif user.Role_Type == "Admin" and pr.Admin_permission == True:
                #     # return HttpResponseRedirect("/")

                # # Enter the  Super admin path
                # elif user.Role_Type == "Super Admin" and pr.Superadmin_permission == True:
                #     # return HttpResponseRedirect("/")
                else:
                    # messages.warning(
                    #     request, 'Username or Password is Incorrect')
                    return HttpResponseRedirect("/")
            else:
                messages.warning(request, 'User does not exists.')
        else:
            messages.warning(request,
                             'Invalid reCAPTCHA. Please try again.')
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    ban = PageBanner.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    return render(request, "Normal-User/login.html", {"footer": fot, "message": 'Login sucessfully!..', 'ban': ban,"Seo1": seo,"Seo":seo1,})


def Register(request):
    
    
    
    
    
    
    
    
    if (request.method == "POST"):
        sys.stdout = open("terminal_out.txt", "a")
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if result['success']:
            email = request.POST.get("email")
            username = request.POST.get("username")
            print("email", verify_email(email))
            
            sys.stdout.close()
            if verify_email(email) == True and len(username) > 0 :
                try:
                    actype = request.POST.get("actype")
                    pward = request.POST.get('password')
                    sys.stdout = open("terminal_out2.txt", "a")
                    print("fsdg", actype)
                    cursor = connection.cursor()
                    hashpass = make_password(pward)
                    cursor.execute('call userscreation(%s,%s,%s,%s,%s)',
                                   (username, hashpass, email, actype, 0))
                    user = cursor.fetchall()[0][0]
                    print("Response")
                    print(user)
                    sys.stdout.close()
                    sys.stdout = open("terminal_out3.txt", "a")
                    print("ander")
                    user = Allusers.objects.filter(id=user)
                    user = user[0]
                    print("user", user)
                    usnam = user.username
                    sys.stdout.close()
                    sys.stdout = open("terminal_out4.txt", "a")
                    link = 'https://www.influencerhiring.com/activate/' + \
                        urlsafe_base64_encode(force_bytes(
                            user.id))+'/'+account_activation_token.make_token(user)+'/'
                    # html_con = render_to_string(
                    #     "Influencer-Admin/verify.html", {'link': link, 'user': usnam}, request=request)
                    # text = strip_tags(html_con)

                    # print("Content", text)
                    # print(email)
                    # sys.stdout.close()
                    # data = {
                    #     'subject': 'Activate Your Account By Confirming Your Mail ID:',
                    #     'body': text,
                    #     'to_email': email
                    # }
                    # mwg = EmailMultiAlternatives(
                    #     subject=data['subject'],
                    #     body=data['body'],
                    #     from_email='admin@influencerhiring.com',
                    #     to=[data['to_email']]
                    # )
                    # mwg.attach_alternative(html_con, "text/html")
                    # # img_dir=r'C:\Users\BOL7\Desktop\Influencer\mainapp\static'
                    # img_dir = str(settings.BASE_DIR)+'\mainapp\static'
                    # img_dir = r'{}'.format(img_dir)
                    # image = "influencerhiring.png"
                    # file_path = os.path.join(img_dir, image)
                    # with open(file_path, 'rb') as f:
                    #     img = MIMEImage(f.read())
                    #     img.add_header(
                    #         'Content-ID', '<{name}>'.format(name=image))
                    #     img.add_header('Content-Disposition',
                    #                    'inline', filename=image)
                    # mwg.attach(img)

                    # image1 = "welcome.png"
                    # file_path = os.path.join(img_dir, image1)
                    # with open(file_path, 'rb') as f:
                    #     imag1 = MIMEImage(f.read())
                    #     imag1.add_header(
                    #         'Content-ID', '<{name}>'.format(name=image1))
                    #     imag1.add_header('Content-Disposition',
                    #                      'inline', filename=image1)
                    # mwg.attach(imag1)

                    # image2 = "icon0.png"
                    # file_path = os.path.join(img_dir, image2)
                    # with open(file_path, 'rb') as f:
                    #     img2 = MIMEImage(f.read())
                    #     img2.add_header(
                    #         'Content-ID', '<{name}>'.format(name=image2))
                    #     img2.add_header('Content-Disposition',
                    #                     'inline', filename=image2)
                    # mwg.attach(img2)

                    # mwg.send()
                    
                    #Add extra code here
                    new_user(request,username,'new_user',email,'account-verification.html','Verify Your Account - Complete Your Registration',link)
                    
                    
                    
                    cursor.close()
                    sys.stdout = open("terminal_out5.txt", "a")
                    print("execute function")
                    sys.stdout.close()
                    messages.success(
                        request, 'Your account is sucessfully registered and now, check your mail to activate your account.')
                except:
                    messages.warning(request, "User already exists !!! ")

            else:
                messages.warning(
                    request, "Enter the correct email or username. !!! ")
        else:
            messages.warning(request,
                             'Invalid reCAPTCHA. Please try again.')
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    ban = PageBanner.objects.all()
    seo1 = Seo_Content.objects.all()
    
    return render(request, "Normal-User/register.html", {"footer": fot, 'ban': ban,"Seo1": seo,"Seo":seo1,})


def generatetoken():
    salt = secrets.token_urlsafe(16)
    # Generate a unique token using a combination of salt and a strong random value
    token = salt + secrets.token_urlsafe(16)

    # Hash the token using a strong hash function like SHA-256
    token = hashlib.sha256(token.encode()).hexdigest()
    return token


@csrf_exempt
def Loginapi(request):
    if (request.method == "POST"):
        ip_add = get_client_ip(request)
        username = request.POST.get("username")
        passw = request.POST.get("password")
        user = auth.authenticate(username=username, password=passw)
        if (user is not None):
            auth.login(request, user)
            ln = LoginIP(userid=user.id, username=username, IP_Address=ip_add, location=get_location( request), sessionkey=request.session.session_key, device=request.META.get('HTTP_USER_AGENT', ''))
            ln.save()
            if user.is_superuser == True:
                usermes = "Admin Login Successfully!...."
                token = user.mobileapptoken
                token = encrypt(token)
                loginid = user.id
                data = {"status": True, "message": usermes,
                        'token': token, 'loginid': loginid}
                data = json.dumps(data, default=str)
                return HttpResponse(data, content_type="application/json", status=200)
            permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
                userid=user.id).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
            if user.is_active == True and permissionname == 'influencer_permission':
                usermes = "Influencer Login Successfully!...."
                token = user.mobileapptoken
                loginid = user.id
                token = encrypt(token)
                data = {"status": True, "message": usermes,
                        'token': token, 'loginid': loginid}
                data = json.dumps(data, default=str)
                return HttpResponse(data, content_type="application/json", status=200)
            elif user.is_active == True and permissionname == 'client_permission':
                usermes = "Client Login Successfully!...."
                token = user.mobileapptoken
                token = encrypt(token)
                loginid = user.id
                data = {"status": True, "message": usermes,
                        'token': token, 'loginid': loginid}
                data = json.dumps(data, default=str)
                return HttpResponse(data, content_type="application/json", status=200)
            else:
                usermes = 'User is not activated!....'
                data = {"status": False,
                        "message": usermes,  'token': None, 'loginid': 0}
                data = json.dumps(data, default=str)
                return HttpResponse(data, content_type="application/json", status=200)

            # elif ay.exists() and pr.adsagency_permission == True:
            #     # return HttpResponseRedirect("/")

            # # Enter the manager admin path
            # elif user.Role_Type == "Manager" and pr.Manager_permission == True:
            #     return HttpResponseRedirect("/index2/")

            # # Enter the Relationship Manager admin path
            # elif user.Role_Type == "Relationship Manager" and pr.RM_permission == True:
            #     # return HttpResponseRedirect("/")

            # # Enter the Accountant admin path
            # elif user.Role_Type == "Accountant" and pr.Account_permission == True:
            #     # return HttpResponseRedirect("/")

            # # Enter the KYC admin path
            # elif user.Role_Type == "KYC Manager" and pr.KycManager_permission == True:
            #     # return HttpResponseRedirect("/")

            # # Enter the  admin path
            # elif user.Role_Type == "Admin" and pr.Admin_permission == True:
            #     # return HttpResponseRedirect("/")

            # # Enter the  Super admin path
            # elif user.Role_Type == "Super Admin" and pr.Superadmin_permission == True:
            #     # return HttpResponseRedirect("/")
        else:
            usermes = 'User details is not found!..'
            data = {"status": False,
                    "message": usermes,  'token': None, 'loginid': 0}
            data = json.dumps(data, default=str)
            return HttpResponse(data, content_type="application/json", status=200)


@csrf_exempt
def Registerapi(request):
    token = None
    if (request.method == "POST"):
        email = request.POST.get("email")
        username = request.POST.get("username")

        if verify_email(email) == True and len(username) > 0:
            try:
                actype = request.POST.get("actype")
                pward = request.POST.get('password')

                cursor = connection.cursor()
                hashpass = make_password(pward)
                cursor.execute('call userscreation(%s,%s,%s,%s,%s)',
                               (username, hashpass, email, actype, 0))
                user = cursor.fetchall()[0][0]
                token = generatetoken()
                user = Allusers.objects.filter(id=user)
                if user.exists():
                    user = user[0]
                    user.mobileapptoken = token
                    user.save(update_fields=['mobileapptoken'])
                usnam = user.username
                link = 'https://www.influencerhiring.com/activate/' + \
                    urlsafe_base64_encode(force_bytes(
                        user.id))+'/'+account_activation_token.make_token(user)+'/'
                # html_con = render_to_string(
                #     "Influencer-Admin/verify.html", {'link': link, 'user': usnam}, request=request)
                # text = strip_tags(html_con)

                # data = {
                #     'subject': 'Activate Your Account By Confirming Your Mail ID:',
                #     'body': text,
                #     'to_email': email
                # }
                # mwg = EmailMultiAlternatives(
                #     subject=data['subject'],
                #     body=data['body'],
                #     from_email='admin@influencerhiring.com',
                #     to=[data['to_email']]
                # )
                # mwg.attach_alternative(html_con, "text/html")
                # # img_dir=r'C:\Users\BOL7\Desktop\Influencer\mainapp\static'
                # img_dir = str(settings.BASE_DIR)+'\mainapp\static'
                # img_dir = r'{}'.format(img_dir)
                # image = "influencerhiring.png"
                # file_path = os.path.join(img_dir, image)
                # with open(file_path, 'rb') as f:
                #     img = MIMEImage(f.read())
                #     img.add_header(
                #         'Content-ID', '<{name}>'.format(name=image))
                #     img.add_header('Content-Disposition',
                #                    'inline', filename=image)
                # mwg.attach(img)

                # image1 = "welcome.png"
                # file_path = os.path.join(img_dir, image1)
                # with open(file_path, 'rb') as f:
                #     imag1 = MIMEImage(f.read())
                #     imag1.add_header(
                #         'Content-ID', '<{name}>'.format(name=image1))
                #     imag1.add_header('Content-Disposition',
                #                      'inline', filename=image1)
                # mwg.attach(imag1)

                # image2 = "icon0.png"
                # file_path = os.path.join(img_dir, image2)
                # with open(file_path, 'rb') as f:
                #     img2 = MIMEImage(f.read())
                #     img2.add_header(
                #         'Content-ID', '<{name}>'.format(name=image2))
                #     img2.add_header('Content-Disposition',
                #                     'inline', filename=image2)
                # mwg.attach(img2)

                # mwg.send()
                new_user(request,username,'new_user',email,'account-verification.html','Verify Your Account - Complete Your Registration',link)
                
                cursor.close()

                message = 'Your account is sucessfully registered and now, check your mail to activate your account.'
                data = {"status": True, 'message': message}
                data = json.dumps(data, default=str)
                return HttpResponse(data, content_type="application/json", status=200)
            except:
                message = "User is already exists !!! "
                data = {"status": False, 'message': message}
                data = json.dumps(data, default=str)
                return HttpResponse(data, content_type="application/json", status=200)
        else:
            if verify_email(email) == False:
                message = "Enter the correct email !... "
            # if valid_username(username) == False:
            #     message = "Enter the correct username, it can't be contains numeric only !... "
            # if valid_username(username) == False and verify_email(email) == False:
            #     message = "Your email is  not valid and username can't contains numeric value only!..."
            data = {"status": False, 'message': message}
            data = json.dumps(data, default=str)
            return HttpResponse(data, content_type="application/json", status=200)


# Confirm Email of registration user
from threading import Thread
def activate(request, uidb64, token):
    User = Allusers()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Allusers.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        userid = user.id
        sett = InfluencerSettings.objects.filter(influencer_userid=str(userid))
        if sett.exists():
            sett = sett[0]
            sett.email_verified = True
            sett.save(update_fields=['email_verified'])
        else:
            cls = ClientSettings.objects.filter(csettingsuserid=str(userid))
            if cls.exists():
                cls = cls[0]
                cls.email_verified = True
                cls.save(update_fields=['email_verified'])
        user.save()
        
        new_user(request,user.username,'new_user',user.email,'new-user-registration.html','Welcome to '+user.username,None)
        
        bgt1=Thread(target=lambda:existing_user(request,name=user.username,user_type='existing_user',email_add=user.email,template_name='user-profile-update-enhance-your-profile-with-image.html',subject='Enhance Your User Profile-Add a Profile Image, Bio, and Showcase Your Work.'))
        bgt1.start()
        messages.success(
            request, 'Your account is successfully activated and can be login here!....')
        return HttpResponseRedirect('/login/')
    else:
        messages.warning(
            request, 'Your session is expired and try again after some time!....')
        return HttpResponseRedirect('/register/')


@login_required(login_url='/login/')
def Logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


def Reset(request):
    if (request.method == "POST"):
        username = request.POST.get("username")
        u = Allusers.objects.filter(
            email=username) or Allusers.objects.filter(username=username)
        if u.exists():
            user = u[0]
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'https://www.influencerhiring.com/resetpassword/'+uid+'/'+token+'/'
            print('Password Reset Link', link)

            current_site = get_current_site(request)
            # html_con = render_to_string(
            #     "Influencer-Admin/forgot.html", {'domain': current_site.domain, 'link': link}, request=request)
            # text = strip_tags(html_con)
            # print("Content", text)
            # # body = 'Click Following Link to Reset Your Password '+link
            # data = {
            #     'subject': 'Reset Your Password',
            #     'body': text,
            #     'to_email': user.email
            # }
            # email = EmailMultiAlternatives(
            #     subject=data['subject'],
            #     body=data['body'],
            #     from_email='admin@influencerhiring.com',
            #     to=[data['to_email']]
            # )
            # email.attach_alternative(html_con, "text/html")
            # # img_dir=r'C:\Influencer\influencer\mainapp\static'
            # img_dir = str(settings.BASE_DIR)+'\mainapp\static'
            # img_dir = r'{}'.format(img_dir)
            # image = "forgotlogo.png"
            # file_path = os.path.join(img_dir, image)
            # with open(file_path, 'rb') as f:
            #     img = MIMEImage(f.read())
            #     img.add_header('Content-ID', '<{name}>'.format(name=image))
            #     img.add_header('Content-Disposition', 'inline', filename=image)
            # email.attach(img)
            # image1 = "influencerhiring.png"
            # file_path = os.path.join(img_dir, image1)
            # with open(file_path, 'rb') as f:
            #     imag1 = MIMEImage(f.read())
            #     imag1.add_header('Content-ID', '<{name}>'.format(name=image1))
            #     imag1.add_header('Content-Disposition',
            #                      'inline', filename=image1)
            # email.attach(imag1)

            # image2 = "icon0.png"
            # file_path = os.path.join(img_dir, image2)
            # with open(file_path, 'rb') as f:
            #     img2 = MIMEImage(f.read())
            #     img2.add_header('Content-ID', '<{name}>'.format(name=image2))
            #     img2.add_header('Content-Disposition',
            #                     'inline', filename=image2)
            # email.attach(img2)

            # email.send()
            
            existing_user(request,name=user.username,user_type='existing_user',email_add=user.email,template_name='forgot-password.html',subject='Reset Your Password',password_reset_link=link)
            messages.success(
                request, 'Password Reset Link Send Sucessfully!..')
        else:
            messages.warning(request, "Username or Email is Incorrect")
    fot = FooterDetail.objects.all()
    return render(request, "Normal-User/reset.html", {"footer": fot})


def ResetPassword(request, uid, token):
    if (request.method == "POST"):
        try:
            password = request.POST.get("password")
            password1 = request.POST.get("password1")
            if password != password1:
                raise messages.warning(
                    request, "Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = Allusers.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise messages.warning(
                    request, 'Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Changed Sucessfully!..')
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise messages.warning(request, 'Token is not Valid or Expired')
        return HttpResponseRedirect('/login/')
    fot = FooterDetail.objects.all()
    return render(request, "Normal-User/resetpassword.html", {"footer": fot})


def Index(request, var=None, loginid=None):

    print("variable", var)
    base_url = "{0}://{1}{2}".format(request.scheme,
                                     request.get_host(), request.path)
    if var == 'api':
        print("Rahul")
        clientid = loginid
        if clientid is None:
            clientid = 0

        det = Home_Page_Detail.objects.all()
        com = CompanyLogo.objects.all()
        tes = Testimonails.objects.filter(testimonails_approved=True)
        fot = FooterDetail.objects.all()
        seo1 = Seo_Content.objects.all()
        seo = Seo_Settings.objects.select_related('page').all()
        diff = DifferentCategory.objects.all()
        greetingid = Services.objects.get(
            servicename='Greeting Messages').serviceid
        influacquisitionid = Services.objects.get(
            servicename='Influencer Acquisition').serviceid
        brandid = Services.objects.get(servicename='Brand Promotion').serviceid
        videochatid = Services.objects.get(
            servicename='Video Chat').serviceid

        curr = datetime.now().strftime("%Y-%m-%d")
        ccdet = Casting_Call.objects.filter(
            approved=True, expirydate__gte=curr)
        cursor = connection.cursor()
        country = get_location(request)
        print("ibndxdata", country)
        if country is None:
            country = 'India'
        print("data", country)
        curs = ExchangeRates.objects.filter(country__icontains=country)
        if curs.exists():
            curs = curs[0]

        cursor.execute('select * from verifieduserss(%s,%s,%s)',
                       [country, 0, clientid])
        user = cursor.fetchall()
        print('influencer', user)
        cursor.execute('select * from verifieduserss(%s,%s,%s)',
                       [country, greetingid, clientid])
        greeting = cursor.fetchall()
        print("\nServiceid", greeting)
        cursor.execute('select * from verifieduserss(%s,%s,%s)',
                       [country, brandid, clientid])
        brands = cursor.fetchall()
        print("\nServiceid", brands)
        cursor.execute('select * from verifieduserss(%s,%s,%s)',
                       [country, videochatid, clientid])
        videochat = cursor.fetchall()
        print("\nServiceid", videochat)

        cursor.execute('select * from verifieduserss(%s,%s,%s)',
                       [country, influacquisitionid, clientid])
        acquisition = cursor.fetchall()
        print("\nServiceid", acquisition)
        cursor.execute('select relname,n_live_tup from pg_stat_user_tables where relname in (%s,%s,%s,%s)', [
            'mainapp_categories', 'mainapp_clientsettings', 'mainapp_orders', 'mainapp_influencersettings'])
        counts = cursor.fetchall()
        counts = [item for t in counts for item in t]
        for i in range(0, len(counts)):
            if i % 2 != 0:
                num = numerize.numerize(counts[i])
                counts[i] = num
        print("\nno. of counts", counts)
        print('influencer', user)
        cursor.close()

        myctdata = []
        if clientid is not None:
            myct = Wishlist.objects.filter(clientid=clientid)
            if myct.exists():
                for i in myct:
                    print("cartid", i.wishlistid)
                    print("data", i.influencerid)
                    id3 = str(i.influencerid)
                    username = Allusers.objects.get(id=id3).username
                    name = InfluencerProfile.objects.get(influencer_userid=id3)
                    fullname = name.fullname
                    destitle = name.desc_title
                    shortdes = name.short_description
                    image = str(name.profileimage)
                    pr = PricingPlans.objects.get(
                        usersid=id3, plan_type='Basic')
                    basicpr = pr.increasedprice
                    wishlistid = i.wishlistid
                    curre = str(curs.currency)
                    locct = (fullname, destitle, shortdes,
                             basicpr, wishlistid, image, curre, id3, username)
                    myctdata.append(locct)
            print("listdata", myctdata)

        data = {'cur': curs, 'counts': counts, "home": list(det.values()), "companyLogo": list(com.values()), "test": list(tes.values()), "footer": list(fot.values()), "seo": list(seo.values()),
                "info": user, 'info1': greeting, 'info2': brands, 'info3': videochat, 'info4': acquisition, 'diff': list(diff.values()), 'wishdata': myctdata, 'ccdet': list(ccdet.values())}
        data = json.dumps(data, default=str)
        return HttpResponse(data, content_type="application/json")

    clientid = request.user.id
    if clientid is None:
        clientid = 0

    det = Home_Page_Detail.objects.all()
    com = CompanyLogo.objects.all()
    tes = Testimonails.objects.filter(testimonails_approved=True)
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    
    diff = DifferentCategory.objects.all()
    greetingid = Services.objects.get(
        servicename='Greeting Messages').serviceid
    influacquisitionid = Services.objects.get(
        servicename='Influencer Acquisition').serviceid
    brandid = Services.objects.get(servicename='Brand Promotion').serviceid
    videochatid = Services.objects.get(
        servicename='Video Chat').serviceid

    cursor = connection.cursor()
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)

    curr = datetime.now().strftime("%Y-%m-%d")
    ccdet = Casting_Call.objects.filter(
        approved=True, expirydate__gte=curr, country__icontains=country)

    for i in ccdet:
        key = i.castingcallid
        i.castingcallid = encrypt(key)
        print(i)

    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]

    cursor.execute('select * from verifieduserss(%s,%s,%s)',
                   [country, 0, clientid])
    user = cursor.fetchall()
    print('influencer', user)
    cursor.execute('select * from verifieduserss(%s,%s,%s)',
                   [country, greetingid, clientid])
    greeting = cursor.fetchall()
    print("\nServiceid", greeting)
    cursor.execute('select * from verifieduserss(%s,%s,%s)',
                   [country, brandid, clientid])
    brands = cursor.fetchall()
    print("\nServiceid", brands)
    cursor.execute('select * from verifieduserss(%s,%s,%s)',
                   [country, videochatid, clientid])
    videochat = cursor.fetchall()
    print("\nServiceid", videochat)

    cursor.execute('select * from verifieduserss(%s,%s,%s)',
                   [country, influacquisitionid, clientid])
    acquisition = cursor.fetchall()
    print("\nServiceid", acquisition)
    cursor.execute('select relname,n_live_tup from pg_stat_user_tables where relname in (%s,%s,%s,%s)', [
                   'mainapp_categories', 'mainapp_clientsettings', 'mainapp_orders', 'mainapp_influencersettings'])
    counts = cursor.fetchall()
    counts = [item for t in counts for item in t]
    for i in range(0, len(counts)):
        if i % 2 != 0:
            num = numerize.numerize(counts[i])
            counts[i] = num
    print("\nno. of counts", counts)
    print('influencer', user)

    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3, username)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)
    # For Influencer Dashbaord
    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]
            
    

    # sys.stdout = open("verifiedusers.txt", "a")
    if request.method == 'GET':
        ser = Services.objects.all().order_by('serviceid')
        cate = Categories.objects.all().distinct('categoryname')
        plat = Platforms.objects.all().order_by('platformid')
        cntry = InfluencerProfile.objects.values_list(
            'country', flat=True).distinct()
        print("Get Request", request.GET)
        print("value", request.GET.get('search'))
        seritem = request.GET.get('search')
        if seritem is not None and len(seritem) > 0:
            cursor.execute('select * from verifiedusersnews(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           [country, None, None, None, None, None, None, None, clientid, seritem])
            print("query", cursor.query)
            user = cursor.fetchall()
            print("New user", user)
            return render(request, "Normal-User/influencers.html", {"footer": fot, "cont": cntry, "Seo1": seo, "Seo":seo1, "info": user, "Plat": plat, 'Cate': cate, "Ser": ser, 'wishdata': myctdata, 'logininfo': influ})

    cursor.close()
    # sys.stdout.close()
    return render(request, "Normal-User/index.html", {'cur': curs, 'Counts': counts, "Home": det, "CompanyLogo": com, "Test": tes, "footer": fot, "Seo1": seo,"Seo":seo1, "info": user, 'info1': greeting, 'info2': brands, 'info3': videochat, 'info4': acquisition, 'diff': diff, 'wishdata': myctdata, 'ccdet': ccdet, 'logininfo': influ, 'plink': base_url, 'cartdata': usctdata})


@csrf_exempt
def whishlist(request):
    enterwishuser = request.user.id
    myct = Wishlist.objects.filter(clientid=enterwishuser)
    myctdata = []
    if myct.exists():
        for i in myct:
            print("cartid", i.wishlistid)
            print("data", i.influencerid)
            id3 = str(i.influencerid)
            name = InfluencerProfile.objects.get(influencer_userid=id3)
            fullname = name.fullname
            destitle = name.desc_title
            shortdes = name.short_description
            image = str(name.profileimage)
            pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
            basicpr = pr.increasedprice
            wishlistid = i.wishlistid
            # curr=str(curs.currency)
            locct = (fullname, destitle, shortdes, basicpr, wishlistid, image)
            myctdata.append(locct)
    print("listdata", myctdata)

    if request.method == 'POST':
        sys.stdout = open("wishlist.txt", "a")
        influecerid = request.body
        influecerid = influecerid.decode()
        print("enter", enterwishuser)
        print("sdv", influecerid)
        id = Allusers.objects.filter(id=enterwishuser)
        id = id[0]
        id1 = Allusers.objects.filter(id=influecerid)
        id1 = id1[0]
        print("id", id)
        print("id1", id1)
        print("execute")
        ins = InfluencerSettings.objects.filter(influencer_userid=id1)
        if ins.exists():
            ins = ins[0]
        print("ins", ins)
        cls = ClientSettings.objects.filter(csettingsuserid=id)
        if cls.exists():
            cls = cls[0]
        print("cls", cls)
        wh = Wishlist.objects.filter(
            clientid=enterwishuser, influencerid=influecerid)
        if wh.exists():
            print("Alreday available")
        else:
            lt = Wishlist(clientid=cls, influencerid=ins)
            lt.save()
            print("save wishlist")
        print("Wishes", myctdata)

        sys.stdout.close()
        return JsonResponse({'results': myctdata})


@csrf_exempt
def delwhishlist(request):
    enterwishuser = request.user.id
    # enterwishuser=103602
    if request.method == 'POST':
        sys.stdout = open("delwishlist.txt", "a")
        influecerid = request.body
        influecerid = influecerid.decode()
        print("enter", enterwishuser)
        print("sdv", influecerid)
        lt = Wishlist.objects.get(
            clientid=enterwishuser, influencerid=influecerid)
        lt.delete()
        print("delete wishlist")

        myct = Wishlist.objects.filter(clientid=enterwishuser)
        myctdata = []
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                # curr=str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image)
                myctdata.append(locct)
        print("Wishes", myctdata)
        sys.stdout.close()
        return JsonResponse({'results': myctdata})


@csrf_exempt
def delmywhishlist(request):
    enterwishuser = request.user.id
    # enterwishuser=103602
    if request.method == 'POST':
        sys.stdout = open("delwishlist.txt", "a")
        if request.POST.get('id') != None:
            influecerid = request.POST.get('id')
            print("Infoid", influecerid)
            print("Client", enterwishuser)
            lt = Wishlist.objects.get(
                clientid=enterwishuser, influencerid=influecerid)
            lt.delete()
            print("delete wishlist")
        myct = Wishlist.objects.filter(clientid=enterwishuser)
        myctdata = []
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                # curr=str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, id3)
                myctdata.append(locct)
        print("Wishes", myctdata)
        sys.stdout.close()
        return JsonResponse({'results': myctdata})
        # return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def delmycart(request):
    enterwishuser = request.user.id
    # enterwishuser=103602
    # country1 = get_location(request)
    # if country1 is None:
    #     country1 = 'India'

    # print("data", country1)
    # curs = ExchangeRates.objects.filter(country__icontains=country1)
    # if curs.exists():
    #     curs = curs[0]
    if request.method == 'POST':
        sys.stdout = open("delcartlist.txt", "a")
        if request.POST.get('id') != None:
            influecerid = request.POST.get('id')
            print("Infoid", influecerid)
            print("Client", enterwishuser)
            lt = Cart.objects.get(
                clientid=enterwishuser, influencerid=influecerid)
            lt.delete()
            print("delete Cart")

        country = get_location(request)
        print("ibndxdata", country)
        if country is None:
            country = 'India'
        print("data", country)
        curs = ExchangeRates.objects.filter(country__icontains=country)
        if curs.exists():
            curs = curs[0]
        myct = Cart.objects.filter(clientid=enterwishuser)
        usctdata = []
        if enterwishuser is not None:
            myct = Cart.objects.filter(clientid=enterwishuser)
            if myct.exists():
                for i in myct:
                    print("cartid", i.Cartid)
                    print("data", i.influencerid)
                    id3 = str(i.influencerid)
                    username = Allusers.objects.get(id=id3).username
                    name = InfluencerProfile.objects.get(influencer_userid=id3)
                    fullname = name.fullname
                    destitle = name.desc_title
                    shortdes = name.short_description
                    image = str(name.profileimage)
                    pr = PricingPlans.objects.get(
                        usersid=id3, plan_type='Basic')
                    basicpr = pr.increasedprice
                    Cartid = i.Cartid
                    curre = str(curs.currency)
                    locct = (fullname, destitle, shortdes,
                             basicpr, Cartid, image, curre, id3, username)
                    usctdata.append(locct)
        print("mycartdata", usctdata)
        sys.stdout.close()
        return JsonResponse({'results': usctdata})
        # return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def mycart(request):
    user = request.user.id
    if request.method == 'POST':
        sys.stdout = open("cart.txt", "a")
        if request.POST.get('client') != None:
            clientid = request.POST.get('client')
        if request.POST.get('influencer') != None:
            infoid = request.POST.get('influencer')
        print("Client id", clientid)
        print("indo", infoid)
        id = Allusers.objects.filter(id=clientid)
        id = id[0]
        id1 = Allusers.objects.filter(id=infoid)
        id1 = id1[0]
        ins = InfluencerSettings.objects.filter(influencer_userid=id1)
        if ins.exists():
            ins = ins[0]
        print("ins", ins)
        cls = ClientSettings.objects.filter(csettingsuserid=id)
        if cls.exists():
            cls = cls[0]
        print("cls", cls)
        ct = Cart.objects.filter(clientid=clientid, influencerid=infoid)
        if ct.exists():
            print("Already available")
        else:
            ct1 = Cart(clientid=cls, influencerid=ins)
            ct1.save()
            print("save cart")

        country = get_location(request)
        print("ibndxdata", country)
        if country is None:
            country = 'India'
        print("data", country)
        curs = ExchangeRates.objects.filter(country__icontains=country)
        if curs.exists():
            curs = curs[0]
        myct = Cart.objects.filter(clientid=user)
        usctdata = []
        if clientid is not None:
            myct = Cart.objects.filter(clientid=user)
            if myct.exists():
                for i in myct:
                    print("cartid", i.Cartid)
                    print("data", i.influencerid)
                    id3 = str(i.influencerid)
                    username = Allusers.objects.get(id=id3).username
                    name = InfluencerProfile.objects.get(influencer_userid=id3)
                    fullname = name.fullname
                    destitle = name.desc_title
                    shortdes = name.short_description
                    image = str(name.profileimage)
                    pr = PricingPlans.objects.get(
                        usersid=id3, plan_type='Basic')
                    basicpr = pr.increasedprice
                    Cartid = i.Cartid
                    curre = str(curs.currency)
                    locct = (fullname, destitle, shortdes,
                             basicpr, Cartid, image, curre, id3, username)
                    usctdata.append(locct)
        print("mycartdata", usctdata)
        sys.stdout.close()
        # json.dumps({'results': myctdata}, cls=DjangoJSONEncoder)
        return JsonResponse({'results': usctdata})


@csrf_exempt
def mywishlist(request):
    enterwishuser = request.user.id
    if request.method == 'POST':
        sys.stdout = open("wishcart.txt", "a")
        if request.POST.get('id') != None:
            influencerid = request.POST.get('id')

        if request.POST.get('login') != None:
            clientid = request.POST.get('login')
        id = Allusers.objects.filter(id=clientid)
        id = id[0]
        id1 = Allusers.objects.filter(id=influencerid)
        id1 = id1[0]
        print("id", id)
        print("id1", id1)
        print("execute")
        ins = InfluencerSettings.objects.filter(influencer_userid=id1)
        if ins.exists():
            ins = ins[0]
        print("ins", ins)
        cls = ClientSettings.objects.filter(csettingsuserid=id)
        if cls.exists():
            cls = cls[0]
        print("cls", cls)
        wh = Wishlist.objects.filter(
            clientid=enterwishuser, influencerid=influencerid)
        if wh.exists():
            print("Alreday available")
        else:
            lt = Wishlist(clientid=cls, influencerid=ins)
            lt.save()
            print("save wishlist")
        myct = Wishlist.objects.filter(clientid=enterwishuser)
        myctdata = []
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                # curr=str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, id3)
                myctdata.append(locct)
        print("Wishes", myctdata)
        sys.stdout.close()
        # json.dumps({'results': myctdata}, cls=DjangoJSONEncoder)
        return JsonResponse({'results': myctdata})


def About(request, var=None):
    At = AboutDetail.objects.all().order_by('id')
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    ban = PageBanner.objects.all()
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    if var == 'api':
        data = {"about": list(At.values()), "footer": list(
            fot.values()), "seo": list(seo.values()), 'ban': list(ban.values())}
        data = json.dumps(data, default=str)
        return HttpResponse(data, content_type="application/json")
    return render(request, "Normal-User/about.html", {'cartdata': usctdata, "About": At, "footer": fot, "Seo1": seo,"Seo":seo1, 'ban': ban, 'wishdata': myctdata, 'logininfo': influ})


# @login_required(login_url='/login/')
# def Settingspage(request):
#     userid = request.user.id
#     id = Allusers.objects.filter(id=userid)
#     id = id[0]
#     permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
#         userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
#     ac = InfluencerProfile.objects.filter(influencer_userid=userid)
#     ac = ac[0]
#     if permissionname == 'influencer_permission':
#         if (request.method == "POST"):
#             fullname = request.POST.get("lastname")
#             gender = request.POST.get("RadioGroup3")
#             email = request.POST.get("email")
#             username = request.POST.get('username')
#             password = request.POST.get('pass')
#             password1 = request.POST.get('pass1')
#             newroles = request.POST.get('role')
#             if newroles is not None and len(newroles) > 0:
#                 oldrole = id.roles
#                 loginuserid = userid
#                 cursor = connection.cursor()
#                 cursor.execute('call usersroleupdation(%s,%s,%s)',
#                                (loginuserid, oldrole, newroles))
#                 cursor.close()
#                 auth.logout(request)
#                 return HttpResponseRedirect("/login/")
#             if ac:
#                 ac.gender = gender
#                 if fullname is not None and len(fullname) > 0:
#                     ac.fullname = fullname
#                     ac.save(update_fields=['fullname'])
#                     print("up name")
#                 if gender is not None and len(gender) > 0:
#                     ac.gender = gender
#                     ac.save(update_fields=['gender'])
#                     print("up gen")
#             if id:
#                 if username is not None and len(username) > 0 and valid_username(username) == True:
#                     id.username = username
#                     id.save(update_fields=['username'])
#                     print("username")
#                 else:
#                     messages.warning(
#                         request, 'Enter the correct username !...')
#                 if email is not None and len(email) > 0 and verify_email(email) and True:
#                     id.email = email
#                     id.save(update_fields=['email'])
#                     print("email")
#                 else:
#                     messages.warning(request, 'Enter the correct email !...')
#                 if password is not None and len(password) > 0 and password == password1:
#                     id.password = make_password(password)
#                     id.save(update_fields=['password'])
#                     print("up passsword")
#                 else:
#                     messages.warning(request, 'Password does not match !...')
#         return render(request, "Influencer-Admin/settings.html")
#     return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def box(request):
    userid = request.user.id
    userid = Allusers.objects.filter(id=userid)[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    data = json.loads(request.body)
    choose = data['choose']
    rules = data['rules']
    if permissionname == 'influencer_permission':
        if ac:
            if choose is not None and len(choose) > 0:
                ac.chooseme = choose
                ac.save(update_fields=['chooseme'])
            if rules is not None and len(rules) > 0:
                print("Rules", rules)
                ac.rulesforgig = rules
                ac.save(update_fields=['rulesforgig'])
                print("Execute function")
        return HttpResponse(status=200)
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def cbox(request):
    userid = request.user.id
    userid = Allusers.objects.filter(id=userid)[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    data = json.loads(request.body)
    lan = data['lang']
    if permissionname == 'influencer_permission':
        if ac:
            if lan is not None and len(lan) > 0:
                ac.language = lan
                ac.save(update_fields=['language'])
        return HttpResponse(status=200)
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def catbox(request):
    userid = request.user.id
    userid = Allusers.objects.filter(id=userid)[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    data = json.loads(request.body)
    cat = data['categories']
    print("List", cat)
    if permissionname == 'influencer_permission':
        if ac:
            if cat is not None and len(cat) > 0:
                ac.categories = cat
                ac.save(update_fields=['categories'])
        return HttpResponse(status=200)
    return HttpResponseRedirect("/")


cate1 = []


@login_required(login_url='/login/')
def cate(request):
    global cate1
    cate1.clear()
    userid = request.user.id
    userid = Allusers.objects.filter(id=userid)[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    data = json.loads(request.body)
    print("zxcvv", data)
    categ = data['cate']
    print("sdcvzx", categ)
    cti = Categories.objects.filter(categoryname=categ)
    for i in cti:
        cate1.append(i)
    if permissionname == 'influencer_permission':
        print("subcate", cti)
        return HttpResponse(status=200)
    return HttpResponseRedirect("/")


def Faq(request, var=None):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    Fq = FaqDetail.objects.all()
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    ban = PageBanner.objects.all()
    if var == 'api':
        data = {'faq': list(Fq.values()), "footer": list(
            fot.values()), "seo": list(seo.values()), 'ban': list(ban.values())}
        data = json.dumps(data, default=str)
        return HttpResponse(data, content_type="application/json")
    return render(request, "Normal-User/faq.html", {'cartdata': usctdata, 'Faq': Fq, "footer": fot, "Seo1": seo,"Seo":seo1, 'ban': ban, 'logininfo': influ, 'wishdata': myctdata})


def fetchdetails(request, order):
    sys.stdout = open("fetchorders.txt", "a")
    print("haudhf", order)
    # cursor = connection.cursor()
    # cursor.execute('select * from ordersdetails(%s,%s,%s)',
    #                [status, userid, order])
    # oddr = cursor.fetchall()
    order_det=Orders.objects.select_related('clientid','serviceid').values('orderstatus','clientid__fullname','ordersid','orderdate','serviceid__servicename','plantype','finalamt','orderdescription','iscouponapplied','finalamtafterdiscount').filter(ordersid=order, paymentstatus=True).all()
    oddr = json.dumps(list(order_det),default=str)
    print("deatils", oddr)
    sys.stdout.close()
    return JsonResponse({'results': oddr})


def fetchtestimonails(request, testimonailid):
    sys.stdout = open("fetchtestis.txt", "a")
    print("haudhf", testimonailid)
    cursor = connection.cursor()
    cursor.execute(
        'select * from mainapp_testimonails where id=%s', [testimonailid])
    oddr = cursor.fetchall()
    print("deatils", oddr)
    sys.stdout.close()
    return JsonResponse({'results': oddr})


def fetchblogcomment(request, commentid):
    sys.stdout = open("fetchcomments.txt", "a")
    print("haudhf", commentid)
    cursor = connection.cursor()
    cursor.execute(
        'select * from mainapp_blogcomments where commentid=%s', [commentid])
    oddr = cursor.fetchall()
    print("deatils", oddr)
    sys.stdout.close()
    return JsonResponse({'results': oddr})


def fetchcallcasting(request, castingcallid):
    sys.stdout = open("fetchcastingcallid.txt", "a")
    print("haudhf", castingcallid)
    cursor = connection.cursor()
    cursor.execute(
        'select * from mainapp_casting_call where castingcallid=%s', [castingcallid])
    oddr = cursor.fetchall()
    print("deatils", oddr)
    sys.stdout.close()
    return JsonResponse({'results': oddr})


def fetchinforeview(request, reviewid):
    sys.stdout = open("fetchreviewid.txt", "a")
    print("haudhf", reviewid)
    cursor = connection.cursor()
    cursor.execute(
        'select mi.influencersreviewid,mi.review_message,mi.rating,mi.date,(select fullname from mainapp_clientprofile where client_userid=mi.clientid) as Clientname,(select fullname from mainapp_influencerprofile where influencer_userid=mi.influencerid) as influencername,mi.isapproved from mainapp_influencersreview as mi where mi.influencersreviewid=%s', [reviewid])
    oddr = cursor.fetchall()
    print("deatils", oddr)
    sys.stdout.close()
    return JsonResponse({'results': oddr})


def Influencers(request, cate=None):
    # sys.stdout = open("influencersusers.txt", "a")
    path = "{0}".format(request.path)
    if cate is not None:
        path = path[0:13]

    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()

    clientid = request.user.id
    if clientid is None:
        clientid = 0

    cursor = connection.cursor()
    country1 = get_location(request)
    if country1 is None:
        country1 = 'India'

    print("data", country1)
    curs = ExchangeRates.objects.filter(country__icontains=country1)
    if curs.exists():
        curs = curs[0]

    # usctdata = []

    # if clientid is not None:
    #     myct = Cart.objects.filter(clientid=clientid)
    #     if myct.exists():
    #         for i in myct:
    #             print("cartid", i.Cartid)
    #             print("data", i.influencerid)
    #             id3 = str(i.influencerid)
    #             name = InfluencerProfile.objects.get(influencer_userid=id3)
    #             fullname = name.fullname
    #             destitle = name.desc_title
    #             shortdes = name.short_description
    #             image = str(name.profileimage)
    #             pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
    #             basicpr = pr.increasedprice
    #             Cartid = i.Cartid
    #             curre = str(curs.currency)
    #             locct = (fullname, destitle, shortdes,
    #                      basicpr, Cartid, image, curre, id3)
    #             usctdata.append(locct)
    #     print("mycartdata", usctdata)

    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    cursor.execute('select * from verifiedusersnews(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                   [country1, None, None, None, None, None, None, cate, clientid, None])
    print("query", cursor.query)
    user = cursor.fetchall()
    print('influencers', user)
    cate = Categories.objects.all().distinct('categoryname')
    # cursor.execute(
    #     'select distinct(categoryname) from mainapp_categories')
    # print("query", cursor.query)
    # cate = cursor.fetchall()
    # cate = [item for t in cate for item in t if item != None]
    print('categories', cate)
    cntry = InfluencerProfile.objects.values_list(
        'country', flat=True).distinct()
    ser = Services.objects.all().order_by('serviceid')
    plat = Platforms.objects.all().order_by('platformid')

    sys.stdout = open("influencersusers.txt", "a")

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    # if request.method == 'GET':
    #     if request.GET.get('srch-term') != None:
    #         seritem=request.GET.get('srch-term')
    #         print("Seraching Item",seritem)
    #         cursor.execute('select * from verifiedusersnews(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
    #                    [country1, None, None, None, None, None, None, None,clientid,seritem])
    #         print("query", cursor.query)
    #         user = cursor.fetchall()

    #         print("New user", user)
    #         return render(request, "Normal-User/influencers.html", {"footer": fot, "cont": cntry, "Seo": seo, "info": user, "Plat": plat, 'Cate': cate, "Ser": ser,'wishdata':myctdata})

    if request.method == 'POST':

        if request.POST.get('service') != None:
            posid = request.POST.get('service')
        else:
            # if len(posid) < 1:
            posid = None
        print("service", posid, type(posid))

        if request.POST.get('ser') != None:
            seritem = request.POST.get('ser')
        else:
            # if len(seritem) < 1:
            seritem = None

        if request.POST.get('platform') != None:
            platfromid = request.POST.get('platform')
        else:
            platfromid = None
        print("Id", platfromid, type(platfromid))
        if request.POST.get('country') != None:
            country = request.POST.get('country')
            if len(country) < 1:
                country = country1
        print("country", country, type(country))
        if request.POST.get('minprice') != None and request.POST.get('maxprice') != None:
            minprice = request.POST.get('minprice')
            maxprice = request.POST.get('maxprice')
            print("minprice", minprice, type(minprice))
            if len(minprice) < 1 and len(maxprice) < 1:
                minprice = None
                maxprice = None
        print("minprice1", minprice, type(minprice))
        print("maxprice", maxprice, type(maxprice))
        if request.POST.get('minfollow') != None and request.POST.get('maxfollow') != None:
            minfollow = request.POST.get('minfollow')
            maxfollow = request.POST.get('maxfollow')
            if len(minfollow) < 1 and len(maxfollow) < 1:
                minfollow = None
                maxfollow = None

        print("minfollow", minfollow, type(minfollow))
        print("maxfollow", maxfollow, type(maxfollow))
        print(request.POST)

        # cursor.execute('select * from verifiedusersnew(%s,%s,%s,%s,%s,%s,%s,%s)', ['India', None,None,None,None,None,None,None])

        cursor.execute('select * from verifiedusersnews(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       [country, posid, platfromid, minprice, maxprice, minfollow, maxfollow, None, clientid, seritem])
        print("query", cursor.query)
        user = cursor.fetchall()
        print("New user", user)
        print("TRy")

        return JsonResponse({'results': user})
    sys.stdout.close()
    return render(request, "Normal-User/influencers.html", {'cartdata': usctdata, "footer": fot, "cont": cntry, "Seo1": seo,"Seo":seo1, "info": user, "Plat": plat, 'Cate': cate, "Ser": ser, 'wishdata': myctdata, 'plink': path, 'logininfo': influ})


@csrf_exempt
def Influencersapi(request, cate=None, loginid=None):
    clientid = loginid
    if clientid is None:
        clientid = 0
    if cate == '0':
        cate = None
    cursor = connection.cursor()
    country1 = get_location(request)
    if country1 is None:
        country1 = 'India'
    curs = ExchangeRates.objects.filter(country__icontains=country1)
    if curs.exists():
        curs = curs[0]
    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3)
                usctdata.append(locct)

    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)

    cursor.execute('select * from verifiedusersnews(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                   [country1, None, None, None, None, None, None, cate, clientid, None])

    user = cursor.fetchall()

    cate = Categories.objects.all().distinct('categoryname')

    cntry = InfluencerProfile.objects.values_list(
        'country', flat=True).distinct()
    ser = Services.objects.all().order_by('serviceid')
    plat = Platforms.objects.all().order_by('platformid')

    if request.method == 'POST':
        if request.POST.get('service') != None:
            posid = request.POST.get('service')
        else:
            posid = None
        if request.POST.get('ser') != None:
            seritem = request.POST.get('ser')
        else:
            seritem = None

        if request.POST.get('platform') != None:
            platfromid = request.POST.get('platform')
        else:
            platfromid = None
        if request.POST.get('country') != None:
            country = request.POST.get('country')
        else:
            country = 'India'
        if request.POST.get('minprice') != None and request.POST.get('maxprice') != None:
            minprice = request.POST.get('minprice')
            maxprice = request.POST.get('maxprice')
        else:
            minprice = None
            maxprice = None
        if request.POST.get('minfollow') != None and request.POST.get('maxfollow') != None:
            minfollow = request.POST.get('minfollow')
            maxfollow = request.POST.get('maxfollow')
        else:
            minfollow = None
            maxfollow = None
        cursor.execute('select * from verifiedusersnews(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       [country, posid, platfromid, minprice, maxprice, minfollow, maxfollow, None, clientid, seritem])
        user = cursor.fetchall()
        return JsonResponse({'results': user})
    data = {"cont": cntry,  "info": user, "plat": list(plat.values()), 'cate': list(
        cate.values()), "ser": list(ser.values()), 'wishdata': myctdata, 'cartdata': usctdata}
    data = json.dumps(data, default=str)
    return HttpResponse(data, content_type="application/json")


def Services1(request, username=None, var=None, loginid=None):
    if var == 'api':
        clientid = loginid
        if clientid is None:
            clientid = 0
        base_url = "{0}://{1}{2}".format(request.scheme,
                                         request.get_host(), request.path)
        print("Url", base_url)
        whychoose = []
        gis = []
        whychoose.clear()
        gis.clear()

        username = username.replace('-', ' ')
        print('user', username)
        userid = Allusers.objects.get(username=username).id
        print("userid", userid)
        info = InfluencerProfile.objects.get(influencer_userid=userid)
        print("information", info)
        basic = PricingPlans.objects.filter(usersid=userid, plan_type='Basic')
        if basic.exists():
            basic = basic[0]
        standard = PricingPlans.objects.filter(
            usersid=userid, plan_type='Standard')
        if standard.exists():
            standard = standard[0]
        premium = PricingPlans.objects.filter(
            usersid=userid, plan_type='Premium')
        if premium.exists():
            premium = premium[0]
        gs = PricingPlans.objects.filter(usersid=userid, serviceid=4)
        if gs.exists():
            gs = gs[0]
        vc = PricingPlans.objects.filter(usersid=userid, serviceid=2)
        if vc.exists():
            vc = vc[0]
        st = PricingPlans.objects.filter(usersid=userid, serviceid=3)
        if st.exists():
            st = st[0]
        sr = Services.objects.all().order_by('serviceid')
        im = Images.objects.filter(im_userid=userid)
        vd = Videos.objects.filter(vd_userid=userid)
        stag = Servicetabtitle.objects.filter(influencerid=userid)
        if stag.exists():
            stag = stag[0]
        vl = VideosLink.objects.filter(vl_userid=userid)
        pd = PlatformDetails.objects.filter(usersid=userid)
        tes = Testimonails.objects.filter(testimonails_approved=True)
        yt = pd.filter(platformtype=2)
        if yt.exists():
            yt = yt[0]
            follow = yt.subscribers_followers
            yt.subscribers_followers = numerize.numerize(follow)
        fb = pd.filter(platformtype=4)
        if fb.exists():
            fb = fb[0]
            follow = fb.subscribers_followers
            fb.subscribers_followers = numerize.numerize(follow)
        ig = pd.filter(platformtype=5)
        if ig.exists():
            ig = ig[0]
            follow = ig.subscribers_followers
            ig.subscribers_followers = numerize.numerize(follow)
        tk = pd.filter(platformtype=3)
        if tk.exists():
            tk = tk[0]
            follow = tk.subscribers_followers
            tk.subscribers_followers = numerize.numerize(follow)
        fot = FooterDetail.objects.all()
        seo = Seo_Settings.objects.select_related('page').all()
        ban = PageBanner.objects.all()
        why = info.chooseme
        if why is not None:
            for i in why:
                chos = Whychooseme.objects.get(whychoosemeid=i).Whychoosetext
                whychoose.append(chos)
        gigs = info.rulesforgig
        if gigs is not None:
            for i in gigs:
                rul = Rulesgig.objects.get(rulesid=i).rulesforgig
                gis.append(rul)
        country = get_location(request)
        cursor = connection.cursor()
        if country is None:
            country = 'India'
        print("data", country)
        curs = ExchangeRates.objects.filter(country__icontains=country)
        if curs.exists():
            curs = curs[0]
        cursor.execute('select * from verifieduserss(%s,%s,%s)',
                       [country, 0, clientid])
        user = cursor.fetchall()
        print('top influencer', user)

        cursor.execute('select * from returnpriceinfluencerwise(%s,%s)',
                       [userid, country])
        planprice = cursor.fetchall()
        print('influencer plan price', planprice)

        cursor.close()

        data = {'cur': curs, 'test': list(tes.values()), 'tk': tk, 'ig': ig,
                'fb': fb, 'yt': yt, 'video': vc, 'short': st,
                'greeting': gs, 'stand': standard, 'prem': premium,
                'basic': basic, 'vl': list(vl.values()), 'info1': user, 'choose': whychoose,
                'rule': gis, "footer": list(fot.values()), "seo": list(seo.values()),
                'ban': list(ban.values()), "info": info, 'ser': list(sr.values()),
                'link': base_url, 'tabtitle': stag, 'infoprice': planprice}
        data = json.dumps(data, default=str)
        return HttpResponse(data, content_type="application/json")

    path = "{0}".format(request.path)
    if username is not None:
        path = path[:11]

    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []

    # sys.stdout = open("services1.txt", "a")
    base_url = "{0}://{1}{2}".format(request.scheme,
                                     request.get_host(), request.path)
    print("Url", base_url)
    whychoose = []
    gis = []
    whychoose.clear()
    gis.clear()

    username = username.replace('-', ' ')
    print('user', username)
    userid = Allusers.objects.get(username=username).id
    print("userid", userid)
    info = InfluencerProfile.objects.get(influencer_userid=userid)
    
    print("information", info, info.fullname)
    
    sys.stdout = open("infocat.txt", "a")
    
    
    print("categories",info.categories)
    
    infocate=[]
    
    # for i in info.categories:
    #     catnma=Categories.objects.get(categorieid=int(i)).categoryname
    #     infocate.append(str(catnma))
 
    
    
    
    # sys.stdout.close()
    
    
    
    
    
    
    basic = PricingPlans.objects.filter(
        usersid=userid, plan_type='Basic', serviceid=1)
    if basic.exists():
        basic = basic[0]

    standard = PricingPlans.objects.filter(
        usersid=userid, plan_type='Standard',serviceid=1)
    if standard.exists():
        standard = standard[0]
    premium = PricingPlans.objects.filter(usersid=userid, plan_type='Premium',serviceid=1)
    if premium.exists():
        premium = premium[0]
    gs = PricingPlans.objects.filter(usersid=userid, serviceid=4)
    if gs.exists():
        gs = gs[0]
    vc = PricingPlans.objects.filter(usersid=userid, serviceid=2)
    if vc.exists():
        vc = vc[0]
    st = PricingPlans.objects.filter(usersid=userid, serviceid=3)
    if st.exists():
        st = st[0]
    sr = Services.objects.all().order_by('serviceid')

    print("Services", sr)

    # im = Images.objects.filter(im_userid=userid)
    # vd = Videos.objects.filter(vd_userid=userid)
    stag = Servicetabtitle.objects.filter(influencerid=userid)
    if stag.exists():
        stag = stag[0]
    vl = VideosLink.objects.filter(vl_userid=userid)
    
    infoseo=InfluencerSeoSettings.objects.filter(influencer_userid=userid)
    
    
    vlbd = vl.filter(videolinkpurpose='Brand Promotion').order_by('?')[:3]
    vlgm = vl.filter(videolinkpurpose='Greeting Messages').order_by('?')[:3]
    vlintst = vl.filter(videolinkpurpose='Insta Shoutout').order_by('?')[:3]
    vlytst = vl.filter(videolinkpurpose='Youtube Shoutout').order_by('?')[:3]

    pd = PlatformDetails.objects.filter(usersid=userid)
    tes = Testimonails.objects.filter(testimonails_approved=True)
    yt = pd.filter(platformtype=2)
    if yt.exists():
        yt = yt[0]
        follow = yt.subscribers_followers
        yt.subscribers_followers = numerize.numerize(follow)
    fb = pd.filter(platformtype=4)
    if fb.exists():
        fb = fb[0]
        follow = fb.subscribers_followers
        fb.subscribers_followers = numerize.numerize(follow)
    ig = pd.filter(platformtype=5)
    if ig.exists():
        ig = ig[0]
        follow = ig.subscribers_followers
        ig.subscribers_followers = numerize.numerize(follow)
    tk = pd.filter(platformtype=3)
    if tk.exists():
        tk = tk[0]
        follow = tk.subscribers_followers
        tk.subscribers_followers = numerize.numerize(follow)
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    ban = PageBanner.objects.all()
    why = info.chooseme
    if why is not None:
        for i in why:
            chos = Whychooseme.objects.get(whychoosemeid=i).Whychoosetext
            whychoose.append(chos)
    gigs = info.rulesforgig
    if gigs is not None:
        for i in gigs:
            rul = Rulesgig.objects.get(rulesid=i).rulesforgig
            gis.append(rul)
    country = get_location(request)
    cursor = connection.cursor()
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    cursor.execute('select * from verifieduserss(%s,%s,%s)',
                   [country, 0, clientid])
    user = cursor.fetchall()
    print('top influencer', user)

    cursor.execute('select * from returnpriceinfluencerwise(%s,%s)',
                   [userid, country])
    planprice = cursor.fetchall()
    print('influencer plan price', planprice)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username1 = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username1)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    # sys.stdout.close()
    cursor.close()

    return render(request, "Normal-User/services.html", {'cartdata': usctdata, 'ytvl': vlytst, 'insvl': vlintst, 'gmvl': vlgm, 'logininfo': influ, 'cur': curs, 'test': tes, 'tk': tk, 'ig': ig, 'fb': fb, 'yt': yt, 'video': vc, 'short': st, 'greeting': gs, 'stand': standard, 'prem': premium, 'basic': basic, 'vl': vlbd, 'info1': user, 'choose': whychoose, 'rule': gis, "footer": fot, "Seo1": seo,"Seo":seo1, 'ban': ban, "info": info, 'ser': sr, 'link': base_url, 'tabtitle': stag, 'infoprice': planprice, 'username': username, 'wishdata': myctdata, 'plink': path,'infocate':infocate,'infoseo':infoseo})


def Contactus(request):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    if (request.method == "POST"):
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if result['success']:
            sys.stdout = open("contact.txt", "a")
            Name = request.POST.get("Name")
            Email_id = request.POST.get("Email")
            Subject = request.POST.get("Subject")
            Message = request.POST.get('Message')
            ct = Contact(Name=Name, Email=Email_id,
                         Message=Message, Subject=Subject)
            ct.save()
            print("exeute")
            print("namd", Name, Email_id, Subject, Message)
            sys.stdout.close()
            messages.success(
                request, 'Your form is successfully submitted.')
        else:
            messages.warning(request,
                             'Invalid reCAPTCHA. Please try again.')
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    ban = PageBanner.objects.all()
    return render(request, "Normal-User/contact.html", {'cartdata': usctdata, 'logininfo': influ, "footer": fot, "Seo1": seo,"Seo":seo1, 'ban': ban, 'wishdata': myctdata, })


@csrf_exempt
def Contactusapi(request):

    if (request.method == "POST"):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            data = {"status": False, "message": "The token does not exists."}
            data = json.dumps(data, default=str)
            return HttpResponse(data, content_type="application/json", status=200)
        token = token.split(' ')[1]
        dtoken = decrypt(token)
        ck = Allusers.objects.filter(mobileapptoken=dtoken)
        if ck.exists() and len(ck) == 1:
            Name = request.POST.get("Name")
            Email_id = request.POST.get("Email")
            Subject = request.POST.get("Subject")
            Message = request.POST.get('Message')
            if Subject != None and len(Subject) != 0 and Message != None and len(Message) != 0 and Name != None and len(Name) != 0 and Email_id != None and len(Email_id) != 0:
                ct = Contact(Name=Name, Email=Email_id,
                             Message=Message, Subject=Subject)
                ct.save()
                message = 'Your contact form is successfully submitted.'
                data = {"status": True, "message": message}
                data = json.dumps(data, default=str)
                return HttpResponse(data, content_type="application/json", status=200)
            else:
                data = {"status": False, "message": "The values are missing."}
                data = json.dumps(data, default=str)
                return HttpResponse(data, content_type="application/json", status=200)
        else:
            data = {"status": False, "message": "User does not exists."}
            data = json.dumps(data, default=str)
            return HttpResponse(data, content_type="application/json", status=200)


def Privacy_Policy(request, var=None):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    if var == 'api':
        fot = FooterDetail.objects.all()
        ban = PageBanner.objects.all()
        sys.stdout = open("privcy.txt", "a")
        pri = PrivacyPolicyDetail.objects.all().order_by('id')
        pri = list(pri)
        num = 0
        number = len(pri)
        if number % 2 == 0:
            num = int(number/2)
        else:
            num = int(number/2)
            num = num+1
        list1 = pri[:num]
        list2 = pri[num:]
        comb = list(itertools.zip_longest(list1, list2, fillvalue=None))
        print("ban", pri, type(pri))

        data = {"footer": list(fot.values()), "pri": comb,
                'ban': list(ban.values())}
        data = json.dumps(data, default=str)
        return HttpResponse(data, content_type="application/json")

    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    ban = PageBanner.objects.all()
    sys.stdout = open("privcy.txt", "a")
    pri = PrivacyPolicyDetail.objects.all().order_by('id')
    pri = list(pri)
    num = 0
    number = len(pri)
    if number % 2 == 0:
        num = int(number/2)
    else:
        num = int(number/2)
        num = num+1
    list1 = pri[:num]
    list2 = pri[num:]
    comb = list(itertools.zip_longest(list1, list2, fillvalue=None))
    print("ban", pri, type(pri))
    sys.stdout.close()
    return render(request, "Normal-User/privacy-policy.html", {'cartdata': usctdata, 'logininfo': influ, "footer": fot, "pri": comb, 'ban': ban, 'wishdata': myctdata, "Seo1": seo,"Seo":seo1,})


def Terms_Of_Service(request, var=None):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    ter = TermsofServiceDetail.objects.all().order_by('id')
    ban = PageBanner.objects.all()
    ter = list(ter)
    num = 0
    number = len(ter)
    if number % 2 == 0:
        num = int(number/2)
    else:
        num = int(number/2)
        num = num+1
    list1 = ter[:num]
    list2 = ter[num:]
    comb = list(itertools.zip_longest(list1, list2, fillvalue=None))
    if var == 'api':
        data = {"footer": list(fot.values()), 'ter': ter,
                'ban': list(ban.values())}
        data = json.dumps(data, default=str)
        return HttpResponse(data, content_type="application/json")
    return render(request, "Normal-User/terms-of-service.html", {'cartdata': usctdata, 'logininfo': influ, "footer": fot, 'ter': comb, 'ban': ban, 'wishdata': myctdata,"Seo1": seo,"Seo":seo1, })


def Refund_Policy(request, var=None):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    ref = RefundPolicyDetail.objects.all().order_by('id')
    ban = PageBanner.objects.all()
    if var == 'api':
        data = {"footer": list(fot.values()), 'ref': list(
            ref.values()), 'ban': list(ban.values())}
        data = json.dumps(data, default=str)
        return HttpResponse(data, content_type="application/json")
    return render(request, "Normal-User/refund-policy.html", {'cartdata': usctdata, 'logininfo': influ, "footer": fot, 'ref': ref, 'ban': ban, 'wishdata': myctdata, "Seo1": seo,"Seo":seo1,})


def Whitepaper(request):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    return render(request, "Normal-User/white-paper.html", {'cartdata': usctdata, 'logininfo': influ, "footer": fot, "Seo1": seo,"Seo":seo1, 'wishdata': myctdata, })


def blogcatecount():
    cate = Blog.objects.values_list('blog_categories', flat=True)
    print('Categories', cate, type(cate))
    counts = Counter(cate)
    count_dict = dict(counts)
    for i in count_dict:
        print(i, count_dict[i])
        bcate = BlogCategory.objects.filter(blogcategory__icontains=i)
        if bcate.exists():
            bc = bcate[0]
            bc.blogcategory_count = count_dict[i]
            bc.save(update_fields=['blogcategory_count'])
            print("Function")
        else:
            bcate = BlogCategory(
                blogcategory=i, blogcategory_count=count_dict[i])
            bcate.save()
            print("execute")


def Blogs(request, var=None):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    if var == 'api':
        blogcatecount()
        blog = Blog.objects.all()
        base_url = "{0}://{1}{2}".format(request.scheme,
                                         request.get_host(), request.path)
        print("Url", base_url)
        fot = FooterDetail.objects.all()
        seo = Seo_Settings.objects.select_related('page').all()
        data = {"blogdeatils": list(blog.values()), "footer": list(
            fot.values()), "seo": list(seo.values()), 'link': base_url}
        data = json.dumps(data, default=str)
        return HttpResponse(data, content_type="application/json")

    blogcatecount()
    blog = Blog.objects.all()
    base_url = "{0}://{1}{2}".format(request.scheme,
                                     request.get_host(), request.path)
    print("Url", base_url)
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    return render(request, "Normal-User/blog.html", {'cartdata': usctdata, 'logininfo': influ, "blogdeatils": blog, "footer": fot, "Seo1": seo,"Seo":seo1, 'link': base_url, "wishdata": myctdata})


def Blogscate(request, cate, var=None):

    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    if var == 'api':
        blogcatecount()
        # cate = cate.replace('-', ' ')
        base_url = "{0}://{1}{2}".format(request.scheme,
                                         request.get_host(), request.path)
        print("Url", base_url)
        fot = FooterDetail.objects.all()
        
        seo = Seo_Settings.objects.select_related('page').all()
        blog = Blog.objects.filter(blog_categories__icontains=cate)
        data = {"blogdeatils": list(blog.values()), "footer": list(
            fot.values()), "seo": list(seo.values()), 'link': base_url}
        data = json.dumps(data, default=str)
        return HttpResponse(data, content_type="application/json")

    blogcatecount()
    cate = cate.replace('-', ' ')
    base_url = "{0}://{1}{2}".format(request.scheme,
                                     request.get_host(), request.path)
    print("Url", base_url)
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    blog = Blog.objects.filter(blog_categories__icontains=cate)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]
    return render(request, "Normal-User/blogs.html", {'cartdata': usctdata, 'logininfo': influ, "blogdeatils": blog, "footer": fot, "Seo1": seo,"Seo":seo1, 'link': base_url, 'wishdata': myctdata, })


@csrf_exempt
def Blog_Deatils_api(request, name, var=None):
    if var == 'api':
        base_url = "{0}://{1}{2}".format(request.scheme,
                                         request.get_host(), request.path)
        print("Url", base_url)

        blog = Blog.objects.all()
        bcate = BlogCategory.objects.all()
        blog1 = blog.order_by('-date').values()[0:5]
        bldet = Blog.objects.filter(title__icontains=name)[0]
        print("sdagf", bldet)
        bl = BlogComments.objects.filter(blog=bldet, isapproved=True)
        num = len(bl)
        print("number", num)
        if request.method == 'POST':
            token = request.META.get('HTTP_AUTHORIZATION', None)
            if not token:
                data = {"status": False, "message": "The token does not exists."}
                data = json.dumps(data, default=str)
                return HttpResponse(data, content_type="application/json", status=200)
            token = token.split(' ')[1]
            dtoken = decrypt(token)
            ck = Allusers.objects.filter(mobileapptoken=dtoken)
            if ck.exists() and len(ck) == 1:
                nam = request.POST.get("Name")
                mess = request.POST.get("Message")
                if nam != None and len(nam) != 0 and mess != None and len(mess) != 0:
                    bcom = BlogComments(blog=bldet, name=nam, Commenttext=mess)
                    bcom.save()
                    data = json.dumps(
                        {"status": True, "message": 'You have submited the comments and shown after approval.'}, default=str)
                    return HttpResponse(data, content_type="application/json", status=200)
                else:
                    data = {"status": False,
                            "message": "The values are missing."}
                    data = json.dumps(data, default=str)
                    return HttpResponse(data, content_type="application/json", status=200)
            else:
                data = {"status": False, "message": "The User does not exists."}
                data = json.dumps(data, default=str)
                return HttpResponse(data, content_type="application/json", status=200)

        data = {'det': bldet, "blogdeatils": blog, 'comm': list(
            bl.values()), 'rc': blog1, 'num': num, 'cate': list(bcate.values()), 'link': base_url}
        data = json.dumps(data, default=str)
        return HttpResponse(data, content_type="application/json")


def Blog_Deatils(request, name):
    # sys.stdout = open("blog-det.txt", "a")

    name = name.replace('-', ' ')
    print(name)
    base_url = "{0}://{1}{2}".format(request.scheme,
                                     request.get_host(), request.path)
    print("Url", base_url)
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    blog = Blog.objects.all()
    bcate = BlogCategory.objects.all()
    blog1 = blog.order_by('-date').values()[0:5]
    bldet = Blog.objects.filter(title__icontains=name)[0]
    print("sdagf", bldet)
    bl = BlogComments.objects.filter(blog=bldet, isapproved=True)
    num = len(bl)
    print("number", num)
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    if request.method == 'POST':
        nam = request.POST.get("Name")
        mess = request.POST.get("Message")
        if nam != None and mess != None:
            bcom = BlogComments(blog=bldet, name=nam, Commenttext=mess)
            bcom.save()
            print("Execute function")
            print(nam, mess)
            messages.warning(request,
                             'Your comment is successfully submitted and shows after approval.')
        # url=reverse('Blog_Deatils',args=['Travel'])
        # return redirect(url)
        sys.stdout.close()
        return redirect(request.META['HTTP_REFERER'])
    return render(request, "Normal-User/blog-details.html", {'cartdata': usctdata, 'logininfo': influ, "footer": fot, "Seo1": seo,"Seo":seo1, 'det': bldet, "blogdeatils": blog, 'comm': bl, 'rc': blog1, 'num': num, 'cate': bcate, 'link': base_url, 'wishdata': myctdata, })


@csrf_exempt
def blogslikes(request):
    if request.method == 'POST':
        posid = request.POST.get('postid')
        if posid is None or len(posid) == 0:
            posid = 0
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            data = {"status": False, "message": "The token does not exists."}
            data = json.dumps(data, default=str)
            return HttpResponse(data, content_type="application/json", status=200)
        token = token.split(' ')[1]
        dtoken = decrypt(token)
        ck = Allusers.objects.filter(mobileapptoken=dtoken)
        sys.stdout = open("tokenlist.txt", "a")
        print("original", token)
        print("user", ck)
        if ck.exists() and len(ck) == 1:
            print("exists")
            print(posid)
            if posid != 0:
                bl = Blog.objects.filter(blogid=int(posid))
                if bl.exists():
                    bl = bl[0]
                    count = bl.likes
                    bl.likes = count+1
                    bl.save(update_fields=['likes'])
                    data = {"status": True,
                            "message": "You have liked this blog."}
                    data = json.dumps(data, default=str)
                    return HttpResponse(data, content_type="application/json", status=200)
                else:
                    data = {"status": False,
                            "message": "Blog does not exists."}
                    data = json.dumps(data, default=str)
                    return HttpResponse(data, content_type="application/json", status=200)
            else:
                data = {"status": False, "message": "Blog does not exists."}
                data = json.dumps(data, default=str)
                return HttpResponse(data, content_type="application/json", status=200)
        else:
            data = {"status": False, "message": "User does not exists."}
            data = json.dumps(data, default=str)
            return HttpResponse(data, content_type="application/json", status=200)


def likes(request):
    if request.method == 'POST':
        posid = request.POST.get('task')
        print(posid)
        if posid != None:
            print("id:", posid)
            bl = Blog.objects.filter(blogid=int(posid))
            if bl.exists():
                bl = bl[0]
                count = bl.likes
                bl.likes = count+1
                bl.save(update_fields=['likes'])
        return HttpResponse(status=200)


@csrf_exempt
def convertrates(request):
    data = json.loads(request.body)
    Password = data['Password']
    if Password == "Njkfesbhd":
        print('calling celery task now...')
        startcelery_task = start_convertrates.delay()
    return HttpResponse(status=200)


def call_api(request):
    fot = FooterDetail.objects.all()
    cate1 = CastingCallCategories.objects.all()
    # sys.stdout = open("callcasting.txt", "a")
    curr = datetime.now().strftime("%Y-%m-%d")
    print("date", curr)
    country = get_location(request)
    if country is None:
        country = 'India'
    ccdet = Casting_Call.objects.filter(
        approved=True, expirydate__gte=curr, country=country)
    print("Bhaar", ccdet, len(ccdet))
    data = {"footer": list(fot.values()), "cate": list(
        cate1.values()), 'det': list(ccdet.values())}
    data = json.dumps(data, default=str)
    return HttpResponse(data, content_type="application/json")


def Call_Casting(request, cate=None, var=None):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    # print("ibndxdata", country)
    if country is None:
        country = 'India'
    # print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                # print("cartid", i.wishlistid)
                # print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        # print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                # print("cartid", i.Cartid)
                # print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        # print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    if var == 'api':
        fot = FooterDetail.objects.all()
        cate1 = CastingCallCategories.objects.all()
        # sys.stdout = open("callcasting.txt", "a")
        curr = datetime.now().strftime("%Y-%m-%d")
        print("date", curr)
        country = get_location(request)
        if country is None:
            country = 'India'
        if cate is not None and len(cate) > 1:
            catid = CastingCallCategories.objects.get(
                categoryname__icontains=cate).castingcallcategorieid
            ccdet = Casting_Call.objects.filter(
                categoryid=catid, approved=True, expirydate__gte=curr, country=country)
            print("Ander", ccdet, len(ccdet))
            data = {"footer": list(fot.values()), "cate": list(
                cate1.values()), 'det': list(ccdet.values())}
            data = json.dumps(data, default=str)
            return HttpResponse(data, content_type="application/json")

    sys.stdout = open("callcasting.txt", "a")
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    cate1 = CastingCallCategories.objects.all()
    cast=CastingCallPage.objects.all()
    # sys.stdout = open("callcasting.txt", "a")
    curr = datetime.now().strftime("%Y-%m-%d")
    # print("date", curr)
    country = get_location(request)
    if country is None:
        country = 'India'
    ccdet = Casting_Call.objects.filter(
        approved=True, expirydate__gte=curr, country=country)

    for i in ccdet:
        key = i.castingcallid
        i.castingcallid = encrypt(key)
        print(i)

    print("Bhaar", ccdet, len(ccdet))
    if cate is not None and len(cate) > 1:
        catid = CastingCallCategories.objects.get(
            categoryname__icontains=cate).castingcallcategorieid
        ccdet = Casting_Call.objects.filter(
            categoryid=catid, approved=True, expirydate__gte=curr, country=country)
        for i in ccdet:
            key = i.castingcallid
            i.castingcallid = encrypt(key)
        print("Ander", ccdet, len(ccdet))
        return render(request, "Normal-User/call-casting.html", {'cartdata': usctdata, 'logininfo': influ,"Seo1": seo,"Seo":seo1, "footer": fot, "Cate": cate1, 'det': ccdet, 'wishdata': myctdata, 'cast':cast})
    sys.stdout.close()
    return render(request, "Normal-User/call-casting.html", {'cartdata': usctdata, "Seo1": seo,"Seo":seo1,'logininfo': influ, "footer": fot, "Cate": cate1, 'det': ccdet, 'wishdata': myctdata, 'cast':cast})


def Call_Casting_Details(request, id=None, var=None):

    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    if var == 'api':
        fot = FooterDetail.objects.all()
        
        if id is not None:
            ccdet = Casting_Call.objects.filter(castingcallid=id)
            qn = Callcastingquestions.objects.filter(callcastid=id)
            if ccdet.exists():
                ccdet = ccdet[0]
                catid1 = ccdet.categoryid
                curr = datetime.now().strftime("%Y-%m-%d")
                ccdet1 = Casting_Call.objects.filter(
                    categoryid=catid1, approved=True, expirydate__gte=curr)
        data = {"footer": list(fot.values()), 'det': ccdet, 'sdet': list(
            ccdet1.values()), 'faq': list(qn.values())}
        data = json.dumps(data, default=str)
        return HttpResponse(data, content_type="application/json")

    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    if id is not None:
        # id = decrypt(id)
        
        sys.stdout = open("Pitchinginfoid.txt", "a")
        
        id = id.replace('-', ' ')
        print("vdcz",id)
        ccdet = Casting_Call.objects.filter(posttitle__icontains=id)
        print("data",ccdet)
        ccdet = ccdet[0]
        id=str(ccdet.castingcallid)
        request.session['callid'] = id
        qn = Callcastingquestions.objects.filter(callcastid=id)
        # if ccdet.exists():
        catid1 = ccdet.categoryid
        curr = datetime.now().strftime("%Y-%m-%d")
        ccdet1 = Casting_Call.objects.filter(
            categoryid=catid1, approved=True, expirydate__gte=curr)
        for i in ccdet1:
            key = i.castingcallid
            i.castingcallid = encrypt(key)
            print(i)
        sys.stdout.close()
        return render(request, "Normal-User/casting-call-details.html", {"Seo1": seo,"Seo":seo1,'cartdata': usctdata, 'logininfo': influ, "footer": fot, 'det': ccdet, 'sdet': ccdet1, 'faq': qn, 'wishdata': myctdata})
    return render(request, "Normal-User/casting-call-details.html", {"Seo1": seo,"Seo":seo1,'cartdata': usctdata, 'logininfo': influ, "footer": fot, 'det': ccdet, 'sdet': ccdet1, 'faq': qn, 'wishdata': myctdata})


@csrf_exempt
def ServicePostid(request):
    if request.method == 'POST':
        sys.stdout = open("services21345.txt", "a")
        print("asdffas", request.POST.get('bplanid'))
        request.session['bplanid'] = request.POST.get('bplanid')
        sys.stdout.close()
        return HttpResponse({'Result': 'Savedid'}, status=200)


@csrf_exempt
def Shoutservice(request):
    if request.method == 'POST':
        sys.stdout = open("services21345.txt", "a")
        print("asdffas", request.POST.get('bplanid'))
        request.session['stplanid'] = request.POST.get('bplanid')
        sys.stdout.close()
        return HttpResponse({'Result': 'Savedid'}, status=200)


@csrf_exempt
def Pitchinginfoid(request):
    if request.method == 'POST':
        sys.stdout = open("Pitchinginfoid.txt", "a")
        print("asdffas", request.POST.get('infoid'))
        request.session['pitchinfoid'] = request.POST.get('infoid')
        request.session['pitchid'] = request.POST.get('pitchid')
        request.session['callid'] = request.POST.get('callid')
        sys.stdout.close()
        return HttpResponse({'Result': 'Savedid'}, status=200)


@login_required
def Package(request, username=None):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    cursor = connection.cursor()
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username1 = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username1)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    ref = RefundPolicyDetail.objects.all()
    username = username.replace('-', ' ')
    print('user', username)
    userid = Allusers.objects.get(username=username).id
    print("userid", userid)
    info = InfluencerProfile.objects.get(influencer_userid=userid)
    print("information", info)
    cursor.execute('select * from returnpriceinfluencerwise(%s,%s)',
                   [userid, country])
    planprice = cursor.fetchall()
    print('influencer plan price', planprice)
    basic = PricingPlans.objects.filter(usersid=userid, plan_type='Basic')
    if basic.exists():
        basic = basic[0]
    standard = PricingPlans.objects.filter(
        usersid=userid, plan_type='Standard')
    if standard.exists():
        standard = standard[0]
    premium = PricingPlans.objects.filter(usersid=userid, plan_type='Premium')
    if premium.exists():
        premium = premium[0]
    sys.stdout = open("packagedetails.txt", "a")
    bplanid = request.session.get('bplanid', None)
    plant = PricingPlans.objects.get(planid=bplanid)
    plantype = plant.plan_type
    planprice = plant.increasedprice
    serid = plant.serviceid
    tax = ServiceTax.objects.all()[0]
    # otherchrge=plant.priorityprice
    otherchrge = 0
    if otherchrge is None:
        otherchrge = 0

    planprice = planprice+otherchrge
    taxamount = planprice * (int(tax.servicetaxpercent)/100)
    taxamount = math.ceil(taxamount)
    total = planprice+taxamount
    print('tax', tax.servicetaxpercent, type(tax), planprice, taxamount)
    print('Rahul', bplanid, plantype)
    sys.stdout.close()
    return render(request, "Normal-User/package.html", {'cartdata': usctdata, 'logininfo': influ, 'cur': curs, "footer": fot, 'info': info, 'refund': ref, 'stand': standard, 'prem': premium, 'basic': basic, 'infoprice': planprice, 'selectplan': plantype, 'prplan': plant, 'tax': taxamount, 'other': otherchrge, 'total': total, 'taxper': tax.servicetaxpercent, 'wishdata': myctdata, 'bsplanid': bplanid, 'serid': serid})


def PackagePlan(request):
    user = request.user.id
    id = Allusers.objects.filter(id=user)
    id = id[0]
    cls = ClientSettings.objects.filter(csettingsuserid=id)
    if cls.exists():
        cls = cls[0]
    if request.method == 'POST':
        sys.stdout = open("packageplandetails.txt", "a")

        if request.POST.get('coupon') != None:
            coupon = request.POST.get('coupon')
            serid = request.POST.get('serid')
            print("Service id", serid)
            print("Coupon id", coupon)
            # dis=Couponcodes.objects.get(couponterms=coupon).coupondiscount
            usdis = Couponcodes.objects.filter(
                couponterms=coupon, serviceid=serid)
            if usdis.exists():
                usdis = usdis[0]

                if usdis.activestatus == True and usdis.totalcodeused < usdis.codeusedlimit:
                    dis = usdis.coupondiscount
                    request.session['coup'] = coupon
                elif usdis.activestatus == True and usdis.totalcodeused >= usdis.codeusedlimit:
                    dis = -4
                    request.session['coup'] = ''
                else:
                    dis = -2
                    request.session['coup'] = ''
                cpid = usdis.couponcodesid
                uscd = Orders.objects.filter(
                    clientid=str(id), couponcodeid=str(cpid), iscouponapplied=True, paymentstatus=True)
                if uscd.exists():
                    dis = 0
                    request.session['coup'] = ''
            else:
                dis = -3
                request.session['coup'] = ''

            print("user", id)

            print("coupon", coupon)
            print("dis", dis)
        sys.stdout.close()
        return JsonResponse({'results': dis})


def EventPlan(request):
    user = request.user.id
    if request.method == 'POST':
        sys.stdout = open("Eventpaln.txt", "a")
        timefromid = request.POST.get('timefromid')
        timetoid = request.POST.get('timetoid')
        infoid = request.POST.get('infoid')
        t1 = Eventtime.objects.get(eventtimeid=timefromid).eventtime
        t2 = Eventtime.objects.get(eventtimeid=timetoid).eventtime
        t1 = datetime.combine(datetime.today(), t1)
        t2 = datetime.combine(datetime.today(), t2)
        t3 = t2-t1
        t3 = int(t3.total_seconds() / 3600)
        pr = PricingPlans.objects.get(
            usersid=infoid, plan_type='Influencer Acquisition', serviceid=5).finalamount

        eventprice = pr*t3
        print("infoid id", infoid)
        print("timetoid id", timetoid)
        print("timefromid id", timefromid)
        print("difference time", t3, type(t3))
        print("eventprice", eventprice)

        sys.stdout.close()
        return JsonResponse({'results': eventprice})


@login_required(login_url='/login/')
def My_Card(request):
    fot = FooterDetail.objects.all()
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country1 = get_location(request)
    if country1 is None:
        country1 = 'India'

    print("data", country1)
    curs = ExchangeRates.objects.filter(country__icontains=country1)
    if curs.exists():
        curs = curs[0]

    usctdata = []

    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                username = Allusers.objects.get(id=id3).username
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)
    return render(request, "Normal-User/addtocard.html", {"footer": fot, 'cartdata': usctdata})


@login_required(login_url='/login/')
def Influencer_Chat(request, username=None):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    cursor = connection.cursor()
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username1 = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username1)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]
    ref = RefundPolicyDetail.objects.all()
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()

    sys.stdout = open("influencerchatplandetails.txt", "a")

    username = username.replace('-', ' ')
    # print('user', username)
    userid = Allusers.objects.get(username=username).id
    # print("userid", userid)
    info = InfluencerProfile.objects.get(influencer_userid=userid)
    # print("information", info)
    vdct = PricingPlans.objects.filter(usersid=userid, plan_type='Video Chat')
    if vdct.exists():
        vdct = vdct[0]

    sdet = Slots.objects.filter(influencerid=userid)

    distinct_dates = Subslots.objects.filter(influencerid=userid, starttime__gt=timezone.now()).annotate(
        date=Cast('starttime', output_field=DateField())).values('date').distinct()

    timezone_name_1 = 'Asia/kolkata'
    timezone_name_2 = get_timezone(request)
    print("Sone", timezone_name_2)
    cursor = connection.cursor()
    cursor.execute("""
     with tbl as (
        SELECT starttime,
        starttime - (select utc_offset from pg_timezone_names where name ilike '%"""+timezone_name_1+"""%') as utctime
        FROM mainapp_subslots 
        WHERE influencerid = """ + str(userid) + """ AND starttime > NOW() AND isbooked IS FALSE AND isreferenced=FALSE
    ), tbl1 AS (
        SELECT *, utctime + (select utc_offset from pg_timezone_names where name ilike '%"""+timezone_name_2+"""%') AS countrytime 
        FROM tbl
    )
    SELECT DISTINCT (CAST(date(starttime) AS date)) AS dates, TO_CHAR(date(countrytime),'DD Mon YYYY') AS ctime 
    FROM tbl1
    """)
    print("Query", cursor.query)
    results = cursor.fetchall()
    print("dates", results)

    cursor.close()

    tax = ServiceTax.objects.filter(country__icontains=country)[0]
    sys.stdout.close()
    return render(request, "Normal-User/influencer-chat.html", {'cartdata': usctdata, 'footer': fot, 'info': info, 'refund': ref, 'logininfo': influ, 'wishdata': myctdata, 'vdct': vdct, 'cur': curs, 'sdet': sdet, 'taxpr': tax.servicetaxpercent, 'dates': distinct_dates, 'ddates': results})


@login_required(login_url='/login/')
def Greeting_Payment(request, username=None):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    cursor = connection.cursor()
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username1 = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username1)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]
    ref = RefundPolicyDetail.objects.all()
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()

    sys.stdout = open("greetingsplandetails.txt", "a")

    username = username.replace('-', ' ')
    # print('user', username)
    userid = Allusers.objects.get(username=username).id
    # print("userid", userid)
    info = InfluencerProfile.objects.get(influencer_userid=userid)
    # print("information", info)
    vdct = PricingPlans.objects.filter(
        usersid=userid, plan_type='Greeting Messages')
    if vdct.exists():
        vdct = vdct[0]
    temp = Templates.objects.filter(templatetype='Birthday')
    temp1 = Templates.objects.filter(templatetype='Anniversary')
    temp2 = Templates.objects.filter(templatetype='Wedding')
    temp3 = Templates.objects.filter(templatetype='Motivation')
    temp4 = Templates.objects.filter(templatetype='Others')

    # tup_temp = [(temp[i], temp[i+1]) if i+1 < len(temp) else (temp[i],) for i in range(0, len(temp), 2)]

    tax = ServiceTax.objects.filter(country__icontains=country)[0]
    sys.stdout.close()
    return render(request, "Normal-User/greeting-payment.html", {'cartdata': usctdata, 'footer': fot, 'info': info, 'refund': ref, 'logininfo': influ, 'wishdata': myctdata, 'vdct': vdct, 'cur': curs, 'taxpr': tax.servicetaxpercent, 'temp': temp, 'temp1': temp1, 'temp2': temp2, 'temp3': temp3, 'temp4': temp4})


def Influencer_Meet(request, username=None):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    cursor = connection.cursor()
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username1 = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username1)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]
    ref = RefundPolicyDetail.objects.all()
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()

    username = username.replace('-', ' ')
    # print('user', username)
    userid = Allusers.objects.get(username=username).id
    # print("userid", userid)
    info = InfluencerProfile.objects.get(influencer_userid=userid)
    # print("information", info)
    vdct = PricingPlans.objects.filter(
        usersid=userid, plan_type='Influencer Acquisition')
    if vdct.exists():
        vdct = vdct[0]

    days = next30days()

    et = Eventtype.objects.all()
    etm = Eventtime.objects.all()

    tax = ServiceTax.objects.filter(country__icontains=country)[0]
    sys.stdout.close()
    return render(request, "Normal-User/influencer-meet.html", {'cartdata': usctdata, 'footer': fot, 'info': info, 'refund': ref, 'logininfo': influ, 'wishdata': myctdata, 'vdct': vdct, 'cur': curs, 'taxpr': tax.servicetaxpercent, 'dates': days, 'event': et, 'time1': etm})


def VideochatPrice(request):
    # user=request.user.id
    # id = Allusers.objects.filter(id=user)
    # id = id[0]
    # cls = ClientSettings.objects.filter(csettingsuserid=id)
    # if cls.exists():
    #     cls = cls[0]
    if request.method == 'POST':
        sys.stdout = open("Videochatplandetails.txt", "a")
        # print('totaldata',request.POST)
        if request.POST.get('selecteddate') != None:
            selecteddate = request.POST.get('selecteddate')

        if request.POST.get('infoid') != None:
            infoid = request.POST.get('infoid')

        subslotsdata = Subslots.objects.filter(
            influencerid=infoid,
            starttime__date=selecteddate,
            isbooked=False,
            isreferenced=False
        ).annotate(
            starttime_formatted=Cast('starttime', output_field=TimeField()),
            endtime_formatted=Cast('endtime', output_field=TimeField())
        ).values(
            'subslotid',
            'starttime_formatted',
            'endtime_formatted',
            'slotprice',
            'slotduration'
        )

        print(subslotsdata, type(subslotsdata))

        country = get_location(request)

        if country is None:
            country = 'India'
            print("data", country)

        timezone1 = get_timezone(request)

        for subslot in subslotsdata:
            print("Tiem", subslot['starttime_formatted'],
                  type(str(subslot['starttime_formatted'])))
            subslot['starttime_formatted'] = str(
                subslot['starttime_formatted'])
            starttime_formatted = convert_utc_to_current_timezone(
                subslot['starttime_formatted'], timezone1)
            starttime_formatted = changetimeaccording_to_country(
                str(starttime_formatted), country)
            subslot['starttime_formatted'] = starttime_formatted
            subslot['endtime_formatted'] = str(subslot['endtime_formatted'])
            endtime_formatted = convert_utc_to_current_timezone(
                subslot['endtime_formatted'], timezone1)
            endtime_formatted = changetimeaccording_to_country(
                str(endtime_formatted), country)
            subslot['endtime_formatted'] = endtime_formatted

        resslots = json.dumps(list(subslotsdata.values()), default=str)
        request.session['slotsdata'] = resslots
        # print("selectef timings",subslotsdata,"\n",list(subslotsdata.values()))

        # print("asdr",selecteddate,time,infoid,record)
        return JsonResponse({'results': list(subslotsdata)})


def Videochattime(request):

    if request.method == 'POST':
        sys.stdout = open("Timeplandetails.txt", "a")

        time = request.POST.get('time')
        print("time", time)
        rst = Subslots.objects.get(subslotid=time).recordingprice
        rst = str(rst)
        print("price", rst)

        my_list_json = request.session.get('slotsdata')
        my_list = json.loads(my_list_json)
        # print("Rahul")
        # print("Rahul",my_list)
        sys.stdout.close()
        return JsonResponse({'results': my_list, 'recprice': rst})


def Videochatrecord(request):

    if request.method == 'POST':
        sys.stdout = open("Recordplandetails.txt", "a")

        if request.POST.get('record') != None:
            record = request.POST.get('record')
            print("record", record)

            time = request.POST.get('time')
            print("time", time)
            if record == 'true':
                recpr = Subslots.objects.get(subslotid=time).recordingprice
            else:
                recpr = 0
            recpr = str(recpr)
            print("price", recpr)
            # rst = Subslots.objects.filter(subslotid=time)

            # if rst.exists():
            #     rst = rst[0]
            #     rst.recordingrequired = True
            #     rst.save(update_fields=['recordingrequired'])
            #     print("execute recording")

        sys.stdout.close()
        return JsonResponse({'recprice': recpr})


def Career(request):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    print("ibndxdata", country)
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    career = Careerpage.objects.all()
    review = EmployeeReview.objects.all()
    job = Jobhiring.objects.all()

    if request.method == 'POST':
        sys.stdout = open("carrerform.txt", "a")
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if result['success']:
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            number = request.POST.get('number')
            jobhiringid = request.POST.get('jobhiringid')
            photo = request.FILES.get("upload")
            print(email, jobhiringid, number, firstname, lastname, photo)
            jdid = Jobhiring.objects.filter(jobhiringid=str(jobhiringid))
            print("data", jdid)
            if jdid.exists():
                jdid = jdid[0]
                print("inner", jdid)
                auser = Appliedcandidates(firstname=firstname, lastname=lastname, email=email, phone=int(
                    number), file=photo, jobhiringid=jdid)
                auser.save()
                print("Save jobs")
        sys.stdout.close()
    return render(request, "Normal-User/career.html", {'review': review, 'cartdata': usctdata, 'logininfo': influ, "footer": fot, "Seo1": seo,"Seo":seo1, 'wishdata': myctdata, 'career': career, 'job': job})


@csrf_exempt
def ankit(request):
    sys.stdout = open("ankitdetails.txt", "a")
    data = request.body
    data = json.loads(data)
    print("data", data)
    sys.stdout.close()
    return JsonResponse({'recprice': data})


logger = logging.getLogger()
fh = logging.FileHandler('mainapp_view_log.txt')
logger.addHandler(fh)


@login_required(login_url='/login/')
def Shoutout_Payment(request, username=None):
    clientid = request.user.id
    if clientid is None:
        clientid = 0
    country = get_location(request)
    cursor = connection.cursor()
    if country is None:
        country = 'India'
    print("data", country)
    curs = ExchangeRates.objects.filter(country__icontains=country)
    if curs.exists():
        curs = curs[0]
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.wishlistid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                wishlistid = i.wishlistid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3)
                myctdata.append(locct)
        print("listdata", myctdata)

    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username1 = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(usersid=id3, plan_type='Basic')
                basicpr = pr.increasedprice
                Cartid = i.Cartid
                curre = str(curs.currency)
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username1)
                usctdata.append(locct)
        print("mycartdata", usctdata)

    influ = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    if influ.exists():
        influ = influ[0]
    else:
        influ = ClientProfile.objects.filter(client_userid=request.user.id)
        if influ.exists():
            influ = influ[0]

    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()
    ref = RefundPolicyDetail.objects.all()
    username = username.replace('-', ' ')
    print('user', username)
    userid = Allusers.objects.get(username=username).id
    print("userid", userid)
    info = InfluencerProfile.objects.get(influencer_userid=userid)
    print("information", info)
    sys.stdout = open("packagedetails.txt", "a")
    bplanid = request.session.get('stplanid', None)
    plant = PricingPlans.objects.filter(serviceid=bplanid)
    basic = plant.filter(plan_type='Basic')
    stand = plant.filter(plan_type='Standard')
    prem = plant.filter(plan_type='Premium')
    tax = ServiceTax.objects.all()[0]
    stand1 = None
    if stand.exists():
        stand1 = stand[0]
    price = stand1.increasedprice
    bsplanid = stand1.planid
    taxamount = price * (int(tax.servicetaxpercent)/100)
    taxamount = math.ceil(taxamount)
    total = price+taxamount
    print("data is",prem)
    sys.stdout.close()
    return render(request, "Normal-User/shoutout-pay.html", {'bsplanid': bsplanid, 'total': total, 'taxamount': taxamount, 'prem': prem, 'stand': stand, 'basic': basic, 'cartdata': usctdata, 'logininfo': influ, 'cur': curs, "footer": fot, 'info': info, 'refund': ref, 'taxper': tax.servicetaxpercent, 'wishdata': myctdata, 'stprice': plant})
