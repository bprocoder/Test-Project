from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import *
from datetime import datetime
import pytz
import requests
from threading import local
from telegram import Bot
from threading import Thread
import asyncio
#send image to frontend
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from agora_chat.models import *
from mainapp.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.exceptions import ObjectDoesNotExist

from mainapp.models import *

################ send notification to whatsapp ###############

def send_msg_whatsapp(mobile,msg):
    req_data = {"sender":"917807404040",
    "to":mobile,
    "type":"image",
    "data":{
    "link":"https://www.influencerhiring.com/media/images/websitethumb.jpg",
    "caption":f"{msg}"
    }
    }
    r = requests.post('https://chat.bol7.com/api/whatsapp/send', json=req_data)

def sendmessagetouseratwhatsapp(user,msg):
    userrole = Allusers.objects.get(id=user).roles
    try:
        if userrole == 'client':
            usermobile = ClientProfile.objects.get(client_userid=user).mobile
            send_msg_whatsapp(usermobile,msg)
        elif userrole == 'agency':
            usermobile = AgencyProfile.objects.get(agency_userid=user).mobilex
            send_msg_whatsapp(usermobile,msg)
        elif userrole == 'influencer':
            usermobile = InfluencerProfile.objects.get(influencer_userid=user).mobile
            send_msg_whatsapp(usermobile,msg)
    except:
        pass
    
    
    return JsonResponse({'user':user})

################################################################

######################################
########### TELEGRAM BOT #############
######################################

# Your telegram bot token
TOKEN = "6482018182:AAFuz1PHgd2P57BTYOwY30hwmqyf8fs7OHc"


@csrf_exempt  # Disable CSRF protection for this view
def telegram_webhook(request):
    # Open a log file to capture debug data
    sys.stdout = open("telegram_webhook_data.txt", "a")

    # Check if the request is a POST request
    if request.method == 'POST':
        # Parse the JSON payload
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        
        # Extract required fields
        update_id = data.get("update_id", None)
        message_data = data.get("message", {})
        chat_id = message_data.get("chat", {}).get("id", None)
        text = message_data.get("text", "")
        
        unique_identifier = None  # Initialize unique identifier

        # Check if the text starts with '/start'
        if text.startswith("/start"):
            try:
                _, unique_identifier = text.split(" ", 1)
            except ValueError:
                pass  # No unique identifier provided

            if unique_identifier:
                print(f"Received unique identifier {unique_identifier} from chat ID {chat_id}")
                obj, created = TelegramNotification.objects.update_or_create(user_id=unique_identifier,
                                                                                defaults={
                                                                                    'chat_id': chat_id,
                                                                                    }
                                                                            )
                # chat_id_in_db = TelegramNotification.objects.get(user_id=unique_identifier).chat_id
                # print('this is chat id',chat_id_in_db)
                # send_message(chat_id_in_db,'Welcome to Influencer Hiring\n\nFrom now on you will recive your personalize notifications here.')
                send_telegram_image('Welcome to Influencer Hiring','From now on you will recive your personalize notifications here.','#',unique_identifier)
                
        # Acknowledge receipt of the update
        return JsonResponse({"status": "ok"})

    # If it's not a POST request
    return JsonResponse({"status": "not ok"})


def send_message(chat_id, message_text):
    # print('getting here')
    # chat_id_in_db = TelegramNotification.objects.get(user_id=userid).chat_id
    payload = {
        'chat_id': chat_id,
        'text': message_text,
    }
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=payload)


#telegram notification sending...
async def serve_image_from_static(heading,body,url,chatid):
    sys.stdout = open("telegramres.txt", "a")
    msg=f'<a href="https://www.influencerhiring.com/{url}/"><b>{heading}</b></a>\n\n{body}'
    # msg1=msg.replace('.', '\.').replace('-', '\-').replace('!', '\!')
    # Define the path to the image
    image_path = os.path.join(settings.MEDIA_ROOT, 'images/websitethumb.jpg')
    print('A')
    bot = Bot(token=TOKEN)
    print('B')
    # try:
    #     chatid = TelegramNotification.objects.get(user_id=userid).chat_id
    # except ObjectDoesNotExist:
    #     # Handle the case where the specified userid doesn't exist in the database
    #     chatid = ''
    print('this is chat id:- ',chatid)
    
    response = await bot.send_photo(chat_id=chatid, photo=open(image_path, 'rb'), caption=msg, parse_mode='HTML')
    # print(response,4444444)

    return JsonResponse({'status': 'ok'})

