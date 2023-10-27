from mainapp.models import *
from django.shortcuts import render, HttpResponse
from inappnotifications.views import *
import requests
import json
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session
from .models import *
from email.mime.image import MIMEImage
from django.conf import settings
from pathlib import Path
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os
import sys
from django.db.models import Q
from datetime import datetime, timedelta
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse

# OAuth configuration
client_id = 'BErHkIPCS5S3QzDJihEiw'
client_secret = 'dlKfKWD5lGL8PjDmoVim67I4Nc8MUAOh'
authorization_base_url = 'https://zoom.us/oauth/authorize'
token_url = 'https://zoom.us/oauth/token'
redirect_uri = 'https://www.influencerhiring.com/oauth/callback/'

x = {'access_token': 'eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6ImM0OGMzYzQ3LThiZTAtNGQ3Zi1hOTY3LTY2YjliMTkzMWQwYSJ9.eyJ2ZXIiOjksImF1aWQiOiI1OWZmYTkxY2FkYWVmYjNhY2Y3NTUxN2E0ZjVkNTgzMiIsImNvZGUiOiIyQ21sZjZ4NjFFb215NThwR2NfUkNDQ3QwRk9CenZBQlEiLCJpc3MiOiJ6bTpjaWQ6QkVySGtJUENTNVMzUXpESmloRWl3IiwiZ25vIjowLCJ0eXBlIjowLCJ0aWQiOjAsImF1ZCI6Imh0dHBzOi8vb2F1dGguem9vbS51cyIsInVpZCI6IlJrUXppR1ZwVFcyVVB4Q2Y1R1NkVmciLCJuYmYiOjE2ODk0MjQ0OTYsImV4cCI6MTY4OTQyODA5NiwiaWF0IjoxNjg5NDI0NDk2LCJhaWQiOiJlZVZjZ0tHSlNFQ0w2ekFQMTB3cWd3In0.E6pEm5-STUWUvZHKpCTzZw9u8jc4lHKMRHvU3yK_dg5MaLraf8O3p9z_JxBJpXapiJO1_h0BGwSi_x0tOwvWUA', 'token_type': 'bearer', 
 'refresh_token': 'eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6ImQzMjBjMjI1LThhNDQtNDc2MS04OTQ2LTRiZmNjYjViN2NmMCJ9.eyJ2ZXIiOjksImF1aWQiOiI1OWZmYTkxY2FkYWVmYjNhY2Y3NTUxN2E0ZjVkNTgzMiIsImNvZGUiOiIyQ21sZjZ4NjFFb215NThwR2NfUkNDQ3QwRk9CenZBQlEiLCJpc3MiOiJ6bTpjaWQ6QkVySGtJUENTNVMzUXpESmloRWl3IiwiZ25vIjowLCJ0eXBlIjoxLCJ0aWQiOjAsImF1ZCI6Imh0dHBzOi8vb2F1dGguem9vbS51cyIsInVpZCI6IlJrUXppR1ZwVFcyVVB4Q2Y1R1NkVmciLCJuYmYiOjE2ODk0MjQ0OTYsImV4cCI6MTY5NzIwMDQ5NiwiaWF0IjoxNjg5NDI0NDk2LCJhaWQiOiJlZVZjZ0tHSlNFQ0w2ekFQMTB3cWd3In0.Mn4Ci7YXQy0Q-pqq886HU55TqOwbeV6VpoE7QtDMbawk2oa8GGM_L2N5pWr0_41JLCVWDL9BXh-A70LAeycMwA', 'expires_in': 3599, 'scope': ['recording:write:admin', 'meeting:read:admin', 'recording:master', 'recording:read:admin', 'meeting:write:admin', 'meeting:master'], 'expires_at': 1689428098.964098}

def oauth_login(request):
    # Create an OAuth2Session instance
    oauth2_session = OAuth2Session(client_id, redirect_uri=redirect_uri)

    # Generate the authorization URL
    authorization_url, state = oauth2_session.authorization_url(authorization_base_url)

    # Save the state in session for later verification
    request.session['oauth_state'] = state
    print('state is theissss',state)

    # Redirect the user to the authorization URL
    return redirect(authorization_url)

