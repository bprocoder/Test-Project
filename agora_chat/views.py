from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from inappnotifications.views import *
from threading import Thread
from django.contrib.auth.decorators import *
from .models import *
from .serializer import *
import datetime
from datetime import datetime
import pytz
import json,sys,logging
# from .time_calculator import modify_datetime
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
import mimetypes
from google.cloud import storage
from google.oauth2 import service_account
from django.utils.timezone import now
from mainapp.models import *

# ManRMPrashant
@login_required(login_url='/login/')
def sendunreadMessageCountGroupChat(request):
    # sys.stdout = open("agrachat.txt", "a")
    username = request.user.id
    name = request.user.username
    print('this is the name of session user:- ',username)
    data = chat_user.objects.filter(user=username).values()
    print('this is the total channels:-',data)
    user_and_unread_count = []
    for item in data:
        channel_name = item['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=name).values()))
        last_message = list(message.objects.filter(channel=channel_name).order_by('created').values())
        if len(last_message) == 0:
            lmessage = ''
            ltime = ''
        else:
            lmessage = last_message[-1]['body']
            ltime = last_message[-1]['created'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        user_and_unread_count.append({'channel':channel_name,'count':unread_messages,'body':lmessage,'created':ltime})
    print('final output:-',user_and_unread_count)
    return JsonResponse({"unread_count":user_and_unread_count})

@login_required(login_url='/login/')
def getorderchatnewmsg(request):
    userid = request.user.id
    username = request.user.username
    data = chat_user.objects.filter(user=userid).values()
    user_new_message = []
    for item in data:
        channel_name = item['channel']
        unrecived_messages = len(list(message.objects.filter(channel=channel_name,status=False,recieve_status=False).exclude(sender=username).values()))
        last_message = list(message.objects.filter(channel=channel_name,status=False,recieve_status=False).order_by('created').values())
        if len(last_message) == 0:
            sender = None
            message1 = None
        else:
            sender = last_message[-1]['sender']
            message1 = last_message[-1]['body']
        user_new_message.append({'sender':sender,'message':message1,'count':unrecived_messages})
        message.objects.filter(channel=channel_name,status=False,recieve_status=False).exclude(sender=username).update(recieve_status=True)
    print('final output:-',user_new_message)
    return JsonResponse({"unread_count":user_new_message})

@login_required(login_url='/login/')
def getsinglechatnewmsg(request):
    userid = request.user.id
    username = request.user.username
    data = single_chat.objects.filter(user=userid).values()
    user_new_message = []
    for item in data:
        channel_name = item['channel']
        unrecived_messages = len(list(message.objects.filter(channel=channel_name,status=False,recieve_status=False).exclude(sender=username).values()))
        last_message = list(message.objects.filter(channel=channel_name,status=False,recieve_status=False).order_by('created').values())
        if len(last_message) == 0:
            sender = None
            message1 = None
        else:
            sender = last_message[-1]['sender']
            message1 = last_message[-1]['body']
        user_new_message.append({'sender':sender,'message':message1,'count':unrecived_messages})
        message.objects.filter(channel=channel_name,status=False,recieve_status=False).exclude(sender=username).update(recieve_status=True)
    print('final output:-',user_new_message)
    return JsonResponse({"unread_count":user_new_message})

@login_required(login_url='/login/')
def sendUnreadMessageCount(request):
    # sys.stdout = open("agrachat.txt", "a")
    username = request.user.id
    name = request.user.username
    print('this is the name of session user:- ',username)
    data = single_chat.objects.filter(user=username).values()
    print('this is the total channels:-',data)
    user_and_unread_count = []
    for item in data:
        channel_name = item['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=name).values()))
        last_message = list(message.objects.filter(channel=channel_name).order_by('created').values())
        if len(last_message) == 0:
            lmessage = ''
            ltime = ''
        else:
            lmessage = last_message[-1]['body']
            ltime = last_message[-1]['created'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        user_and_unread_count.append({'channel':channel_name,'count':unread_messages,'body':lmessage,'created':ltime})
    print('final output:-',user_and_unread_count)
    return JsonResponse({"unread_count":user_and_unread_count})


@csrf_exempt
def updateGetLastActivity(request):
    # sys.stdout = open("agrachat.txt", "a")
    username = request.user.id
    print('this is the name of session user:- ',username)
    data = chat_user.objects.filter(user=username).values()
    print('this is the data:- ',data)
    user_and_online_status = []
    for item in data:
        channel_name = item['channel']
        other_user = chat_user.objects.filter(channel=channel_name,RM=False).exclude(user=username).values().first()
        print(other_user['last_activity'])
        last_activity = other_user['last_activity']
        activity = datetime.now(pytz.utc)
        if last_activity == None:
            online_status = False
            chat_user.objects.filter(channel=channel_name,RM=False).exclude(user=username).values().update(last_activity=datetime.now(pytz.utc))
        else:
            diffrance = ((last_activity-activity).total_seconds())*-1
            online_status = round(int(diffrance)) <= 30
        user_status = {'channel':channel_name,'online':online_status}
        user_and_online_status.append(user_status)
    print(user_and_online_status)
    # print(round(int(diffrance)),online_status)
    chat_user.objects.filter(user=username).update(last_activity=activity)
    return JsonResponse({'success':True,'status':user_and_online_status})

credentials = {
  "type": "service_account",
  "project_id": "durable-bond-390313",
  "private_key_id": "3858c28f14b094482825b8b2409fda040c71865d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCyniI/ZXpczVTO\n8sjjwGILiyAWwNIkgJKqI87DXcM+N8Gmx5qmZcZeB6+EoWHG+xFsqXUCRkUIaJaR\nMXbLyMnbmhaAbgKHzpCWi6fR+qc3qabwWqyjNqYDkMBny3GNE2OHZHLlsB299SON\n88+ZLAOoo6Uym5wLcJUsGxDWnK+M3qqBNkttdKWNDTF/PLVhytuIFXGIekNVGRez\niJvg5ybIs841iqe/58k+pvpaHf4s9g5yJCJZdxLtK/4b1CYj/LIpQmgoXg3dx7fF\nzHYpBSPMI6n/an1f/YxvhB4QWOYh5fd6K7T+XzDzNjcPhmNzntAPYfRysnFIIApk\nDWpu+4HhAgMBAAECggEABK5TPHEW31a8Ob4wGJPineXT/fSorS83aMEOep068Cb6\n6rmBaonxRGaUKXgnPVU4FC5utBQOXBWNmJmAwP9ultQ3cb8wTsnRjTh0ufKFLlbC\nWrstmgtlF2PUPwQcYjOXYKV3w2A1r1Q8zcwNbTizkdhUDHr6gGw/ZIwDCXTKvvjN\nnlv0tQSAd8b+/CohICfaAKntHC0PbaooGuvQ6tFYsCYdPXklMdMg5GuAB0b7Ro4B\nltGY6ctesDJ7sKoHai31aFLxBEJdwCNkHV12zosKhgMd5JML/DfKN0+frVKRDi7n\n1gvAQJMS0D4yi/h9wt/scQzJuvKC/VMp1gmavrLN7wKBgQDuB50QTmxwjepQVSOh\nDGlap9cfUoK8zC7FTql6Vc9Dem2bT0FKyIbN/cjtYGO4+UHHqystfV2E83a29mWu\nl2vp/NBuUpLL7G81mZAw3TzFYvVRopqQyxv9KkthzPT+7lAia2s7piC2y++qiCQc\n5lmnZCtp5yx1soj6vgRInGF9AwKBgQDAGkR745pbQwkg74C0AJKX0/UFNZGhtCDV\n2RIhrCTaz3V3JzdzoIG9r9qhUTiC1JDa0FXITw172vo7bGxLP79GFP3i//5hsMjI\naduCVR8In1dZYJ8/yec7yQJVIEByTlikjD4B52+uf6mzezr3IEjDdxWiD3l4vUpG\nPzKG6Rn2SwKBgEkseAFSSo3TYsvtUHWq7hxbaouLfvtxPZOUWg9sn7nbwiQzmhvW\nR3K96O3oat+raKhsG2rxljVP7xfR6XJhxF/7Q0wXAF/GQG3W1nffG1aG1GmTNjb6\n6ZDLVr8rFcnlEydxpFaC/J2VVgkzrv5fZgJKjfoRgh5wkyGaFpEH2gRnAoGAAX3y\nvDeXUlAh+QSDLmK2wMEfrQuuduAMRTzrXCGXI6/qzKMcViSP/WYpP4l+890sxtZJ\nZEXg5+5adS2xZaA4HxY4ppOwaRfTZ2MTFl8M36dFKWeLtRYfWqKEBx86AOlE3PpN\n3PvsLSHGsqMpYRP6HLKHE3wlSF/H/OWuwcd7sSMCgYBC3qv6daf3LgH3SuY7Tawq\nbM46NxDWgdkmN7OPQeQz5H2s8zpZ2p6/ho/7cGRrURtki3rfq43F8/HqX7kdaNcz\niGzP8DHF8IahhvbUR+18yUZ7RagPRmcEu9MuLWsF7I8Y8Ur3CHvNPapxg7VLBcit\ndszhbYh2vbvZFuhla+3YLg==\n-----END PRIVATE KEY-----\n",
  "client_email": "chat-file-strorage-acount@durable-bond-390313.iam.gserviceaccount.com",
  "client_id": "110124669600287224507",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/chat-file-strorage-acount%40durable-bond-390313.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
credentil_obj = service_account.Credentials.from_service_account_info(credentials)
storage_client = storage.Client(credentials=credentil_obj)
bucket = storage_client.get_bucket('file-storage-for-chat-app')
from datetime import timedelta
@csrf_exempt
def get_signed_url(request):
    if request.method == 'POST':
        # Get the filename and content type from the request
        data = json.loads(request.body)
        filename = data['filename']
        content_type = data['contentType']
        channel = data['channel']
        full_file_name = f'{channel}/{filename}'
        ms_time = now().strftime('%f')
        # Generate a signed URL for GCS upload
        client = storage.Client(credentials=credentil_obj)
        bucket = client.bucket('file-storage-for-chat-app')
        blob = bucket.blob(full_file_name)
        if blob.exists():
            full_file_name = f'{channel}/{ms_time}{filename}'
            blob = bucket.blob(full_file_name)
        # blob.make_public()
        # public_url = blob.public_url
        # Set the desired expiration time for the signed URL (e.g., 1 hour)
        
        expiration_time = timedelta(hours=1)

        # Generate the signed URL
        signed_url = blob.generate_signed_url(
            version='v4',
            expiration=expiration_time,
            method='PUT',
            content_type=content_type
        )
        
        
        
        # Return the signed URL to the client 
        return JsonResponse({'signedUrl': signed_url})

@csrf_exempt
def upload_file(request):
    #sys.stdout = open("agrachat.txt", "a")
    if request.method == 'POST':
        file = request.FILES.get('file')
        order_name = request.POST.get('order_name')
        print('this is order name',order_name)
        if file:
            file_name = str(file).replace(' ','-')
            print(file_name)
            file_path = str(order_name)+'/'+file_name
            blob = bucket.blob(file_path)
            if blob.exists():
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_file_name = f"{timestamp}_{str(file_name)}"
                file_path1 = str(order_name)+'/'+new_file_name
                blob = bucket.blob(file_path1)
            else:
                new_file_name = None  # Set a default value if blob does not exist
                # file_path = file_path1
            blob.upload_from_file(file, timeout=3600)
            if new_file_name != None:
                output_name = new_file_name
                url = make_public('file-storage-for-chat-app',file_path1)
            else:
                url = make_public('file-storage-for-chat-app',file_path)
                output_name = str(file)
            output_url = '<a href="'+str(url)+'">'+str(output_name)+'</a>'
            print(output_url)
            return JsonResponse({'sucess':True,'file_url':output_url})
        else:
            return JsonResponse({'sucess':False})


def get_download_url(bucket_name, blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    #generate a signed url with expiration
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=604800)
    url = blob.generate_signed_url(
        version='v4',
        expiration=expiration,
        method='GET'
    )
    return url

@login_required(login_url='/login/')
def file_make_public(request,filename, foldername):
    # sys.stdout = open("agrachat.txt", "a")
    print('Abbbbbbb this is make_public')
    fname = filename
    folname = foldername
    full_file_name = f'{folname}/{fname}'
    print(full_file_name)
    bucket = storage_client.bucket('file-storage-for-chat-app')
    blob = bucket.blob(full_file_name)

    # Make the blob publicly accessible
    blob.make_public()

    # Get the publicly accessible URL
    url = blob.public_url
    final_url = f'<a href="{url}" target="_blank" download>{fname}</a>'
    return JsonResponse({'download_url':final_url})#https://youtube.com/shorts/dv8oqiZFCyI?feature=share


@login_required(login_url='/login/')
def login_user(request):
    # sys.stdout = open("agrachat.txt", "a")
    try:
        username = request.user.id
        # print('abcd',username)
        name=request.user.username
        data = chat_user.objects.filter(user=username,channel_status=True).values()
        status = data[0]['channel_status']
        # print("data",data[0]['channel_status'])
        if not data:
            return HttpResponse('<div style="display: flex;align-items: center;justify-content: center;height: 100%;background-color: skyblue;font-size: 24px;color: white;"><h1>Not Authorized</h1></div>')
        channel_name_with_unread_message = []
        for item in data:
            channel_name = item['channel']
            # print('channel',channel_name)
            orderuser = chat_user.objects.filter(channel=channel_name)
            # print('this is order user',orderuser)
            order_id=orderuser[0].orderid
            # print(order_id)
            user = chat_user.objects.filter(user=username,channel=channel_name,RM=True).values()
            # print('user',user)
            image=None
            if not user:
                influencer = chat_user.objects.filter(channel=channel_name,RM=False).exclude(user=username).values()[0]['user_id']
                image=InfluencerProfile.objects.filter(influencer_userid=str(influencer))
                if image.exists():
                    image=image[0].profileimage
                else:
                    image=ClientProfile.objects.filter(client_userid=str(influencer))
                    if image.exists():
                        image=image[0].profileimage
                    else:
                        image=AgencyProfile.objects.filter(agency_userid=str(influencer))
                        if image.exists():
                            image=image[0].profileimage
                influencer=Allusers.objects.get(id=str(influencer)).username
                # print('image',image)
                # print('influencr',influencer)
            else:
                influencer=channel_name
                image='None'
                # print(influencer)
            
            last_message = message.objects.filter(channel=channel_name).order_by('created').values()
            if last_message.exists():
                last_message=list(last_message)
                lmessage = last_message[-1]['body']
                ltime = last_message[-1]['created'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                # with open('agora_time.txt', 'w') as f:
                #     f.write(ltime)
                    # pass
            else:
                lmessage = ''
                ltime = ''
            # print(last_message['created'])
            # if orderuser.exists():
            #     for i in orderuser:
            unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=name).values()))
            channel_name_with_unread_message.append((name,channel_name,strip_tags(lmessage),ltime,influencer,order_id,image,status,unread_messages))
        channel_name_with_unread_message.sort(key=lambda x: x[3], reverse=True)
        print(channel_name_with_unread_message)
        
        role = request.user.roles
        print(role)
        if role == 'client':
            rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid.rmid
            rmobj = Rmprofile.objects.get(rmid=rmid)
            userrmname = rmobj.name
            userrmprofile = rmobj.profilepic
        elif role == 'agency':
            rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid.rmid
            rmobj = Rmprofile.objects.get(rmid=rmid)
            userrmname = rmobj.name
            userrmprofile = rmobj.profilepic
        elif role == 'influencer':
            rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
            userrmname = rmid.rmid.rmprofile.name
            userrmprofile = rmid.rmid.rmprofile.profilepic
        else:
            userrmname = 'None'
            userrmprofile = 'None'
            
        
        print('this is the user RM details---',userrmname,userrmprofile,'\n',channel_name_with_unread_message)

        return render(request,'group-chat.html',{'channel_name':channel_name_with_unread_message,'userrmname':userrmname,'userrmprofile':userrmprofile})
    except:
        role = request.user.roles
        print(role)
        if role == 'client':
            rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid.rmid
            rmobj = Rmprofile.objects.get(rmid=rmid)
            userrmname = rmobj.name
            userrmprofile = rmobj.profilepic
        elif role == 'agency':
            rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid.rmid
            rmobj = Rmprofile.objects.get(rmid=rmid)
            userrmname = rmobj.name
            userrmprofile = rmobj.profilepic
        elif role == 'influencer':
            rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
            userrmname = rmid.rmid.rmprofile.name
            userrmprofile = rmid.rmid.rmprofile.profilepic
        else:
            userrmname = 'None'
            userrmprofile = 'None'
        
        print('this is the user RM details---',userrmname,userrmprofile)
        return render(request,'group-chat.html',{'userrmname':userrmname,'userrmprofile':userrmprofile})



@api_view(['GET'])    
def show_chat(request,name,channel):
    # sys.stdout = open("agrachat.txt", "a")
    print('chennel',channel)
    name=Allusers.objects.get(username=name).id
    user = chat_user.objects.filter(user=name, RM=False)
    print('this is user', user)
    if user:
        seen_status = message.objects.filter(channel=channel,status=False).exclude(sender=name).update(status=True)
    try:
        channel_detail = chat_user.objects.filter(user=name,channel=channel).values().first()['channel_status']
        print('this is channel detail',channel_detail)
        posts = message.objects.filter(channel=channel).order_by('created').values()
        print('post office',posts)
        user_icon = chat_user.objects.filter(channel=channel).values()
        users = []
        for item in user_icon:
            icon_user = item['user_id']
            print(icon_user)
            usern=Allusers.objects.get(id=icon_user)
            imag=None
            if usern.roles=='RM':
                imag=usern.rmprofile.profilepic
            if usern.roles=='client':
                imag=usern.clientprofile.profileimage
            if usern.roles=='influencer':
                imag=usern.influencerprofile.profileimage
            if usern.roles=='agency':
                imag=usern.agencyprofile.profileimage
            print('sab betichod sale sab betichod----',imag)
            
            
            users.append((usern.username,usern.roles,str(imag)))
        showuser = {"users":users}
        data = {"data":posts}
        #print(users)
        # if channel_detail:
        return Response({"data":posts,"users":users})
    except:
        return Response({"error":'not autheticated',
                         "status":400})
    
    
@api_view(['post'])
def add_post(request):
    #sys.stdout = open("agrachat.txt", "a")
    data = request.data
    print('this is the data we get at backend',data, end='\n')
    name=Allusers.objects.get(username=data['sender']).id
    status = chat_user.objects.filter(user=name,channel=data['channel']).values().first()['channel_status']
    if status:
        post_data = message.objects.create(
            sender=data['sender'],
            body=data['body'],
            channel=data['channel'],
        )
        print('this is the data we creating',post_data, end='\n')
        serializer  = postSerializer(post_data, many=False)
        print(serializer.data, end='\n')
        return Response(serializer.data)
    else:
        return Response({'message':'Your channel has been deavtivated.'})
    


@api_view(['post'])
def single_chat_add_post(request):
    # sys.stdout = open("agrachat.txt", "a")
    data = request.data
    print('this is the data we get at backend',data, end='\n')
    name=Allusers.objects.get(username=data['sender']).id
    print(name)
    user_status = single_chat.objects.filter(user=name,channel=data['channel']).values().first()
    print(user_status)
    if user_status['channel_for_RM_chat'] == False:
        length_of_messages = len(list(message.objects.filter(sender=data['sender'],channel=data['channel']).values()))
        print('this is message length',length_of_messages)
        if length_of_messages > 11:
            single_chat.objects.filter(user=name,channel=data['channel']).values().first().update(channel_status=False)
            created = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            print('This is the time stamp',created)
            return Response({'body':'You have reached the limit.','sender':'Influencer Hiring','status':'False','created':created})
        
    status = single_chat.objects.filter(user=name,channel=data['channel']).values().first()['channel_status']
    if status:
        post_data = message.objects.create(
            sender=data['sender'],
            body=data['body'],
            channel=data['channel'],
        )
        print('this is the data we creating',post_data, end='\n')
        serializer  = postSerializer(post_data, many=False)
        print(serializer.data, end='\n')
        return Response(serializer.data)
    else:
        return Response({'message':'Your channel has been deavtivated.'})

@api_view
def unread_count(request):
    # data = request.data
    pass

### single user chat limit of 600 chracters.
@login_required(login_url='/login/')
def influencerchat(request):
    # sys.stdout = open("agrachat.txt", "a")
    name = request.user.username
    # print(name)
    username = request.user.id
    # print(username)
    user_channel = single_chat.objects.filter(user=username,channel_for_RM_chat=False).values()
    # print(user_channel)
    user_channels_and_channel_status = []
    for item in user_channel:
        channel = item['channel']
        print('this is the channel',channel)
        channel_status = item['channel_status']
        other = single_chat.objects.filter(channel=channel).exclude(user=username).values().first()['user_id']
        print(other)
        other_user=Allusers.objects.get(id=str(other)).username
        print('this is other user',other_user)
        last_message = message.objects.filter(channel=channel).order_by('created').values()
        if last_message.exists():
            # print('ABCD')
            last_message = list(last_message)
            lmessage = last_message[-1]['body']
            lmessagetime = last_message[-1]['created'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            # print('1234')
            lmessage = ''
            lmessagetime = ''
        
        influencer = single_chat.objects.filter(channel=channel).exclude(user=username).values()[0]['user_id']
        image=InfluencerProfile.objects.filter(influencer_userid=str(influencer))
        if image.exists():
            image=image[0].profileimage
            print('this is the image1 to print',str(image))
        else:
            image=ClientProfile.objects.filter(client_userid=str(influencer))
            if image.exists():
                image=image[0].profileimage
            else:
                image=AgencyProfile.objects.filter(agency_userid=str(influencer))
                if image.exists():
                    image=image[0].profileimage
                # print('this is the image to print',image)
        #influencer=Allusers.objects.get(id=str(influencer)).username
        
        unread_messages = len(list(message.objects.filter(channel=channel,status=False).exclude(sender=name).values()))
        
        user_channels_and_channel_status.append((name,channel,other_user,channel_status,lmessage,lmessagetime,image,unread_messages))
        # channel_name = f'{influencer_name}{username}'
        # posts = list(post.objects.filter(channel=channel_name).values())
    user_channels_and_channel_status.sort(key=lambda x: x[-1], reverse=True)
    print(user_channels_and_channel_status)
    data_to_send = request.session.get('clicked-elemet-data',{})
    influencer = data_to_send
    influncer = data_to_send.get('influencer', '')
    clickchannel = data_to_send.get('channel', '')
    try:
        del request.session['clicked-elemet-data']
    except:
        pass
    role = request.user.roles
    print(role)
    if role == 'client':
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid

        userrmname = rmid.rmid.rmprofile.name
        userrmprofile = rmid.rmid.rmprofile.profilepic
    if role == 'agency':
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid

        userrmname = rmid.rmid.rmprofile.name
        userrmprofile = rmid.rmid.rmprofile.profilepic
    if role == 'influencer':
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        userrmname = rmid.rmid.rmprofile.name
        userrmprofile = rmid.rmid.rmprofile.profilepic
    
    print('this is the user RM details---',userrmname,userrmprofile)

    return render(request,'chat.html',{'channels':user_channels_and_channel_status,'clickelementid':[influncer,clickchannel],'userrmname':userrmname,'userrmprofile':userrmprofile})
    # return HttpResponse(f'<h1>Your name is {influencer_name}</h1><br><h2>and my name is {username}<h2><br><h3>our channel name is {influencer_name}{username}</h3>')


@api_view(['GET'])
def single_show_chat(request,name,channel):
    #sys.stdout = open("agrachat.txt", "a")
    # print(name,channel,end='\n')
    sender = name
    name=Allusers.objects.get(username=name).id
    user = single_chat.objects.filter(user=name)
    # print(user)
    if user:
        seen_status = message.objects.filter(channel=channel,status=False).exclude(sender=sender).update(status=True)
    try:
        total_messages_len = message.objects.filter(channel=channel,sender=sender).values()
        print('this is the len:-- ',total_messages_len)
        channel_detail = single_chat.objects.filter(user=name,channel=channel).values().first()['channel_status']
        # print('details',channel_detail)
        posts = list(message.objects.filter(channel=channel).order_by('created').values())
        # print('postes',posts)
        user_icon = single_chat.objects.filter(channel=channel).values()
        # print(user_icon)
        users = []
        for item in user_icon:
            icon_user = item['user_id']
            # print(icon_user)
            usern=Allusers.objects.get(id=icon_user)
            imag=None
            if usern.roles=='RM':
                imag=usern.rmprofile.profilepic
            if usern.roles=='client':
                imag=usern.clientprofile.profileimage
            if usern.roles=='influencer':
                imag=usern.influencerprofile.profileimage
            if usern.roles=='agency':
                imag=usern.agencyprofile.profileimage
            

            users.append((usern.username,usern.roles,str(imag)))
        showuser = {"users":users}
        data = {"data":posts}
        # if channel_detail:
        return Response({"data":posts,"users":users,"status":channel_detail})
    except:
        return Response({"error":'not autheticated',
                         "status":400})
        

@api_view(['POST'])
def show_RM_chat(request):
    # sys.stdout = open("agrachat.txt", "a")

    data = request.data
    channel = data['channel']
    name = data['name']
    sender = name
    name=Allusers.objects.get(username=name).id
    user = single_chat.objects.filter(user=name,channel_for_RM_chat=True)
    print(name,channel,end='\n')
    print(user)
    if user:
        seen_status = message.objects.filter(channel=channel,status=False).exclude(sender=sender).update(status=True)
    try:
        channel_detail = single_chat.objects.filter(user=name,channel=channel).values().first()['channel_status']
        print('details',channel_detail)
        posts = list(message.objects.filter(channel=channel).order_by('created').values())
        print('postes',posts)
        user_icon = single_chat.objects.filter(channel=channel).values()
        print(user_icon)
        RMid = single_chat.objects.filter(channel=channel,channel_for_RM_chat=True).exclude(user=name).values().first()['user_id']
        print('this is the RMid',RMid)
        Rm = Allusers.objects.get(id=RMid).username
        print('this is the RM',Rm)
        data = {"data":posts}
        if channel_detail:
            return Response({"data":posts,"RM":Rm})
    except:
        return Response({"error":'not autheticated',
                         "status":400})
    

@login_required(login_url='/login/')
def rm_client_chat(request):
    # sys.stdout = open("agrachat.txt", "a")
    name = request.user.username
    print('namesauioefgsahdhg',name)
    username = request.user.id
    print('usernameasdhfguiosadh',username)
    user_channel = single_chat.objects.filter(user=username,channel_for_RM_chat=True).values()
    print('user_channel',len(user_channel))
    user_channels_and_channel_status = []
    for item in user_channel:
        channel = item['channel']
        print('channel',channel)
        channel_status = item['channel_status']
        other = single_chat.objects.filter(channel=channel).exclude(user=username).values().first()['user_id']
        print('this is other=----',other)
        other_user=Allusers.objects.get(id=str(other)).username
        # print(other_user)
        last_message = message.objects.filter(channel=channel).order_by('created').values()
        if last_message.exists():
            # print('ABCD')
            last_message = list(last_message)
            lmessage = last_message[-1]['body']
            lmessagetime = last_message[-1]['created'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            # print('1234')
            lmessage = ''
            lmessagetime = ''
        
        influencer = single_chat.objects.filter(channel=channel).exclude(user=username).values()[0]['user_id']
        print('influencer is here----',influencer)
        image=InfluencerProfile.objects.filter(influencer_userid=str(influencer))
        if image.exists():
            image=image[0].profileimage
        else:
            image=ClientProfile.objects.filter(client_userid=str(influencer))
            if image.exists():
                image=image[0].profileimage
            else:
                image=AgencyProfile.objects.filter(agency_userid=str(influencer))
                if image.exists():
                    image=image[0].profileimage
        
        unread_messages = len(list(message.objects.filter(channel=channel,status=False).exclude(sender=name).values()))
        
        user_channels_and_channel_status.append((name,channel,other_user,channel_status,lmessage,lmessagetime,image,unread_messages))
        # channel_name = f'{influencer_name}{username}'
        # posts = list(post.objects.filter(channel=channel_name).values())
    user_channels_and_channel_status.sort(key=lambda x: x[5], reverse=True)
    # print(user_channels_and_channel_status)
    return render(request,'Rm-client-chat.html',{'channels':user_channels_and_channel_status})


@api_view(['GET'])
def RM_single_show_chat(request,name,channel):
    # sys.stdout = open("agrachat.txt", "a")
    print(name,channel,end='\n')
    sender = name
    name=Allusers.objects.get(username=name).id
    user = single_chat.objects.filter(user=name)
    print(user)
    if user:
        seen_status = message.objects.filter(channel=channel,status=False).exclude(sender=sender).update(status=True)
    try:
        total_messages_len = message.objects.filter(channel=channel,sender=sender).values()
        print('this is the len:-- ',total_messages_len)
        channel_detail = single_chat.objects.filter(user=name,channel=channel).values().first()['channel_status']
        # print('details',channel_detail)
        posts = list(message.objects.filter(channel=channel).order_by('created').values())
        print('postes',posts)
        user_icon = single_chat.objects.filter(channel=channel).values()
        # print(user_icon)
        users = []
        for item in user_icon:
            icon_user = item['user_id']
            # print(icon_user)
            usern=Allusers.objects.get(id=icon_user)
            imag=None
            if usern.roles=='RM':
                imag=usern.rmprofile.profilepic
            if usern.roles=='client':
                imag=usern.clientprofile.profileimage
            if usern.roles=='influencer':
                imag=usern.influencerprofile.profileimage
            if usern.roles=='agency':
                imag=usern.agencyprofile.profileimage
            users.append((usern.username,usern.roles,str(imag)))
        showuser = {"users":users}
        data = {"data":posts}
        # sorted_data = sorted(data, key=lambda x: x['created'])
        # if channel_detail:
        return Response({"data":posts,"users":users,"status":channel_detail})
    except:
        return Response({"error":'not autheticated',
                         "status":400})



@login_required(login_url='/login/')
def create_Channel(request,influencer):
    cleint = request.user.username
    cleintid = request.user.id
    if influencer == cleint:
        return redirect("/client-influencer-chat/")
    else:
        influencerid = Allusers.objects.get(username=influencer)
        cleintid=Allusers.objects.get(id=cleintid)
        # time = str(datetime.datetime.now().time())[-6:]
        channel_c = cleint+influencer
        request.session['clicked-elemet-data'] = {'influencer':cleint,'channel':channel_c}
        if not channel_c in single_chat.objects.values_list("channel", flat=True):
            user1 = single_chat.objects.create(user=cleintid, channel=channel_c, channel_status=True)
            user2 = single_chat.objects.create(user=influencerid, channel=channel_c, channel_status=True)
            
            Thread(target=lambda:sendInfluencernotification(user=influencerid.id,key='influencer-chatinvitation',RM_Name=None,Influencer_Name=cleintid.username,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None)).start()
                        
            return redirect("/client-influencer-chat/")
        else:
            return redirect("/client-influencer-chat/")


def join(request,name,channel):
    pass
#     try:
#         channel_detail = chat_user.objects.filter(user=name,channel=channel).values().first()['channel_status']
#         # print(chat_user.objects.filter(user=name,channel=channel).values().first())
#         posts = message.objects.filter(channel=channel).order_by('-created').values()
#         context = {'posts':posts}
#         print(posts)
#         if channel_detail:
#             return render(request, 'feed.html', context)
#         else:
#             return render(request, 'feed_history.html', context)
#     except:
#         return HttpResponse('<div><h1>Unauthorised Please try again!!!! <a href="/"><button >Login</button></a></h1></div>')



def deavtivate_channel(request,name,channel):
    pass
#     # user = request.message.get('username')
#     # channel = request.message.get('channel')
#     chat_user.objects.filter(user=name,channel=channel).update(channel_status=False)
#     return HttpResponse('<div><h1>Channel Deactivated</h1></div>')






logger = logging.getLogger()
fh = logging.FileHandler('agora_chat_log.txt')
logger.addHandler(fh)