def send_telegram_image(heading,body,url,unique_identifier):
    try:
        chatid = TelegramNotification.objects.get(user_id=unique_identifier).chat_id
        asyncio.run(serve_image_from_static(heading,body,url,chatid))
        return JsonResponse({'status': 'ok'})
    except ObjectDoesNotExist:
        # Handle the case where the specified userid doesn't exist in the database
        chatid = ''
        print('chat id does not exist--!!',chatid)
        # asyncio.run(serve_image_from_static(heading,body,url,chatid))
        
        return JsonResponse({'status': 'not ok'})


def sendmessagetelegram(request):
    # send_telegram_image('Welcome to Influencer Hiring!!','Now! You will recieve your personalise notification here.','#')
    pass


######################################################################################################################
######################################################################################################################


def notificationstatus(request):
    # sys.stdout = open("send_Influencer_count_notification.txt", "a")
    user_notifications = notification.objects.filter(user=request.user.id).values().order_by('-timestamp')
    unread_notifications = [n for n in user_notifications if n['read']==False]
    unread_notifications_no = len(unread_notifications)
    
    # print('this is notifications:---',unread_notifications)
    # print('this is notification nombers:---',unread_notifications_no)
    if unread_notifications_no > 0 :
        unread_status = True
        notifications = unread_notifications
    else:
        # print('getting here B')
        unread_status = False
        notifications = [n for n in user_notifications][:5]
    # print(notifications)
    return JsonResponse({'data':notifications,'unread_status':unread_status,'unread_count':unread_notifications_no})

# update status of notification
def updatenotificatoinreadstatus(request):
    username = request.user.id
    notifications = notification.objects.filter(user=username,read=False).update(read=True)
    return JsonResponse({'statusupdated':True})



import sys

def format_string(s, **kwargs):
    try:
        return s.format(**kwargs)
    except KeyError:
        return s

def sendusernotification(user,key,RM_Name,Influencer_Name,Product_Name,Decline_Reason,Order_Id,user_name=None):
    sys.stdout = open("sendInfluencernotification.txt", "a")
    print('inside sendusernotification')
    # print('Users careayion')
    # print(user,key,RM_Name,Influencer_Name,Product_Name,Decline_Reason,Order_Id)
    keyword = key
    user = user
    icon = clientnotification.objects.get(name=keyword).icon
    heading = format_string(clientnotification.objects.get(name=keyword).head, RM_Name=RM_Name,Influencer_Name=Influencer_Name,Product_Name=Product_Name,Decline_Reason=Decline_Reason,Order_Id=Order_Id,user_name=user_name)
    body = format_string(clientnotification.objects.get(name=keyword).body, RM_Name=RM_Name,Influencer_Name=Influencer_Name,Product_Name=Product_Name,Decline_Reason=Decline_Reason,Order_Id=Order_Id,user_name=user_name)
    redirect = clientnotification.objects.get(name=keyword).redirect_link
    username=Allusers.objects.get(id=user)
    time = datetime.now(pytz.utc)
    noti = notification.objects.create(title=heading,message=body,user=username,icon=icon,timestamp=time,redirect_link=redirect)
    #response=send_telegram(heading,body)
    send_telegram_image(heading,body,redirect,user)
    # print('last execute')
    msg = str(heading)+'\n\n'+str(body)
    sendmessagetouseratwhatsapp(user,msg)