def oauth_callback(request):
    # Retrieve the state from the session and verify it
    state = request.session.pop('oauth_state', None)
    # if state is None or state != request.GET.get('state'):
    #     return HttpResponse(f'oauth_failure this is {state}')

    # Create an OAuth2Session instance
    oauth2_session = OAuth2Session(client_id, redirect_uri=redirect_uri)

    # Fetch the access token using the authorization code
    token = oauth2_session.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.build_absolute_uri(),
    )

    # Store the access token in session or use it as needed
    request.session['oauth_token'] = token
    print(token)
    # Redirect the user to a success page
    token_id = zoomtoken.objects.filter(id=1)
    if token_id.exists():
        zoomtoken.objects.filter(id=1).update(access_token=token['access_token'],refresh_token=token['refresh_token'])
    else:
        zoomtoken_ref = zoomtoken(access_token=token['access_token'],refresh_token=token['refresh_token'])
        zoomtoken_ref.save()
    return HttpResponse(f'this is the full token {token}')
    # return redirect('schedule-meet')


# refresh_token = 'eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6ImQzMjBjMjI1LThhNDQtNDc2MS04OTQ2LTRiZmNjYjViN2NmMCJ9.eyJ2ZXIiOjksImF1aWQiOiI1OWZmYTkxY2FkYWVmYjNhY2Y3NTUxN2E0ZjVkNTgzMiIsImNvZGUiOiIyQ21sZjZ4NjFFb215NThwR2NfUkNDQ3QwRk9CenZBQlEiLCJpc3MiOiJ6bTpjaWQ6QkVySGtJUENTNVMzUXpESmloRWl3IiwiZ25vIjowLCJ0eXBlIjoxLCJ0aWQiOjAsImF1ZCI6Imh0dHBzOi8vb2F1dGguem9vbS51cyIsInVpZCI6IlJrUXppR1ZwVFcyVVB4Q2Y1R1NkVmciLCJuYmYiOjE2ODk0MjQ0OTYsImV4cCI6MTY5NzIwMDQ5NiwiaWF0IjoxNjg5NDI0NDk2LCJhaWQiOiJlZVZjZ0tHSlNFQ0w2ekFQMTB3cWd3In0.Mn4Ci7YXQy0Q-pqq886HU55TqOwbeV6VpoE7QtDMbawk2oa8GGM_L2N5pWr0_41JLCVWDL9BXh-A70LAeycMwA'


def refresh_access_token():
    # Zoom API endpoint for token refresh
    url = 'https://zoom.us/oauth/token'
    
    refresh_token = zoomtoken.objects.get(id=1).refresh_token
    # refresh_token = 'eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6ImFmYjJjZDVhLTkzNmYtNDFlMS1iYzhjLWQzMWZmMGEzNmMzZSJ9.eyJ2ZXIiOjksImF1aWQiOiI1OWZmYTkxY2FkYWVmYjNhY2Y3NTUxN2E0ZjVkNTgzMiIsImNvZGUiOiJNTTRIMlhScjdMRE1PM3dhMEt0UVZXNzgzcHFXbGppSmciLCJpc3MiOiJ6bTpjaWQ6QkVySGtJUENTNVMzUXpESmloRWl3IiwiZ25vIjowLCJ0eXBlIjoxLCJ0aWQiOjAsImF1ZCI6Imh0dHBzOi8vb2F1dGguem9vbS51cyIsInVpZCI6IlJrUXppR1ZwVFcyVVB4Q2Y1R1NkVmciLCJuYmYiOjE2ODk1NzgyNjEsImV4cCI6MTY5NzM1NDI2MSwiaWF0IjoxNjg5NTc4MjYxLCJhaWQiOiJlZVZjZ0tHSlNFQ0w2ekFQMTB3cWd3In0.izj26ktDiDtxBxN5gXsV5Tz9Q4swUPW49iWFm9yAU6FrKbgNrgu42tDTf9p6qhLex5RjjBTpJ_bVx4RXkZtg2Q'
    # Request payload
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    # Send POST request to refresh the access token
    response = requests.post(url, data=payload)

    # Process the response
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        zoomtoken.objects.filter(id=1).update(access_token=token_data['access_token'],refresh_token=token_data['refresh_token'])
        # Use the new access token for authorized API requests
        print(f"New access token: {access_token}")
        # return redirect(f'/schedule-meet/{order_id}/')
    else:
        print(f"Failed to refresh the access token. Error: {response.text}")
        # return HttpResponse(f"Failed to refresh the access token. Error: {response.text}")


