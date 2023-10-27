from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
import sys

# save token w.r.t. user id
def savebrowesrid(request,token):
    userid = request.user.id
    user = Allusers.objects.get(id=userid)
    userobj = fcmuserandbrowerid.objects.filter(user=userid)
    if userobj.exists():
        fcmuserandbrowerid.objects.filter(user=user).update(browserid=token)
        return JsonResponse({'status':'updated token'})
    else:
        fcmuserandbrowerid.objects.create(user=user, browserid=token)
        return JsonResponse({'status':'saved token'})


# @csrf_exempt
def send_notification(registration_ids, message_title, message_desc):
    fcm_api = "AAAA4tu3chg:APA91bEdhIO0U6ZN8UayLh0dV-_tXEFhPxk8G_7rZp3d8m7NmHhPGf4Pp58_NQidCEnl2Pxowm4ehAS-OfMX2OSGAezaJiz4OAssIaNQtxoqiuQLy_DZUtxMNKQJ-GmXsjoPXNnnv35Y"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers ={
        "Content-Type":"application/json",
        "Authorization":"key="+fcm_api
    }
    
    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "sound" : "https://www.influencerhiring.com/media/notification.ogg",
            "click_action":"https://www.influencerhiring.com/",
            "image" : "https://www.influencerhiring.com/mainapp/static/images/logoIcon/logo_dark.png",
            "icon": "https://www.influencerhiring.com/mainapp/static/images/logoIcon/favicon.png",
        }
    }
    
    result = requests.post(url, data=json.dumps(payload), headers=headers)
    print(result.text)

def send():
    # sys.stdout = open("pushnoti.txt", "a")
    all_rows = SendNotificationtoUser.objects.all()
    if len(all_rows) != 0 :
        for row in all_rows:
            # print(row)
            try:
                userid = row.userid
                # print(userid)
                user = fcmuserandbrowerid.objects.get(user=userid)
                # print(userid)
                registration = [user.browserid]
                # print('A',registration)
            except:
                registration = ['']
            # print('B',registration)
            send_notification(registration, row.title, row.body)
            row.delete()
    return None
    # return HttpResponse("<div><h1>sent!! to </h1></div>")
# def sendhere(request):
#     send()
    
def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyC12zRqMZPpcx8o9tKTLSqDstUvOnL5N68",' \
         '        authDomain: "send-push-notification-77012.firebaseapp.com",' \
         '        projectId: "send-push-notification-77012",' \
         '        storageBucket: "send-push-notification-77012.appspot.com",' \
         '        messagingSenderId: "974348841496",' \
         '        appId: "1:974348841496:web:962860e313aca5098a096d",' \
         '        measurementId: "G-2BRNNG25XV"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'\

    return HttpResponse(data,content_type="text/javascript")


#######################################################################
###################### INFLUENCER FOLLOWER COUND UPDATE ###############
#######################################################################
from mainapp.models import *

def get_influencer_profilelink(request):
    
    if 'HTTP_AUTHORIZATION' in request.META:
        authorization_header = request.META['HTTP_AUTHORIZATION']
        if authorization_header=='cbvcasdghcvsdhcvjhsdgjhasdjhsdadjasjdjkhasjhdgjasd':
    
            data = PlatformProfileLink.objects.all()
            
            profile_links = []
            for item in data:
                userid = item.usersid.id
                platformanme=item.platformtype
                platid=Platforms.objects.get(platform_name=platformanme).platformid
                compredata=PlatformDetails.objects.filter(usersid=userid,platformtype=str(platid))
                if compredata.exists():
                    compredata=compredata[0]
                    if compredata.subscribers_followers is None or compredata.subscribers_followers==0 or compredata.subscribers_followers=='' :
                        profile_links.append((userid,platformanme,item.profilelink))
                else:
                    profile_links.append((userid,platformanme,item.profilelink))
        else:
            profile_links=None
                
        # pass
    return JsonResponse(profile_links,safe=False)



@csrf_exempt
def post_influencer_profiledata(request):
    profile_links=None
    if 'HTTP_AUTHORIZATION' in request.META:
        authorization_header = request.META['HTTP_AUTHORIZATION']
        if authorization_header=='cbvcasdghcvsdhcvjhsdgjhasdjhsdadjasjdjkhasjhdgjasd':
            sys.stdout = open("ainfluencerdata.txt", "a")
            userid = request.POST.get('userid')
            platformanme=request.POST.get('platformname')
            followers=request.POST.get('followers')
            platformcredential=request.POST.get('platformcredential')
            
            print(userid,platformanme,followers,platformcredential)
            platid=Platforms.objects.get(platform_name=platformanme).platformid
            compredata=PlatformDetails.objects.filter(usersid=userid,platformtype=str(platid))
            if compredata.exists():
                compredata=compredata[0]
                compredata.additiontime=timezone.now()
                compredata.isapproved=True
                compredata.subscribers_followers=followers
                compredata.platformcredential=platformcredential
                compredata.save(update_fields=['platformcredential','additiontime','isapproved','subscribers_followers'])
                profile_links='Update sucessfully'
            else:
                compredata=PlatformDetails()
                compredata.platformtype=str(platid)
                compredata.usersid=Allusers.objects.get(id=userid)
                compredata.additiontime=timezone.now()
                compredata.isapproved=True
                compredata.subscribers_followers=followers
                compredata.platformcredential=platformcredential
                compredata.save()
                profile_links='save sucessfully'
        else:
            profile_links='Not authorized'
                
    return JsonResponse(profile_links,safe=False)