def sendagencynotification(user,key,castingcallid,RM_Name,Influencer_Name,Product_Name,Decline_Reason,Order_Id):
    
    print('Users careayion')
    print(user,key,castingcallid,RM_Name,Influencer_Name,Product_Name,Decline_Reason,Order_Id)
    keyword = key
    user = user
    icon = BrandOrAgencynotification.objects.get(name=keyword).icon
    heading = format_string(BrandOrAgencynotification.objects.get(name=keyword).head, castingcallid=castingcallid,RM_Name=RM_Name,Influencer_Name=Influencer_Name,Product_Name=Product_Name,Decline_Reason=Decline_Reason,Order_Id=Order_Id)
    body = format_string(BrandOrAgencynotification.objects.get(name=keyword).body, castingcallid=castingcallid,RM_Name=RM_Name,Influencer_Name=Influencer_Name,Product_Name=Product_Name,Decline_Reason=Decline_Reason,Order_Id=Order_Id)
    redirect = BrandOrAgencynotification.objects.get(name=keyword).redirect_link
    username=Allusers.objects.get(id=user)
    time = datetime.now(pytz.utc)
    noti = notification.objects.create(title=heading,message=body,user=username,icon=icon,timestamp=time,redirect_link=redirect)
    #response=send_telegram(heading,body)
    send_telegram_image(heading,body,redirect,user)
    # print('last execute')
    msg = str(heading)+'\n\n'+str(body)
    sendmessagetouseratwhatsapp(user,msg)


def sendInfluencernotification(user,key,RM_Name,Influencer_Name,Product_Name,Decline_Reason,Order_Id,reason):
    sys.stdout = open("sendInfluencernotification.txt", "a")
    print('inside sendInfluencernotification')
    keyword = key
    print(user,key,RM_Name,Influencer_Name,Product_Name,Decline_Reason,Order_Id,reason)
    user = user
    icon = influencernotification.objects.get(name=keyword).icon
    heading = format_string(influencernotification.objects.get(name=keyword).head, RM_Name=RM_Name,Influencer_Name=Influencer_Name,Product_Name=Product_Name,Decline_Reason=Decline_Reason,Order_Id=Order_Id,reason=reason)
    body = format_string(influencernotification.objects.get(name=keyword).body, RM_Name=RM_Name,Influencer_Name=Influencer_Name,Product_Name=Product_Name,Decline_Reason=Decline_Reason,Order_Id=Order_Id,reason=reason)
    redirect = format_string(influencernotification.objects.get(name=keyword).redirect_link, Influencer_Name=Influencer_Name)
    username=Allusers.objects.get(id=user)
    time = datetime.now(pytz.utc)
    noti = notification.objects.create(title=heading,message=body,user=username,icon=icon,timestamp=time,redirect_link=redirect)
    #response=send_telegram(heading,body)
    send_telegram_image(heading,body,redirect,user)
    msg = str(heading)+'\n\n'+str(body)
    sendmessagetouseratwhatsapp(user,msg)

def sendRMnotification(key,RM_Name,client_type,client_Name,rmid,Influencer_Name,Order_ID,reason,Order_Stage):
    keyword = key
    user = rmid
    icon = RMnotification.objects.get(name=keyword).icon
    heading = format_string(RMnotification.objects.get(name=keyword).head, RM_Name=RM_Name,client_type=client_type,client_Name=client_Name,rmid=rmid,Influencer_Name=Influencer_Name,Order_ID=Order_ID,reason=reason,Order_Stage=Order_Stage)
    body = format_string(RMnotification.objects.get(name=keyword).body, RM_Name=RM_Name,client_type=client_type,client_Name=client_Name,rmid=rmid,Influencer_Name=Influencer_Name,Order_ID=Order_ID,reason=reason,Order_Stage=Order_Stage)
    redirect = RMnotification.objects.get(name=keyword).redirect_link
    username=Allusers.objects.get(id=user)
    time = datetime.now(pytz.utc)
    noti = notification.objects.create(title=heading,message=body,user=username,icon=icon,timestamp=time,redirect_link=redirect)
    #response=send_telegram(heading,body)
    send_telegram_image(heading,body,redirect,user)
    msg = str(heading)+'\n\n'+str(body)
    sendmessagetouseratwhatsapp(user,msg)