def schedule_zoom_meeting(request,order_id):
    #sys.stdout = open('schedule-zoom-meet.txt', 'a')
    refresh_access_token()
    token = zoomtoken.objects.get(id=1).access_token
    
    # Schedule meeting endpoint
    url = 'https://api.zoom.us/v2/users/me/meetings'
    
    
    order_id=Orders.objects.get(ordersid=str(order_id))
    
    meeting_start_time = order_id.subslotid.starttime

    meeting_start_time += timedelta(hours=5, minutes=30)
    
    scheduled_date_time = meeting_start_time.strftime('%Y-%m-%dT%H:%M:%S')
    print(scheduled_date_time)
    
    duration = int(order_id.subslotid.slotduration.total_seconds() / 60)

    # Meeting details
    meeting_data = {
        'topic': "Influencer's Meet",
        'type': 2,  # Scheduled meeting
        'start_time': scheduled_date_time,  # Adjust the start time as needed time is in 24hrs format
        'duration': duration,  # Duration in minutes
        'timezone': 'Asia/Kolkata', #'America/New_York',  # Adjust the timezone as needed
        'settings': {
            'auto_recording': 'cloud',
            'mute_upon_entry': True,
            'max_participants':2,
            'participant_video':True,
            'join_before_host':True,
            'waiting_room':False,
        }
    }
    
    # Set request headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    
    # Send POST request to schedule meeting
    response = requests.post(url, headers=headers, json=meeting_data)
    
    # Process the response
    if response.status_code == 201:
        # Meeting scheduled successfully
        meeting_info = response.json()
        meeting_id = meeting_info.get('id')
        join_url = meeting_info.get('join_url')
        password=meeting_info.get('password')

        # client_send_meet_mail(join_url,order_id)
        # influencer_send_meet_mail(join_url,order_id)
        
        ref=zoomeet.objects.filter(orderid=str(order_id.ordersid))
        if ref.exists():
            ref=ref[0]
            ref.meet_link=join_url
            ref.meet_id=meeting_id
            ref.meet_password=password
            ref.schedule_date=scheduled_date_time
            ref.ismeetingend=False
            ref.islinksent=False
            ref.save(update_fields=['islinksent','ismeetingend','meet_link','meet_id','meet_password','schedule_date'])
        else:        
            zoomeet_ref=zoomeet(orderid=order_id,meet_link=join_url,meet_id=meeting_id,meet_password=password,schedule_date=scheduled_date_time,ismeetingend=False,islinksent=False)
            zoomeet_ref.save()
            
        
        print(f"Meeting scheduled successfully with ID: {meeting_id}")
        print(f"Join URL: {join_url}")
        return HttpResponse(f'<p>this is the order id -- {order_id}</p></br><p>Meeting scheduled successfully with ID: {meeting_id}</p></br><p>Join URL: <a href="{join_url}">join</a></p></br><p> password:-{password}</p></br><p>meeting info-- {meeting_info}</p>')
    else:
        # Meeting scheduling failed
        print(f"Failed to schedule a meeting. Error: {response.text}")
        return HttpResponse(f"Failed to schedule a meeting. Error: {response.text}")
    # return HttpResponse(f'this is your data {subslot_id}')



def client_send_meet_mail(link,order_id):
    template_name = "zoom-meet-client.html"
    email_add = str(order_id.clientid.email)
    sbdet=Subslots.objects.get(subslotid=str(order_id.subslotid.subslotid))
    redefined_time = sbdet.starttime + timedelta(hours=5, minutes=30)
    date = str(redefined_time.strftime("%d-%m-%Y"))
    time =str(redefined_time.strftime("%I:%M %p"))
    duration = str(sbdet.slotid.singleslotduration)+" minutes"
    influencer = str(order_id.influencerid.influencer_userid.username)
    client = str(order_id.clientid.username)
    subject = f"Confirmation: Your Upcoming Video Chat Session with {influencer}"
    template = render_to_string(template_name, 
                                {'link':link, 
                                'influencer':influencer, 
                                'client':client,
                                'date':date,
                                'time':time,
                                'duration':duration
                                })
    # text_content = strip_tags(template)
    email = EmailMultiAlternatives(subject,template,settings.EMAIL_HOST_USER,[email_add])
    email.attach_alternative(template, "text/html")
    # adding image in email template
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
    
    return HttpResponse(f'<div><h1> Hi {client} please check your email!!</h1><br></div>')


