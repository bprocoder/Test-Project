from django.shortcuts import render,HttpResponse, redirect, get_object_or_404
from django.shortcuts import  HttpResponseRedirect
from django.db.models import Q
import phonenumbers
import requests
import random
import string
import json
from .models import *
import sys
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import jwt
import base64
import uuid
from datetime import datetime, timedelta
import pycountry
from mainapp.models import *
from django.db import connection
from django.contrib.auth.hashers import make_password
import time
from Admin.models import UserReferral
import ipaddress
from django.core.exceptions import ObjectDoesNotExist



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    port = request.META['SERVER_PORT']
    # #sys.stdout = open("ip.txt", "a")
    print("IP", ip, port)
    return ip+"-"+port


def get_location(request):
    ip_address = get_client_ip(request)
    # # #sys.stdout = open("country.txt", "a")
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
    
    
    # sys.stdout = open("country.txt", "a")
    # ip = ip_address.split("-")[0]
    # # for Iv6 Address
    # # if ':' in ip:
    # #     print("ip_Address", ip_address)
    # #     response = requests.get(f"https://ipinfo.io/{ip}/json")
    # #     if response.status_code == 200:
    # #         data = response.json()
    # #         print("Data", data)
    # #         country_code = data["country"]
    # #         country = pycountry.countries.get(alpha_2=country_code)
    # #         # print(f"Country name: {country.name}")
    # #         return country.name
    # # else:
    # #     # For IpV4
    # #     response = requests.get(
    # #         'https://get.geojs.io/v1/ip/geo/'+ip+'.json').json()
    # #     print("data1", response)
    # #     country = response.get('country')
    # #     # print("country", country)
    # #     return country
    
    # try:
    #     ip_version = ipaddress.ip_address(ip).version
        
    #     # Determine the correct model based on IP version
        
    #     print('ip ',ip)
    #     if ip_version == 4:
    #         model = IPV4
    #         print('execute ipv4')
    #         parts = ip.split(".")
    #         start_value = ".".join(parts[:2])
    #     elif ip_version == 6 and ':' in ip:
    #         model = IPV6
    #         print('execute ipv6 rb')
    #         parts = ip.split(":")
    #         start_value = ":".join(parts[:2])
    #     else:
    #         print('nio ip')
            
    #         raise ValueError("Invalid IP version")  # This will be caught by the outer exception

    #     # Try to get the country
    #     county=model.objects.get(ip_address__startswith=start_value).country
    #     print('datasdgdfgfhg',county)
        
    #     return county

    # except ObjectDoesNotExist:
    #     print('execute doesnot exists')
        
    #     return 'India'
    # except ValueError:
    #     print('execute value error')
        
    #     return 'India'
    

def send_msg_whatsapp(mobile,msg):
    req_data = {"sender": "917807404040", 
    "to": mobile,
    "type": "text",    
    "data": {
    "preview_url":"false",
    "body": f"{msg}"}}
    r = requests.post('https://chat.bol7.com/api/whatsapp/send', json=req_data)
    # return HttpResponse(r.text)
    # return JsonResponse({'status':'ok'})



def hit_api(link,mobile):
    # whatsapp_user.saves(mobile=mobile)
    req_data = {"sender":"917807404040",
    "to":mobile,
    "type":"image",
    "data":{
    "link":"https://influencerhiring.com/media/images/websitethumb.jpg",
    "caption":f"click here to {link}"
    }
}
    r = requests.post('https://chat.bol7.com/api/whatsapp/send', json=req_data)
    # return HttpResponse(r.text)
    print('link sended to user')
    return JsonResponse({'status':'ok'})




def generate_jwt(username,mobile, password=None,key=None):
    expiration_minutes=720
    expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)

    payload = {
        "username": username,
        "password": password,
        "mobile":mobile,
        "exp": expiration_time.timestamp()
    }
    
    secret = 'tmzHcYuvLUhxjcxZ4k_iqfCx-HUq6PCvdbXr4vOC5B4='
    token = jwt.encode(payload, secret, algorithm='HS256')
    
    UsedJWToken.objects.create(token_id=token,status=False)
    if key=="login":
        print('login token',token)
        user_register_link = 'login'+'\n'+f'https://influencerhiring.com/Loginappuser/{token}/'

        # print('login link',url_shortner(user_register_link))
    else:
        print('register token',token)
        user_register_link = 'register'+'\n'+f'https://influencerhiring.com/whatsapplogin/{token}/'
        # print('register link',url_shortner(user_register_link))

    return user_register_link