def sendkycmanagernotification(user,key,influencer_user_name,client_name):
    
    print('Users careayion')
    print(user,key,influencer_user_name)
    keyword = key
    user = user
    icon = KYCnotification.objects.get(name=keyword).icon
    heading = format_string(KYCnotification.objects.get(name=keyword).head, influencer_user_name=influencer_user_name,client_name=client_name)
    body = format_string(KYCnotification.objects.get(name=keyword).body, influencer_user_name=influencer_user_name,client_name=client_name)
    redirect = KYCnotification.objects.get(name=keyword).redirect_link
    username=Allusers.objects.get(id=user)
    time = datetime.now(pytz.utc)
    noti = notification.objects.create(title=heading,message=body,user=username,icon=icon,timestamp=time,redirect_link=redirect)
    #response=send_telegram(heading,body)
    send_telegram_image(heading,body,redirect,user)
    # print('last execute')
    msg = str(heading)+'\n\n'+str(body)
    sendmessagetouseratwhatsapp(user,msg)
    return HttpResponse('done')

def sendmanagernotification(user,key,client_id,client_name,influencer_name):
     
    print(user,key,client_name,influencer_name)
    keyword = key
    user = user
    icon = managernotification.objects.get(name=keyword).icon
    print('icon',icon)
    heading = format_string(managernotification.objects.get(name=keyword).head, client_id=client_id,client_name=client_name,influencer_name=influencer_name)
    body = format_string(managernotification.objects.get(name=keyword).body, client_id=client_id,client_name=client_name,influencer_name=influencer_name)
    redirect = managernotification.objects.get(name=keyword).redirect_link
    username=Allusers.objects.get(id=user)
    time = datetime.now(pytz.utc)
    noti = notification.objects.create(title=heading,message=body,user=username,icon=icon,timestamp=time,redirect_link=redirect)
    #response=send_telegram(heading,body)
    send_telegram_image(heading,body,redirect,user)
    # print('last execute')
    msg = str(heading)+'\n\n'+str(body)
    sendmessagetouseratwhatsapp(user,msg)
    return HttpResponse('done')



# def updateallnotificatonread(request):
#     userid = request.user.id
#     pass

###################################

from django.core.paginator import Paginator

from django.db.models import Q

def Notificationapi(request):
    userid = request.user.id
    # DataTables parameters
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    order_column = int(request.GET.get('order[0][column]', 2))  # We only consider ordering by one column for simplicity
    order_direction = request.GET.get('order[0][dir]', 'desc')

    # Initial query
    user_notifications = notification.objects.filter(user=userid)

    # If there's a search value, filter based on it (you can adjust fields as needed)
    if search_value:
        user_notifications = user_notifications.filter(
            Q(title__icontains=search_value) |
            Q(message__icontains=search_value)
        )

    # Order the results
    columns = ['title', 'message', 'timestamp']
    if order_direction == 'desc':
        user_notifications = user_notifications.order_by('-' + columns[order_column])
    else:
        user_notifications = user_notifications.order_by(columns[order_column])

    # Total count before filtering
    total_count = user_notifications.count()

    # Apply pagination
    user_notifications = user_notifications[start:start + length]

    # Serialize data
    data = [
        {'name': notif.title, 'date': notif.message, 'time': notif.timestamp, 'link':notif.redirect_link}
        for notif in user_notifications
    ]

    return JsonResponse({
        'data': data,
        'recordsTotal': total_count,
        'recordsFiltered': total_count,  # You can adjust this if you add more filtering options
        'draw': request.GET.get('draw', 1),  # Echo the 'draw' parameter back
        'start':start
    })


###################################


def Notification(request):
    userid = request.user.id
    role = request.user.roles
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        if role == "influencer":
            rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
            rmname = rmid.rmid.rmprofile.name
            image = rmid.rmid.rmprofile.profilepic
        if role == "client":
            rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
            rmname = rmid.rmid.rmprofile.name
            image = rmid.rmid.rmprofile.profilepic
        if role == "agency":
            rmid = AgencyProfile.objects.get(client_userid=request.user.id).rmid
            rmname = rmid.rmid.rmprofile.name
            image = rmid.rmid.rmprofile.profilepic
        if role == "RM":
            rmid = Rmsettings.objects.get(rmid=request.user.id).managerid
            rmname = rmid.rmid.rmprofile.name
            image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'
    
    user_notifications = notification.objects.filter(user=request.user.id).values().order_by('-timestamp')
    unread_notifications_no = len(list(notification.objects.filter(user=request.user.id,read=False)))

    return render(request, "notification.html", {'user_notifications':user_notifications,'unread_notifications_no':unread_notifications_no,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name,})