def influencer_send_meet_mail(link,order_id):
    template_name = "zoom-meet-influencer.html"
    sbdet=Subslots.objects.get(subslotid=str(order_id.subslotid.subslotid))
    redefined_time = sbdet.starttime + timedelta(hours=5, minutes=30)
    date = str(redefined_time.strftime("%d-%m-%Y"))
    time =str(redefined_time.strftime("%I:%M %p"))
    duration = str(sbdet.slotid.singleslotduration)+" minutes"
    email_add = str(order_id.influencerid.influencer_userid.email)
    influencer = str(order_id.influencerid.influencer_userid.username)
    client = str(order_id.clientid.username)
    subject = "Your Video Chat Session on InfluencerHiring.com"
    template = render_to_string(template_name, 
                                {'link':link, 
                                'influencer':influencer, 
                                'client':client,
                                'date':date,
                                'time':time,
                                'duration':duration
                                })
    # text_content = strip_tags(template)
    email = EmailMultiAlternatives(subject,template,settings.EMAIL_HOST_USER,[email_add])
    email.attach_alternative(template, "text/html")
    # adding image in email template
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
    
    return HttpResponse(f'<div><h1> Hi {influencer} please check your email!!</h1><br></div>')



def get_recording_download_link():
    
    print('rahuds')
    qs = zoomeet.objects.filter(Q(ismeetingend=False) | Q(islinksent=False)).order_by('-id')
    print('qs',qs)
    for i in qs :
        meeting_id=i.meet_id
        print('meey',meeting_id)
        order=str(i.orderid)
        print(order, 1111, i.orderid)
        slotid=str(i.orderid.subslotid.subslotid)
        print(slotid)
        print('i.ismeetingend',i.ismeetingend)
        endtime=Subslots.objects.get(subslotid=slotid).endtime
        if timezone.now() > endtime and i.ismeetingend==False:
            print('barawal')
            print(timezone.now() , endtime)
        
            print('time after',endtime + timedelta(seconds=10))
            # end the meeting
            end_meeting(meeting_id)
            ostid = Orderstatus.objects.get(status='Completed')
            oid=Orders.objects.filter(ordersid=order)
            if oid.exists():
                oid=oid[0]
                oid.orderstatus = ostid
                oid.completedate = timezone.now()
                oid.save(update_fields=[
                            'orderstatus', 'completedate'])
            
            i.ismeetingend=True
            i.save(update_fields=['ismeetingend'])
            
        if timezone.now() > (endtime + timedelta(hours=1)) and i.islinksent==False:
            # get the download link
            print('execute after 30 hius')
            
            oid=Orders.objects.filter(ordersid=order)
            if oid.exists():
                oid=oid[0]
                des=oid.orderdescription
                if des=='Recording service acquired':
                    refresh_access_token()
                    token = zoomtoken.objects.get(id=1).access_token

                    # API endpoint
                    url = f'https://api.zoom.us/v2/meetings/{meeting_id}/recordings'

                    # Set request headers
                    headers = {
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json',
                    }

                    # Send GET request to retrieve meeting recordings
                    response = requests.get(url, headers=headers)

                    # Process the response
                    if response.status_code == 200:
                        recordings = response.json()
                        password = recordings['password']
                        for recording in recordings['recording_files']:
                            if recording['file_type'] == "MP4":
                                download_url = recording['download_url']
                            else:
                                pass
                        download_urls = [recording_file['download_url'] for recording_file in recordings['recording_files']]
                        user_send_meet_download_link(download_url,password,order)
                        print(f"Download Link: {download_urls}")
                        i.islinksent=True
                        i.save(update_fields=['islinksent'])
                        print('recording link sent')
                else:
                    
                    print('recording link not sent')
                # return None # HttpResponse(f'<p>these are downloadble links--<a href="{download_url}" target="_blank">download file</a></p></br><p>this is password:-{password}</p>')
            else:
                print(f"Failed to retrieve meeting recordings. Error: {response.text}")
                # return None #HttpResponse(f"Failed to retrieve meeting recordings. Error: {response.text}")
        
        # sys.stdout = open("ip_get_recording.txt", "a")
        
        # starttime=Subslots.objects.get(subslotid=slotid).starttime
        # print('Rahultime',starttime)
        # with ThreadPoolExecutor(max_workers=4) as executor:
        #     if (timezone.now() >  (starttime - timedelta(minutes=15)) and timezone.now() <  (starttime - timedelta(minutes=14))): 
        #         print('getting here')
        #         executor.submit(sendusernotification(user=i.orderid.clientid.id,key="user-15minalertofvideocall",RM_Name=None,Influencer_Name=i.orderid.influencerid.influencer_userid.username,Product_Name=None,Decline_Reason=None,Order_Id=None,user_name=i.orderid.clientid.username))
        #         executor.submit(sendInfluencernotification(user=i.orderid.influencerid.influencer_userid.id,key="influencer-15minalertofvideocall",RM_Name=None,Influencer_Name=i.orderid.clientid.username,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None))
        #         executor.submit(send_customer_email(key='user-15minalertofvideocall',user_email=i.orderid.clientid.email,client=i.orderid.clientid.username,influencer=i.orderid.influencerid.influencer_userid.username,order_id=None,service_type=None,order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None))
        #         executor.submit(send_customer_email(key='influencer-15minalertofvideocall',user_email=i.orderid.influencerid.influencer_userid.email,client=i.orderid.clientid.username,influencer=i.orderid.influencerid.influencer_userid.username,order_id=None,service_type=None,order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None))

        #     if (timezone.now() >  (starttime - timedelta(minutes=59)) and timezone.now() <  (starttime - timedelta(minutes=58))):
        #         print('getting here B1')
        #         executor.submit(sendusernotification(user=i.orderid.clientid.id,key="user-1hralertofvideocall",RM_Name=None,Influencer_Name=i.orderid.influencerid.influencer_userid.username,Product_Name=None,Decline_Reason=None,Order_Id=None,user_name=i.orderid.clientid.username))
        #         print('getting here B2')
        #         executor.submit(sendInfluencernotification(user=i.orderid.influencerid.influencer_userid.id,key="influencer-1hralertofvideocall",RM_Name=None,Influencer_Name=i.orderid.clientid.username,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None))
        #         print('getting here B3')
        #         executor.submit(send_customer_email(key='user-1hralertofvideocall',user_email=i.orderid.clientid.email,client=i.orderid.clientid.username,influencer=i.orderid.influencerid.influencer_userid.username,order_id=None,service_type=None,order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None))
        #         print('getting here B4')
        #         executor.submit(send_customer_email(key='influencer-1hralertofvideocall',user_email=i.orderid.influencerid.influencer_userid.email,client=i.orderid.clientid.username,influencer=i.orderid.influencerid.influencer_userid.username,order_id=None,service_type=None,order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None))
        #         print('sdfsdf',starttime)
            
                                                                                                                                 
        