def decode_jwt_get_userdata(token):
    secret = 'tmzHcYuvLUhxjcxZ4k_iqfCx-HUq6PCvdbXr4vOC5B4='
    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
        password = payload.get('password', '')
        username = payload.get('username', '')
        mobile = payload.get('mobile', '')
        
        return {'username':username, 'password':password,"mobile":mobile,}
        # Populate the form with phone and username, or process further
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}


def generate_password(length):     
    characters = string.ascii_letters + string.digits + string.punctuation 
    password = ''.join(random.choice(characters) for i in range(length)) 
    return password



def reisteruser(username,mob_no):
    sys.stdout = open("offerpost.txt", "a")
    #############################################################################################
    
    #############################################################################################

    print(username,mob_no)
    try:
        actype ='client'
        pward = generate_password(8)
        print("fsdg", pward)
        cursor = connection.cursor()
        hashpass = make_password(pward)
        print('This is haspass',hashpass)
        cursor.execute('call userscreation(%s,%s,%s,%s,%s)',
                    (username, hashpass, None, actype, 0))
        user = cursor.fetchall()[0][0]
        cursor.close()
        use=Allusers.objects.get(id=user)
        print('this is created user',use)
        appuser=Whatsappuser(clientid=use,access_id=pward,secret_id=hashpass)
        print('this is appuser',appuser)
        appuser.save()
        
        use.is_active=True
        clt=ClientProfile.objects.get(client_userid=user)
        clt.mobile=mob_no
        use.save()
        clt.save()
        print('generating jwt link to register user')
        link = generate_jwt(username=username,mobile=mob_no,password=pward,key=None)
        print(link)
        hit_api(link,mob_no)
        # password_user_id = f"""🌟 Welcome to Influencer Hiring! 🌟\n\nTo get started quickly, you can use the temporary credentials below to log in:\nuser id- {username} (This is your unique identifier and cannot be changed)\npassword- {pward}\n\n🔒 Please, set your email and password immediately once you log in to ensure your account's security."""
        # send_msg_whatsapp(mob_no,password_user_id)
        
        
        
        
        sys.stdout = open("offerpost.txt", "a")
        print('beforesave generate_referral_id',use)
        # generate_referral_id = UserReferral(
        # user=use, referral_id='CPA'+use.username+'_'+str(int(time.time())), potential_referral_count_detail={'all': []})
        # generate_referral_id.save()
    except:
        print('user does not exists')
        msg='User is already registered'
        send_msg_whatsapp(mob_no,msg)



@csrf_exempt
def Whatsapp_webhook(request):
    sys.stdout = open('whatsapp_webhook_data.txt', 'a')
    print(request.body)
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        recived_msg = data['message']
        mob_no = data['number']
        username = str(data['name'].split(' ')[0].lower()) + str(mob_no[-4:])

        if recived_msg == 'I Want To Register My Self':
            already_reagister_no = Mobilelist()
            if int(mob_no) in already_reagister_no:
                print('user no and all user no',mob_no,already_reagister_no)
                msg='User is already registered Please Log In'
                send_msg_whatsapp(mob_no,msg)
            else:
                reisteruser(username,mob_no)
            

        if recived_msg == 'I Need To Login':
            username=username.lower()
            try:
                user=Allusers.objects.get(username=username)
                link = generate_jwt(username,mob_no,key='login')
                print(link)
                hit_api(link,mob_no)                
            except:
                reisteruser(username,mob_no)

                
                    
                
            # phone=None
            # if user.roles=='client':
            #     phone=ClientProfile.objects.get(client_userid=user.id).mobile
            # if user.roles=='influencer':
            #     phone=InfluencerProfile.objects.get(influencer_userid=user.id).mobile
            # if user.roles=='agency':
            #     phone=AgencyProfile.objects.get(agency_userid=user.id).mobile
            # if mob_no==phone:
            #     passw=user.password
            #     link = generate_jwt(username,passw,mob_no)
            #     hit_api(link,mob_no)       
            
            

        return JsonResponse({'status':'ok','message':'data recived sucessfully!!'})
    
    
    
def Mobilelist():

    # Query the InfluencerProfile model for mobile numbers
    influencer_mobiles = InfluencerProfile.objects.filter(
        ~Q(mobile=None)
    ).values_list('mobile', flat=True)

    # Query the ClientProfile model for mobile numbers
    client_mobiles = ClientProfile.objects.filter(
        ~Q(mobile=None)
    ).values_list('mobile', flat=True)

    # Query the AgencyProfile model for mobile numbers
    agency_mobiles = AgencyProfile.objects.filter(
        ~Q(mobile=None)
    ).values_list('mobile', flat=True)

    # Combine the mobile numbers from all three models into a single list
    mobile_numbers = list(influencer_mobiles) + list(client_mobiles) + list(agency_mobiles)

    # Remove duplicates from the list (if needed)
    unique_mobile_numbers = list(set(mobile_numbers))
    
    return unique_mobile_numbers
    
    
    