def count_filled_fields():
    sys.stdout = open("dataaaa.txt", "a")
    
    excluded_fields = ["gender", "imagegallery", "videogallery", "videolink", "analyticsid"]

    influencers_data = []  # List to store influencer_userid and their corresponding count

    # Iterate over all instances of InfluencerProfile
    for profile in InfluencerProfile.objects.all():
        count = 0  # Counter for filled fields for each profile
        
        # Iterate over all fields in the InfluencerProfile model
        for field in InfluencerProfile._meta.fields:
            if field.name not in excluded_fields:
                value = getattr(profile, field.name)
                # Check if the field has a non-default value
                if value is not None and value != field.default:
                    # If it's an ArrayField, check if it's not empty
                    if isinstance(value, list) and not value:
                        continue
                    count += 1
        if count==22:
            username=profile.influencer_userid.username
            
            kycids=Allusers.objects.filter(roles='kyc')
            for i in kycids:
                Thread(target=lambda:sendkycmanagernotification(user=i.id,key='kyc-influencervarification',influencer_user_name=username,client_name=None)).start()
                profile.send=True
                profile.save(update_fields=['send'])
                print('execute send mail')
            
        
        # Appending the influencer_userid and their corresponding count to the list
        influencers_data.append({
            'influencer_userid': profile.influencer_userid,
            'filled_fields_count': count
        })

    
    print("datas",influencers_data)

# count_filled_fields()


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from pathlib import Path
import os
from email.mime.image import MIMEImage
from django.core.mail.backends.smtp import EmailBackend

def format_string(s, **kwargs):
    try:
        return s.format(**kwargs)
    except KeyError:
        return s

def send_customer_email(key,user_email,client,influencer,order_id,service_type,order_start_date,order_end_date,rm,casting_call_id,brief_pitch,decline_reson,pward=None,otp=None):
    sys.stdout = open("sendrahulwithimanuu.txt", "a")
    print('inside send_customer_email')
    
    print('InfleucnerA',influencer)
    
    print('rahul')
    
    amazon_backend = EmailBackend(
        host='email-smtp.us-east-1.amazonaws.com',
        port=587,
        username='AKIAUUGAOKJTZCJPILPC',
        password='BC8JvtCJK4ul/14LLeQK5kjQYkV0XQP5pwkVgWoEQfix',
        use_tls=True
    )
    
    object = EmailTemplate.objects.get(template_id = key)
    subject = object.subject.format(client=client,influencer=influencer,order_id=order_id,service_type=service_type,order_start_date=order_start_date,order_end_date=order_end_date,rm=rm,casting_call_id=casting_call_id,brief_pitch=brief_pitch,decline_reson=decline_reson,pward=pward,otp=otp)
    print('subject',subject)
    print('Infleucner B',influencer)
    body = object.html_content.format(client=client,influencer=influencer,order_id=order_id,service_type=service_type,order_start_date=order_start_date,order_end_date=order_end_date,rm=rm,casting_call_id=casting_call_id,brief_pitch=brief_pitch,decline_reson=decline_reson,pward=pward,otp=otp)
    print('subject',body)
    print('Infleucner B',influencer)
    from_email = 'no-reply@influencerhiring.com'
    recipient_list = [user_email]
    template = render_to_string('notification-basic.html',{'body':body})
    email = EmailMultiAlternatives(subject, template, from_email, recipient_list, connection=amazon_backend)
    email.attach_alternative(template, "text/html")
    img_dir = str(Path(__file__).resolve().parent.parent/'mainapp/static/images')
        
    image_list = ["youtube.png","icon-facebook.png","icon-linkedin.png","icon-twitter.png","instagram.png"]
    for image in image_list:
        file_path = os.path.join(img_dir, image)
        img_type = image[-3:]
        with open(file_path, 'rb') as f:
            img = MIMEImage(f.read(), _subtype=img_type)
            img.add_header('Content-ID','<{name}>'.format(name=image))
            img.add_header('Content-Disposition', 'inline', filename=image)
        email.attach(img)
        
    email.send()