def notifyuserforvideochat():
    sys.stdout = open("ip_get_recording.txt", "a")    
    qs = zoomeet.objects.filter(Q(ismeetingend=False) | Q(islinksent=False)).order_by('-id')
    
    for i in qs :
        slotid=str(i.orderid.subslotid.subslotid)    
        starttime=Subslots.objects.get(subslotid=slotid).starttime
        print('Vc starttime',starttime)
        print('current time',timezone.now())
        with ThreadPoolExecutor(max_workers=4) as executor:
            if (timezone.now() >  (starttime - timedelta(minutes=15)) and timezone.now() <  (starttime - timedelta(minutes=14))): 
                print('getting here')
                print('15 mintues executeion time',timezone.now())
                executor.submit(sendusernotification(user=i.orderid.clientid.id,key="user-15minalertofvideocall",RM_Name=None,Influencer_Name=i.orderid.influencerid.influencer_userid.username,Product_Name=None,Decline_Reason=None,Order_Id=None,user_name=i.orderid.clientid.username))
                executor.submit(sendInfluencernotification(user=i.orderid.influencerid.influencer_userid.id,key="influencer-15minalertofvideocall",RM_Name=None,Influencer_Name=i.orderid.clientid.username,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None))
                executor.submit(send_customer_email(key='user-15minalertofvideocall',user_email=i.orderid.clientid.email,client=i.orderid.clientid.username,influencer=i.orderid.influencerid.influencer_userid.username,order_id=None,service_type=None,order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None))
                executor.submit(send_customer_email(key='influencer-15minalertofvideocall',user_email=i.orderid.influencerid.influencer_userid.email,client=i.orderid.clientid.username,influencer=i.orderid.influencerid.influencer_userid.username,order_id=None,service_type=None,order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None))

            if (timezone.now() >  (starttime - timedelta(minutes=59)) and timezone.now() <  (starttime - timedelta(minutes=58))):
                print('1 hour executeion time',timezone.now())
                
                print('getting here B1')
                executor.submit(sendusernotification(user=i.orderid.clientid.id,key="user-1hralertofvideocall",RM_Name=None,Influencer_Name=i.orderid.influencerid.influencer_userid.username,Product_Name=None,Decline_Reason=None,Order_Id=None,user_name=i.orderid.clientid.username))
                print('getting here B2')
                executor.submit(sendInfluencernotification(user=i.orderid.influencerid.influencer_userid.id,key="influencer-1hralertofvideocall",RM_Name=None,Influencer_Name=i.orderid.clientid.username,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None))
                print('getting here B3')
                executor.submit(send_customer_email(key='user-1hralertofvideocall',user_email=i.orderid.clientid.email,client=i.orderid.clientid.username,influencer=i.orderid.influencerid.influencer_userid.username,order_id=None,service_type=None,order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None))
                print('getting here B4')
                executor.submit(send_customer_email(key='influencer-1hralertofvideocall',user_email=i.orderid.influencerid.influencer_userid.email,client=i.orderid.clientid.username,influencer=i.orderid.influencerid.influencer_userid.username,order_id=None,service_type=None,order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None))
                print('sdfsdf',starttime)
    
        

        