def Loginappuser(request,token):
    sys.stdout = open("infocat.txt", "a")
    data=decode_jwt_get_userdata(token)
    print('data',data)
    mob=data['mobile']
    
    token_status = UsedJWToken.objects.get(token_id=token).status
    if 'error' not in  data.keys():
        if token_status==True:
            print('link is already user')
            msg='link is already used.'
            send_msg_whatsapp(mob,msg)
            return HttpResponseRedirect("/login/")
        else:
            try:
                username=data['username']
                user = Allusers.objects.get(username=username)
                print("user",user)
                print("username",username)
                print("psssword",user.password)
                ppassw=Whatsappuser.objects.get(clientid=username).access_id
                print('----->>',ppassw)
                user = authenticate(request, username=username, password=ppassw)
                if user is not None and user.is_active == True:
                    print("user",user)
                    print("username",username)
                    login(request, user)
                    print('user logged in sucessfully!!')
                    usedtoken=UsedJWToken.objects.get(token_id=token)
                    usedtoken.status=True
                    usedtoken.save()
                    try:
                        ip_add = get_client_ip(request)
                        ln = LoginIP(userid=user.id, username=username, IP_Address=ip_add, location=get_location(
                                    request), sessionkey=request.session.session_key, device=request.META.get('HTTP_USER_AGENT', ''))
                        ln.save()
                    except:
                        pass
                    if user.profilestatus != True:
                        return HttpResponseRedirect("/Select-Account-Type/")
                    else:
                        return HttpResponseRedirect("/")
                    
            except:
                print('user does not exists')
                msg='User Does not exists'
                send_msg_whatsapp(mob,msg)
    else:
        print('exsisrdas')
        msg='Link is expired'
        send_msg_whatsapp(mob,msg)
    
    

# """
# if user.profilestatus != True:
                # return HttpResponseRedirect(f"/Select_Account_for_whatsapp/{token}/")
# """

 ################# to register user through whatsapp ##################

from django.contrib.auth import authenticate, login
    
def whatsapplogin(request,token):
    sys.stdout = open("infocat.txt", "a")
    
    print('token',token)
    
    data=decode_jwt_get_userdata(token)
    print(data)
    mob=data['mobile']
    print('this is mobile',mob)
    print('data',data)
    if 'error' not in  data.keys():
        username=data['username']
        username=username.lower()
        passw=data['password']
        mob=data['mobile']
        
        token_status = UsedJWToken.objects.get(token_id=token).status
        try:
            user = authenticate(request, username=username, password=passw)
            if user is not None:
                # Log in the user
                if token_status==True:
                    print('link is already user')
                    msg='link is already used.'
                    send_msg_whatsapp(mob,msg)
                    return HttpResponseRedirect("/login/")
                else:
                    login(request, user)
                    if user.is_active == True and request.user.profilestatus==False:
                        print('inner execute')
                        usedtoken=UsedJWToken.objects.get(token_id=token)
                        usedtoken.status=True
                        usedtoken.save()
                        return HttpResponseRedirect("/Select-Account-Type/")
                    else:
                        usedtoken=UsedJWToken.objects.get(token_id=token)
                        usedtoken.status=True
                        usedtoken.save()
                        return HttpResponseRedirect("/")
                            # Redirect to the home page or any other desired page
            else:
                msg='Invalid username or password.'
                send_msg_whatsapp(mob,msg)
                # return HttpResponse( "Invalid username or password.")
        except:
            print('user does not exists')
            msg='User Does not exists'
            send_msg_whatsapp(mob,msg)
            # return HttpResponse('User Does not exists')
    else:
        print('exsisrdas')
        msg='Link is expired'
        send_msg_whatsapp(mob,msg)
        # return HttpResponse('Link is expired')

#############################################################################

############### IMPLIMENTING URL SHORTNER #######################

def url_shortner(log_url):
    print('this is get url',log_url)
    obj = ShortURL.objects.create(long_url=log_url)
    short_url = "http://your-domain.com/" + obj.short_code
    print('this is short url',short_url)
    return short_url


def redirect_view(request, short_code):
    obj = get_object_or_404(ShortURL, short_code=short_code)
    return redirect(obj.long_url)