def delete_meeting(meeting_id):
    token = zoomtoken.objects.get(id=1).access_token

    # API endpoint
    url = f'https://api.zoom.us/v2/meetings/{meeting_id}'

    # Set request headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    # Update the meeting status to 'end'
    payload = {
        'action': 'end'
    }

    # Send PUT request to update the meeting status
    response = requests.delete(url, headers=headers, json=payload)

    # Process the response
    if response.status_code == 204:
        print(f"Meeting with ID: {meeting_id} has deleted.")
        return HttpResponse(f"Meeting with ID: {meeting_id} has deleted.")
    else:
        print(f"Failed to end the meeting. Error: {response.text}")
        return HttpResponse(f"Failed to end the meeting. Error: {response.text}")
        
        
        

def end_meeting(meeting_id):
    refresh_access_token()
    token = zoomtoken.objects.get(id=1).access_token

    # API endpoint
    url = f'https://api.zoom.us/v2/meetings/{meeting_id}/status'

    # Set request headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    # Update the meeting status to 'end'
    payload = {
        'action': 'end'
    }

    # Send PUT request to update the meeting status
    response = requests.put(url, headers=headers, json=payload)

    # Process the response
    if response.status_code == 204:
        print(f"Meeting with ID: {meeting_id} has ended.")
        delete_meeting(meeting_id)
        return HttpResponse(f"Meeting with ID: {meeting_id} has ended.")
    else:
        print(f"Failed to end the meeting. Error: {response.text}")
        return HttpResponse(f"Failed to end the meeting. Error: {response.text}")

def user_send_meet_download_link(link,password,order):
    
    order=Orders.objects.get(ordersid=str(order))
    template_name = "download-meet.html"
    subject = "Your Video Chat Session recording on InfluencerHiring.com"
    user = str(order.clientid.username)
    email_add = str(order.clientid.email)
    template = render_to_string(template_name, 
                                {'download_link':link,
                                'user':user, 
                                'password':password,
                                })
    # text_content = strip_tags(template)
    email = EmailMultiAlternatives(subject,template,settings.EMAIL_HOST_USER,[email_add])
    email.attach_alternative(template, "text/html")
    # adding image in email template
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
    
    return HttpResponse(f'<div><h1> Hi {user} please check your email!!</h1><br></div>')