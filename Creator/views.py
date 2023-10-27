from django.shortcuts import render, HttpResponseRedirect
from mainapp.models import *
from .models import *
from inappnotifications.views import *
from Client.models import *
from Account.models import *
import random,string
from zoomeet.views import *
from zoomeet.models import *
from Admin.models import *
from RM.models import *
from django.contrib import messages
from inappnotifications.views import *
from agora_chat.models import *
from zoomeet.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from threading import Thread
from django.db import IntegrityError
import calendar
import logging
import sys
import json
from googleapiclient.discovery import build
import instaloader
from django.shortcuts import redirect
from datetime import datetime, timedelta
from mainapp.enanddc import encrypt, decrypt
from django.db.models import Q

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# from django.db import connection
from django.utils import timezone
# from django.contrib.sessions.models import Session
# from PIL import Image
from django.db.models import Sum, Case, When, F, Value, IntegerField, Count
# from django.utils.timezone import make_aware
from django.db.models.functions import ExtractMonth, Coalesce
from emil_send.views import existing_user
from django.views.decorators.csrf import csrf_exempt
from mainapp.views import get_location,get_timezone
# from geoip2 import database
# from whatsapp_login.views import decode_jwt_get_userdata
import math
# views.py
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def convert_to_indian_time(user_time, user_timezone):
    try:
        user_time_obj = datetime.strptime(user_time, '%Y-%m-%d %H:%M:%S')
        user_timezone = pytz.timezone(user_timezone)
       
        indian_timezone = pytz.timezone('Asia/Kolkata')
       
        user_time_obj = user_timezone.localize(user_time_obj)
        indian_time = user_time_obj.astimezone(indian_timezone)
       
        return indian_time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return str(e)



def convert_timezone_to_timezone(timestamp_str, from_timezone, to_timezone):
    try:
        timestamp_obj = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        from_tz = pytz.timezone(from_timezone)
        to_tz = pytz.timezone(to_timezone)

        timestamp_obj = from_tz.localize(timestamp_obj)

        converted_time = timestamp_obj.astimezone(to_tz)

        return converted_time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return str(e)
    
    
def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier




def get_date_from_days(days):
    
    current_date = datetime.now().date()
    total_seconds = days.total_seconds()
    total_days = total_seconds / (60 * 60 * 24)
    target_date = current_date + timedelta(days=total_days)
    return target_date


def get_monthly_orders(inforder):
    orders = inforder.annotate(
        month=ExtractMonth('orderdate')
    ).values('month').annotate(
        total_orders=Count('ordersid'),
        total_finalamt=Coalesce(
            Sum(
                Case(
                    When(iscouponapplied=False, then=F('finalamt')),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            Value(0)
        ),
        total_finalamtafterdiscount=Coalesce(Sum(
            Case(
                When(iscouponapplied=True, then=F('finalamtafterdiscount')),
                default=Value(0),
                output_field=IntegerField()
            )
        ),
            Value(0))
    ).order_by('month')

    monthly_data = []
    for order in orders:
        month_name = calendar.month_name[order['month']]
        finalamt = order['total_finalamt']
        finalamtafterdiscount = order['total_finalamtafterdiscount']

        if finalamt is None:
            finalamt = 0

        if finalamtafterdiscount is None:
            finalamtafterdiscount = 0

        monthly_data.append({
            'month': month_name,
            'total_orders': order['total_orders'],
            'total_finalamt': finalamt,
            'total_finalamtafterdiscount': finalamtafterdiscount
        })

    return monthly_data


def instagramdata(username):
    # bot = instaloader.Instaloader()
    #
    L = instaloader.Instaloader()
    username = "ankit_singhx"
    # L.login("bol7test", "Rblogin227$")
    L.login("bol72774", "Rbankit123$")
    profile = instaloader.Profile.from_username(L.context, username)
    print("rahul")
    print(profile.followers)
    return profile.followers


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
        pd.additiontime = datetime.now()
        pd.save(update_fields=['subscribers_followers', 'allviews'])
        print("function execute")
    else:
        dp = PlatformDetails(usersid=id, platformtype=platformid,
                             subscribers_followers=sub, allviews=views, additiontime=datetime.now())
        dp.save()
        print("insert youtube")


# Create your views here.

@login_required(login_url='/login/')
def Logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


@login_required(login_url='/login/')
def Influencer_Dashboard(request):
    sys.stdout = open("bsrb.txt", "a")
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
        
        print("ggjfjgfjgfjgjfg", rmname)
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'

    
        
    print('this is the fuckign channel', channel_name)
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    payout_history_entries = ClientPayoutHistory.objects.filter(clientid=userid,remark='Order Completed')

    # Extract the ordersid values from the queryset
    orders_id_list = list(payout_history_entries.values_list('paymentid__ordersid', flat=True))

   
    print('orders',orders_id_list)
    order = Orders.objects.select_related('serviceid').filter(
        influencerid=userid, paymentstatus=True)
    

    array = []
    array1 = []
    array2 = []
    array3 = []
    ordercom=order.filter(orderstatus=1,ordersid__in=orders_id_list)
    mon = get_monthly_orders(ordercom)
    print("data", mon)

    for i in mon:
        array.append(i['total_orders'])
        array1.append(i['total_finalamt']+i['total_finalamtafterdiscount'])
        array2.append(i['month'])
        amt = i['total_finalamt']+i['total_finalamtafterdiscount']
        
        num = amt/i['total_orders']
        rounded_num = round_up(num, 2)
        array3.append(rounded_num)

    com = order.filter(orderstatus=1).count()
    request.session['com'] = com
    can = order.filter(orderstatus=3).count()
    request.session['can'] = can
    pan = order.filter(orderstatus=5).count()
    request.session['pan'] = pan
    act = order.filter(orderstatus__in=[6,7]).count()
    request.session['act'] = act

    tot = order.count()
    request.session['tot'] = tot
    brand1 = order.filter(serviceid=1)
    brand = brand1.count()
    gm1 = order.filter(serviceid=4)
    gm = gm1.count()
    vcs1 = order.filter(serviceid=2)
    vcs = vcs1.count()
    ss1 = order.filter(serviceid=3)
    ss2 = order.filter(serviceid=7)
    ss = ss1.count()+ss2.count()
    ina1 = order.filter(serviceid=5)
    ina = ina1.count()

    totbrand = 0
    for i in brand1.filter(orderstatus=1,ordersid__in=orders_id_list):
        
            if i.iscouponapplied == True and i.finalamtafterdiscount > 0:
                totbrand = totbrand+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totbrand = totbrand+i.finalamt

    totgm = 0
    for i in gm1.filter(orderstatus=1,ordersid__in=orders_id_list):
        
            if i.iscouponapplied == True and i.finalamtafterdiscount > 0:

                totgm = totgm+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totgm = totgm+i.finalamt

    totvcs = 0
    for i in vcs1.filter(orderstatus=1,ordersid__in=orders_id_list):
        
            if i.iscouponapplied == True and i.finalamtafterdiscount > 0:
                totvcs = totvcs+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totvcs = totvcs+i.finalamt

    totina = 0
    for i in ina1.filter(orderstatus=1,ordersid__in=orders_id_list):
        
            if i.iscouponapplied == True and i.finalamtafterdiscount > 0:
                totina = totina+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totina = totina+i.finalamt

    totss = 0
    for i in ss1.filter(orderstatus=1,ordersid__in=orders_id_list):
        

        
            if i.iscouponapplied == True:
                totss = totss+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totss = totss+i.finalamt
    for i in ss2.filter(orderstatus=1,ordersid__in=orders_id_list):
        
        
            if i.iscouponapplied == True:
                totss = totss+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totss = totss+i.finalamt

    totalearn = totbrand+totgm+totvcs+totina+totss

    request.session['totalearn'] = totalearn

    if permissionname == 'influencer_permission':
        ac = InfluencerProfile.objects.select_related(
            'influencer_userid').filter(influencer_userid=userid)
        ac = ac[0]
        cyc = InfluencerSettings.objects.filter(influencer_userid=id)
        if cyc.exists():
            cyc = cyc[0]
        
        if 'feedratevalue' in request.POST:
            feedratevalue=request.POST.get('feedratevalue')
            feedmess=request.POST.get('feedmess')
                        
            if request.user.roles=='influencer':
                rmid=request.user.influencersettings.mappings.mappedtoid.rmid
            elif request.user.roles=='client':
                rmid=request.user.clientprofile.rmid.rmid
            else:
                rmid=request.user.agencyprofile.rmid.rmid
            
            inrew=RMsReview()
            inrew.clientid=Allusers.objects.get(id=str(request.user.id))
            inrew.rmid=Rmsettings.objects.get(rmid=str(rmid))
            if feedmess is not None and len(feedmess) > 0:
                inrew.review_message=feedmess
            if feedratevalue is not None and len(feedratevalue) > 0:
                inrew.rating=int(feedratevalue)
            inrew.isapproved=False
            inrew.save()
            print('save review')
        
        
      

        return render(request, "Creator/index.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'active': request.user.is_authenticated, 'cost': array3, 'monthname': array2, 'revenue': array1, 'completed_tasks': array, 'totina': totina, 'totvcs': totvcs,  'info': ac,  'kyc': cyc, 'com': com, 'tot': tot, 'can': can, 'pan': pan, 'act': act, 'brand': brand, 'gm': gm, 'vcs': vcs, 'ss': ss, 'ina': ina, 'total': totbrand, 'totgm': totgm, 'totss': totss, 'totalearn': totalearn})
    return HttpResponseRedirect("/")


@login_required(login_url='/login')
def deleteImage(request, num):
    #sys.stdout = open("bankdetails.txt", "a")
    print("imageid", num)
    try:
        image = Images.objects.get(imageid=num)
        image.delete()
        print("delete photos")
    except:
        pass
    return HttpResponseRedirect("/Photo-Gallery/")


@login_required(login_url='/login')
def deleteSubslots(request, num):
    #sys.stdout = open("bankdetails.txt", "a")
    print("imageid", num)
    try:
        image = Subslots.objects.get(subslotid=num)
        image.delete()
        print("delete photos")
    except:
        pass
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login')
def deleteVideo(request, num):
    try:
        videos = Videos.objects.get(videosid=num)
        videos.delete()
    except:
        pass
    return HttpResponseRedirect("/Video-Gallery/")


@login_required(login_url='/login')
def deleteVideolink(request, num):
    try:
        videolink = VideosLink.objects.get(videosLinkid=num)
        videolink.delete()
    except:
        pass
    return HttpResponseRedirect("/Video-Gallery/")


@login_required(login_url='/login')
def deletemycart(request, cartid):
    try:
        car = Cart.objects.get(Cartid=cartid)
        car.delete()
    except:
        pass
    return HttpResponseRedirect("/influencers/")


@login_required(login_url='/login')
def deletewish(request, wishid):
    try:
        car = Wishlist.objects.get(wishlistid=wishid)
        car.delete()
    except:
        pass
    return HttpResponseRedirect("/influencers/")


@login_required(login_url='/login/')
def Photo_Gallery(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    im = Images.objects.filter(im_userid=userid)
    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()

    

    username = id.email
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    kyc = InfluencerSettings.objects.get(influencer_userid=id).kyc
    if permissionname == 'influencer_permission':
        if request.method == 'POST':
            image_caption = request.POST.get("image_caption")
            photo = request.FILES.get("photo")
            imcap = Images(imagecaption=image_caption,
                           imagepath=photo, im_userid=id)
            imcap.save()
        return render(request, "Creator/photo-gallery.html", {'rmname':rmname,'image':image,'unread_status':unread_status, 'channel_name': channel_name, 'info': ac, 'user': username, 'kyc': kyc, 'images': im, 'noti': noti, 'notcount': conoti, })
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def Bank_Details(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    #sys.stdout = open("bankdetails.txt", "a")

    accoun = Useraccounts.objects.filter(usersid=id)
    if accoun.exists():
        accoun = accoun[0]
        accno = decrypt(accoun.accountnumber)
        print("account", accno, accoun.accountnumber)
    else:
        accno = ''

    cyc = InfluencerSettings.objects.filter(influencer_userid=id)
    if cyc.exists():
        cyc = cyc[0]
    docs = UserDocuments.objects.filter(usersid=id)

    depan = docs.filter(documentname='Pan')
    if depan.exists():
        depan = depan[0]

    deaddhar = docs.filter(documentname='Addhar')
    if deaddhar.exists():
        deaddhar = deaddhar[0]

    decan = docs.filter(documentname='Cancel Cheque')
    if decan.exists():
        decan = decan[0]
    depass = docs.filter(documentname='Passport')
    if depass.exists():
        depass = depass[0]

    totalearn = request.session.get('totalearn', None)
    tot = request.session.get('tot', None)
    com = request.session.get('com', None)

    
    if permissionname == 'influencer_permission':
        if request.method == 'POST':
            #sys.stdout = open("earningsdetails.txt", "a")
            
            print("fsd", request.POST)
            bankname = request.POST.get("bankname")
            currcode = request.POST.get("currnecy")
            accountname = request.POST.get("accountname")
            accountnumber = request.POST.get("accountno")
            accountnumber1 = encrypt(accountnumber)
            ifsccode = request.POST.get("branchcode")
            pan = request.FILES.get("pan")
            aadhar = request.FILES.get("aadhar")
            cancel = request.FILES.get("cancel")
            passport = request.FILES.get("passport")

            print("baraeal")
            print(bankname,currcode,accountname,accountnumber)
            print(ifsccode,pan,aadhar,cancel)

            ac = Useraccounts.objects.filter(usersid=id)
            if ac.exists():
                ac = ac[0]
                if bankname is not None and len(bankname) > 1:
                    ac.bankname = bankname
                    ac.save(update_fields=['bankname'])
                    print("update bankname", bankname)
                if currcode is not None and len(currcode) > 1:
                    ac.currencycode = currcode
                    ac.save(update_fields=['currencycode'])
                    print("update currcode", currcode)
                if accountname is not None and len(accountname) > 0:
                    ac.account_name = accountname
                    ac.save(update_fields=['account_name'])
                    print("update account_name", accountname)
                if accountnumber is not None and len(accountnumber) > 0:
                    ac.accountnumber = accountnumber1
                    ac.save(update_fields=['accountnumber'])
                    print("update accountnumber", accountnumber)
                if ifsccode is not None and len(ifsccode) > 0:
                    ac.ifsc_codes = ifsccode
                    ac.save(update_fields=['ifsc_codes'])
                    print("update ifsccode", ifsccode)
            else:
                ac = Useraccounts()
                ac.usersid = id
                if bankname is not None and len(bankname) > 0:
                    ac.bankname = bankname
                if currcode is not None and len(currcode) > 0:
                    ac.currencycode = currcode
                if accountname is not None and len(accountname) > 0:
                    ac.account_name = accountname
                if accountnumber is not None and len(accountnumber) > 0:
                    ac.accountnumber = accountnumber1
                if ifsccode is not None and len(ifsccode) > 0:
                    ac.ifsc_codes = ifsccode
                ac.save()
                print("insert accounts")

            dc = UserDocuments.objects.filter(usersid=id)
            if dc.exists():
                if pan is not None and len(pan) > 0:
                    dc1 = dc.filter(documentname='Pan')
                    if dc1.exists():
                        dc1 = dc1[0]
                        dc1.documentpath = pan
                        dc1.save(update_fields=['documentpath'])
                        print('update pan')
                    else:
                        dc = UserDocuments()
                        dc.usersid = id
                        dc.documentpath = pan
                        dc.documentname = 'Pan'
                        dc.save()
                        print("insert pan")
                if aadhar is not None and len(aadhar) > 0:
                    dc2 = dc.filter(documentname='Addhar')
                    if dc2.exists():
                        dc2 = dc2[0]
                        dc2.documentpath = aadhar
                        dc2.save(update_fields=['documentpath'])
                        print('update addhar')
                    else:
                        dc = UserDocuments()
                        dc.usersid = id
                        dc.documentpath = aadhar
                        dc.documentname = 'Addhar'
                        dc.save()
                        print("insert addhar")
                if cancel is not None and len(cancel) > 0:
                    dc3 = dc.filter(documentname='Cancel Cheque')
                    if dc3.exists():
                        dc3 = dc3[0]
                        dc3.documentpath = cancel
                        dc3.save(update_fields=['documentpath'])
                        print('update cancel')
                    else:
                        dc = UserDocuments()
                        dc.usersid = id
                        dc.documentpath = cancel
                        dc.documentname = 'Cancel Cheque'
                        dc.save()
                        print("insert cancel")
                if passport is not None and len(passport) > 0:
                    print('passwoprt', passport)
                    dc3 = dc.filter(documentname='Passport')
                    if dc3.exists():
                        dc3 = dc3[0]
                        dc3.documentpath = passport
                        dc3.save(update_fields=['documentpath'])
                        print('update passport')
                    else:
                        dc = UserDocuments()
                        dc.usersid = id
                        dc.documentpath = passport
                        dc.documentname = 'Passport'
                        dc.save()
                        print("insert passport")
            else:
                print('bank details insert')
                if pan is not None and len(pan) > 0:
                    dc = UserDocuments()
                    dc.usersid = id
                    dc.documentpath = pan
                    dc.documentname = 'Pan'
                    dc.save()
                    print("insert pan")
                if aadhar is not None and len(aadhar) > 0:
                    dc = UserDocuments()
                    dc.usersid = id
                    dc.documentpath = aadhar
                    dc.documentname = 'Addhar'
                    dc.save()
                    print("insert addhar")
                if cancel is not None and len(cancel) > 0:
                    dc = UserDocuments()
                    dc.usersid = id
                    dc.documentpath = cancel
                    dc.documentname = 'Cancel Cheque'
                    dc.save()
                    print("insert cancel")
                if passport is not None and len(passport) > 0:
                    dc = UserDocuments()
                    dc.usersid = id
                    dc.documentpath = passport
                    dc.documentname = 'Passport'
                    dc.save()
                    print("insert passport")
            send_customer_email(key='influencer-kycvarificationrequest',user_email=request.user.email,client=None,influencer=request.user.username,order_id=None,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)

            sendkycmanagernotification(user=103899,key="kyc-influencervarification",influencer_user_name=request.user.username,client_name=None)

            return redirect(request.META['HTTP_REFERER'])
        #sys.stdout.close()
        return render(request, "Creator/bank-details.html", {'rmname':rmname,'image':image,'unread_status':unread_status, 'channel_name': channel_name, 'active': request.user.is_authenticated, 'com': com,  'tot': tot, 'totalearn': totalearn, 'info': ac, 'pass': depass, 'pan': depan, 'addhar': deaddhar, 'cancel': decan, 'kyc': cyc, 'account': accoun, 'accnum': accno})
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def Earning(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = single_chat.objects.filter(channel=channel_name).values().exclude(user_id=userid).first()['user_id']
        image=Rmprofile.objects.get(rmid=rmid)
        rmname=image.name
        image=image.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    # cursor = connection.cursor()
    # #sys.stdout = open("earningsdetails.txt", "a")
    # cursor.execute('select * from ordersdetails(%s,%s,%s)', [1, userid, 0])
    # oddr = cursor.fetchall()
    # print("Rahul")
    # print('orderdetals', oddr)
    # cursor.close()
   
   
    oddr=ClientPayoutHistory.objects.filter(clientid=str(request.user.id),remark='Order Completed').order_by('-payouthistoryid')
    username = request.user.email
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc

    if permissionname == 'influencer_permission':
        return render(request, "Creator/earnings.html", {'rmname':rmname,'image':image,'unread_status':unread_status, 'channel_name': channel_name, 'info': ac, 'user': username, 'kyc': kyc, 'earn': oddr, })
    return HttpResponseRedirect("/")



@login_required(login_url='/login/')
def Activity(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
    username = Allusers.objects.get(id=userid).email
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]

    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    if permissionname == 'influencer_permission':
        return render(request, "Creator/activity.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'active': request.user.is_authenticated, 'info': ac, 'user': username, 'noti': noti, 'notcount': conoti, })
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def Video_Gallery(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    vd = Videos.objects.filter(vd_userid=userid)

    rmid = single_chat.objects.filter(channel=channel_name).values().exclude(user_id=userid).first()['user_id']
    image=Rmprofile.objects.get(rmid=rmid).profilepic

    username = id.email
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    kyc = InfluencerSettings.objects.get(influencer_userid=id).kyc

    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    if permissionname == 'influencer_permission':
        vl = VideosLink.objects.filter(
            vl_userid=userid, videolinkpurpose__isnull=False)
        if request.method == 'POST':
            #sys.stdout = open("photo.txt", "a")
            print(request.POST)
            videolink = request.POST.get("videolink")
            linkpurpose = request.POST.get("linkpurpose")

            photo = request.FILES.get("photo")
            print("link phto", photo)

            # For Youtube Shorts
            videolink = videolink.replace(
                'youtube.com/shorts/', 'www.youtube.com/embed/')
            videolink = videolink.replace('?feature=share', '')
            print("avsf", videolink)
            # For Youtube Videos
            videolink = videolink.replace('youtu.be', 'www.youtube.com/embed')
            print("new", linkpurpose)
            lk = VideosLink(videosLink=videolink,
                            videolinkpurpose=linkpurpose, thumbnail=photo, vl_userid=id)
            lk.save()
            print("insert video link")
        return render(request, "Creator/video-gallery.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'info': ac, 'user': username, 'kyc': kyc, 'video': vd, 'link': vl, 'noti': noti, 'notcount': conoti, })
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def Select_Account(request):
    try:
        user = request.user.id
        id = Allusers.objects.filter(id=user)
        id = id[0]
        permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
            userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

        exch = ExchangeRates.objects.all().order_by('country')

        if permissionname == 'client_permission':
            if request.user.profilestatus == False:

                return render(request, "Creator/select-account.html", {
                    'exch': exch, })
            else:
                return HttpResponseRedirect("/")
    except IntegrityError:
        messages.warning(request,
                         f'IntegrityError Some problem occured, reason:{type(error).__name__}')
    except Exception as error:
        print('Exception occured:', type(error).__name__)
        messages.warning(request,
                         f'Some problem occured , reason:{type(error).__name__}')
        return redirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect("/")


# def Select_Account_for_whatsapp(request,token):
#     data=decode_jwt_get_userdata(token)
#     mob=data['mobile']
#     username = data['username']
#     user_instance = Allusers.objects.get(username=username)
#     try:
#         user = user_instance.id
#         id = Allusers.objects.filter(id=user)
#         id = id[0]
#         permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
#             userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

#         exch = ExchangeRates.objects.all().order_by('country')

#         if permissionname == 'client_permission':
#             if request.user.profilestatus == False:

#                 return render(request, "Creator/select-account.html", {
#                     'exch': exch, })
#             else:
#                 return HttpResponseRedirect(f"/Loginappuser/{token}/")
#     except IntegrityError:
#         messages.warning(request,
#                          f'IntegrityError Some problem occured, reason:{type(error).__name__}')
#     except Exception as error:
#         print('Exception occured:', type(error).__name__)
#         messages.warning(request,
#                          f'Some problem occured , reason:{type(error).__name__}')
#         return redirect(request.META['HTTP_REFERER'])
#     return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def Order1(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    username = Allusers.objects.get(id=userid).email
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    kyc = InfluencerSettings.objects.get(influencer_userid=id).kyc

    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    order = Orders.objects.select_related('serviceid', 'clientid', 'orderstatus').filter(
        influencerid=userid, paymentstatus=True).order_by('-ordersid')
    tot = order.count()
    act = order.filter(orderstatus__in=[6,7]).count()
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    order = order.filter(orderstatus=5)
    pan = order.count()

    if permissionname == 'influencer_permission':
        
        return render(request, "Creator/orders.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'unread_status':unread_status,'channel_name': channel_name, 'active': request.user.is_authenticated, 'noti': noti, 'notcount': conoti, 'com': com, 'tot': tot, 'can': can, 'pan': pan, 'act': act, 'info': ac, 'user': username, 'kyc': kyc, 'order': order})
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def Cancel_Orders(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    username = Allusers.objects.get(id=userid).email
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    kyc = InfluencerSettings.objects.get(influencer_userid=id).kyc
    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    order = Orders.objects.select_related('serviceid', 'clientid', 'orderstatus').filter(
        influencerid=userid, paymentstatus=True).order_by('-ordersid')
    tot = order.count()
    act = order.filter(orderstatus__in=[6,7]).count()
    pan = order.filter(orderstatus=5).count()
    com = order.filter(orderstatus=1).count()
    order = order.filter(orderstatus=3)
    can = order.count()
    if permissionname == 'influencer_permission':
        return render(request, "Creator/cancel-order.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'active': request.user.is_authenticated, 'info': ac, 'user': username, 'kyc': kyc, 'order': order, 'noti': noti, 'notcount': conoti, 'com': com, 'tot': tot, 'can': can, 'pan': pan, 'act': act})
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def Complete_Orders(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    username = Allusers.objects.get(id=userid).email
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    kyc = InfluencerSettings.objects.get(influencer_userid=id).kyc
    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    order = Orders.objects.select_related('serviceid', 'clientid', 'orderstatus').filter(
        influencerid=userid, paymentstatus=True).order_by('-ordersid')
    tot = order.count()
    act = order.filter(orderstatus__in=[6,7]).count()
    pan = order.filter(orderstatus=5).count()
    can = order.filter(orderstatus=3).count()
    order = order.filter(orderstatus=1)
    com = order.count()
    if permissionname == 'influencer_permission':
        return render(request, "Creator/completed-order.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'active': request.user.is_authenticated, 'info': ac, 'user': username, 'kyc': kyc, 'order': order, 'noti': noti, 'notcount': conoti, 'com': com, 'tot': tot, 'can': can, 'pan': pan, 'act': act})
    return HttpResponseRedirect("/")


def compafterdays():
    ostid = Orderstatus.objects.get(status='Completed')
    sctk=ScheduleCompletionTasks.objects.filter(comptask=False)
    #sys.stdout = open("serviceplan.txt", "a")
    for i in sctk:
        if timezone.now() == i.date+timedelta(days=7):
            oid = Orders.objects.get(ordersid=str(i.orderid))
            oid.orderstatus = ostid
            oid.completedate = timezone.now()
            oid.save(update_fields=[
                        'orderstatus', 'completedate'])
            
            
            clientid=oid.influencerid.influencer_userid
            clientpayout, created = ClientPayout.objects.get_or_create(clientid=clientid, defaults={
            'remaining_balance_bank':0, 'successful_withdrawal_bank':0, 'hold_bank':0,
        
            })
        
            payments=Payments.objects.get(ordersid=str(oid.ordersid))
            
            requested_currency =payments.ordersid.paymentcurrency
            if requested_currency == 'INR':
                
                
                if oid.iscouponapplied==True:
                    newprice=oid.planid.planprice-oid.totaldiscount
                    clientpayout.remaining_balance_bank += newprice
                else:
                
                    clientpayout.remaining_balance_bank += oid.planid.planprice
                    newprice=oid.planid.planprice
                
                
                clientpayout.currency=requested_currency
                clientpayout.save()
                clientpayouthistory = ClientPayoutHistory(clientid=clientid, paymentid=payments,requested_currency=requested_currency,wallet_transaction_amount=int(newprice),isrefund_balance=True,isrefund_hold=False,remark='Order Completed')
                clientpayouthistory.save()
                payments.is_refunded=True
                payments.save()
            
            
            
            print('execue')
        i.comptask=True
        i.save(update_fields=['comptask'])
    


@login_required(login_url='/login/')
def Accepted_Orders(request):
    #sys.stdout = open("serviceplan.txt", "a")
    
    print('time',timezone.localtime(timezone.now()))
    
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    username = Allusers.objects.get(id=userid).email
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    kyc = InfluencerSettings.objects.get(influencer_userid=id).kyc
    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    order = Orders.objects.select_related('serviceid', 'clientid', 'orderstatus').filter(
        influencerid=userid, paymentstatus=True).order_by('-ordersid')
    tot = order.count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    com = order.filter(orderstatus=1).count()
    order = order.filter(orderstatus__in=[6, 7])
    act = order.count()
    
    
    
        
    
    
    
    if permissionname == 'influencer_permission':
        if "acceptorder" in request.POST:
            uploadvideo = request.FILES.get("uploadvideo")
            videolink = request.POST.get("videolink")
            ordersummay = request.POST.get("ordersummay")
            ordeid = request.POST.get('acceptorder')
            # For Youtube Shorts
            
            

            if videolink is not None and len(videolink) > 1:
                # videolink = videolink.replace(
                # 'youtube.com/shorts/', 'www.youtube.com/embed/')
                # videolink = videolink.replace('?feature=share', '')
                # print("avsf", videolink, uploadvideo, ordersummay)
                # # For Youtube Videos
                # videolink = videolink.replace('youtu.be', 'www.youtube.com/embed')
                lk = VideosLink(videosLink=videolink,
                                vl_userid=id,videolinkpurpose='Order Related')
                lk.save()
            else:
                lk=''
            if uploadvideo is not None and len(uploadvideo) > 1:
                vd = Videos(videospath=uploadvideo, vd_userid=id,purpose='Order Related')
                vd.save()
            else:
                vd=''
            oid = Orders.objects.get(ordersid=ordeid)
            res = OrderResponse.objects.filter(orderid=ordeid)
            if res.exists():
                res = res[0]
                if vd !='':
                    res.videoid = vd
                if lk!='':
                    res.videolink = lk
                res.ordersummary = ordersummay
                res.save(update_fields=['videoid',
                         'videolink', 'ordersummary'])
            else:
                res = OrderResponse()
                res.orderid=oid
                if vd !='':
                    res.videoid=vd
                if lk!='':
                    res.videolink=lk
                res.ordersummary=ordersummay
                res.save()
            
            sctk=ScheduleCompletionTasks(orderid=oid,date=timezone.now(),comptask=False)
            sctk.save()
          
            ostid = Orderstatus.objects.get(status='Processing')
            oid.orderstatus = ostid
            oid.acceptancedate = timezone.now()
            oid.save(update_fields=[
                        'orderstatus','acceptancedate'])
            # existing_user(request,name=oid.clientid.client_userid.username,user_type='existing_user',email_add=oid.clientid.client_userid.email,template_name='order-completed.html',subject='Your Order #'+str(oid.ordersid)+' is Complete!',order_date=oid.orderdate,order_no=oid.ordersid,tracking_no='None')
            Thread(target=lambda: existing_user(request, name=oid.clientid.username, user_type='existing_user', email_add=oid.clientid.email,
                   template_name='order-completed.html', subject='Your Order #'+str(oid.ordersid)+' is Complete!', order_date=oid.orderdate, order_no=oid.ordersid, tracking_no='None')).start()
            
            send_customer_email(key='client/agency-orderreviewbyinfluencer',user_email=oid.clientid.email,
                   client=oid.clientid.username,influencer=oid.influencerid.influencer_userid.username,order_id=oid.ordersid,service_type=oid.serviceid.servicename,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)   
            
            send_customer_email(key='influencer-orderreviewbyinfluencer',user_email=oid.influencerid.influencer_userid.email,
                   client=oid.clientid.username,influencer=oid.influencerid.influencer_userid.username,order_id=oid.ordersid,service_type=oid.serviceid.servicename,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)   
            
            
            
            
            if oid.clientid.roles=='client':
                Thread(target=lambda:sendusernotification(user=oid.clientid.id,key='user-revieworder',RM_Name=None,Influencer_Name=oid.influencerid.influencer_userid.username,Product_Name=oid.serviceid.servicename,Decline_Reason=None,Order_Id=oid.ordersid)).start()
            
            if oid.clientid.roles=='agency':            
                Thread(target=lambda:sendagencynotification(user=oid.clientid.id,key='agency-revieworder',castingcallid=None,RM_Name=None,Influencer_Name=oid.influencerid.influencer_userid.username,Product_Name=oid.serviceid.servicename,Decline_Reason=None,Order_Id=oid.ordersid)).start()            
            
            
            
            Thread(target=lambda:sendRMnotification(key='rm-influencersubmitorder',RM_Name=None,client_type=None,client_Name=oid.clientid.username,rmid=oid.rmid,Influencer_Name=oid.influencerid.influencer_userid.username,Order_ID=oid.ordersid,reason=None,Order_Stage=None)).start()

            Thread(target=lambda:sendInfluencernotification(user=oid.influencerid.influencer_userid.id,key='influencer-orderforuserreview',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=oid.ordersid,reason=None)).start()

            
            print("szave response")

        return render(request, "Creator/accepted-order.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'active': request.user.is_authenticated, 'info': ac, 'user': username, 'kyc': kyc, 'order': order, 'noti': noti, 'notcount': conoti, 'com': com, 'tot': tot, 'can': can, 'pan': pan, 'act': act})
    return HttpResponseRedirect("/")





def get_info_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    port = request.META['SERVER_PORT']
    # #sys.stdout = open("ip.txt", "a")
    print("IP", ip, port)
    return ip


def get_timezone_from_ip(ip_address):
    try:
        response = requests.get(f'http://ipinfo.io/{ip_address}/json')
        data = response.json()
       
        if 'timezone' in data:
            return data['timezone']
        else:
            return 'Asia/Kolkata'
    except Exception as e:
        return str(e)

    
    

def convert_to_timezone(timestamp_str, from_timezone, to_timezone):
    # Convert the timestamp string to a datetime object
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

    # Define the time zones
    from_tz = pytz.timezone(from_timezone)
    to_tz = pytz.timezone(to_timezone)

    # Convert the datetime object to the source time zone
    timestamp_with_from_tz = from_tz.localize(timestamp)

    # Convert the timestamp to the target time zone
    timestamp_with_to_tz = timestamp_with_from_tz.astimezone(to_tz)

    return timestamp_with_to_tz.strftime('%Y-%m-%d %H:%M:%S %Z')



@login_required(login_url='/login/')
def Service_Plan(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    username = Allusers.objects.get(id=userid).email
    id = Allusers.objects.filter(id=userid)
    id = id[0]

    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.filter(influencer_userid=userid)
    ac = ac[0]
    
    rates=ExchangeRates.objects.get(countery_abbrevation=str(ac.currency)).rates

    iset = InfluencerSettings.objects.filter(influencer_userid=userid)
    if iset.exists():
        iset = iset[0]

    stt123 = Servicetabtitle.objects.filter(influencerid=userid)

    # ser=Services.objects.filter(Q(servicename__isnull=False) | Q(subservice__isnull=False)).values_list('servicename', 'subservice','serviceid').order_by('serviceid')

    ser = Services.objects.all().values_list(
        'servicename', 'subservice', 'serviceid').order_by('serviceid')

    ent = Eventtype.objects.all().values_list(
        'eventtype', 'eventtypeid').order_by('eventtypeid')

    print("ser", ser)
    print("type", type(ser))

    plan = PricingPlans.objects.filter(usersid=id, serviceid=1)
    debasic = None
    destd = None
    depre = None
    if plan.exists():
        debasic = plan.filter(plan_type='Basic')
        if debasic.exists():
            debasic = debasic[0]
            debasic.planprice=debasic.planprice*rates
            debasic.exculsiveprice=debasic.exculsiveprice*rates
            
        destd = plan.filter(plan_type='Standard')
        if destd.exists():
            destd = destd[0]
            destd.planprice=destd.planprice*rates
            destd.exculsiveprice=destd.exculsiveprice*rates
            print('destd', destd)

        depre = plan.filter(plan_type='Premium')
        if depre.exists():
            depre = depre[0]
            depre.planprice=depre.planprice*rates
            depre.exculsiveprice=depre.exculsiveprice*rates

    event_price = ''
    gm_price = ''
    vc_price = ''

    pry = PricingPlans.objects.filter(usersid=id)
    if pry.exists():
        event_price = pry.filter(serviceid=5)
        if event_price.exists():
            event_price = event_price[0]
            event_price.planprice=event_price.planprice*rates
            event_price.exculsiveprice=event_price.exculsiveprice*rates
        else:
            event_price = ''
        gm_price = pry.filter(serviceid=4)
        if gm_price.exists():
            gm_price = gm_price[0]
            gm_price.planprice=gm_price.planprice*rates
            gm_price.exculsiveprice=gm_price.exculsiveprice*rates
        else:
            gm_price = ''
        vc_price = pry.filter(serviceid=2)
        if vc_price.exists():
            vc_price = vc_price[0]
            vc_price.planprice=vc_price.planprice*rates
            vc_price.exculsiveprice=vc_price.exculsiveprice*rates
        else:
            vc_price = ''

    plan1 = PricingPlans.objects.filter(usersid=id, serviceid=7)
    if plan1.exists():
        debasic1 = plan1.filter(plan_type='Basic')
        if debasic1.exists():
            debasic1 = debasic1[0]
            debasic1.planprice=debasic1.planprice*rates
            debasic1.exculsiveprice=debasic1.exculsiveprice*rates
        else:
            debasic1 = ''
        destd1 = plan1.filter(plan_type='Standard')
        if destd1.exists():
            destd1 = destd1[0]
            destd1.planprice=destd1.planprice*rates
            destd1.exculsiveprice=destd1.exculsiveprice*rates
        else:
            destd1 = ''
        depre1 = plan1.filter(plan_type='Premium')
        if depre1.exists():
            depre1 = depre1[0]
            depre1.planprice=depre1.planprice*rates
            depre1.exculsiveprice=depre1.exculsiveprice*rates
        else:
            depre1 = ''
    else:
        debasic1 = None
        destd1 = None
        depre1 = None

    plan2 = PricingPlans.objects.filter(usersid=id, serviceid=3)
    if plan2.exists():
        debasic2 = plan2.filter(plan_type='Basic')
        if debasic2.exists():
            debasic2 = debasic2[0]
            debasic2.planprice=debasic2.planprice*rates
            debasic2.exculsiveprice=debasic2.exculsiveprice*rates
        else:
            debasic2 = ''
        destd2 = plan2.filter(plan_type='Standard')
        if destd2.exists():
            destd2 = destd2[0]
            destd2.planprice=destd2.planprice*rates
            destd2.exculsiveprice=destd2.exculsiveprice*rates
        else:
            destd2 = ''
        depre2 = plan2.filter(plan_type='Premium')
        if depre2.exists():
            depre2 = depre2[0]
            depre2.planprice=depre2.planprice*rates
            depre2.exculsiveprice=depre2.exculsiveprice*rates
        else:
            depre2 = ''
    else:
        debasic2 = None
        destd2 = None
        depre2 = None

    totalearn = request.session.get('totalearn', None)
    tot = request.session.get('tot', None)
    com = request.session.get('com', None)
    kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc
    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    current_datetime = datetime.now()
    
    country = get_location(request)
    
    subsslots = Subslots.objects.filter(
        influencerid=str(id),starttime__gte=current_datetime).order_by('-subslotid')
    
    if country !='India':    
        user_ip=get_info_ip(request)
        user_timezone=get_timezone_from_ip(user_ip)
    else:
        user_timezone='Asia/Kolkata'
        # ustim=Defaulttimezoneinfluencer.objects.filter(userid=str(request.user.id))
        # if ustim.exists():
        #     user_timezone=ustim[0].timezone
        # else:
            # user_timezone='None'
        # if user_timezone!='Asia/Kolkata':
        #     for i in subsslots:
        #         i.starttime=convert_timezone_to_timezone(i.starttime,user_timezone,'Asia/Kolkata')
        #         i.endtime=convert_timezone_to_timezone(i.endtime,user_timezone,'Asia/Kolkata')
            
    try:
        currency=request.user.influencerprofile.currency
        if currency is None or currency =='':
            permissionname=None
                   
    except:
        permissionname=permissionname
        
        
    
    
        
    

    if permissionname == 'influencer_permission':

        if request.method == 'POST':
            #sys.stdout = open("serviceplan.txt", "a")
            print('date', request.POST)

            vc_start_date = request.POST.get('vc_start_date')
            vc_start_time = request.POST.get('vc_start_time')

            # vc_end_date = request.POST.get('vc_end_date')
            vc_end_time = request.POST.get('vc_end_time')
            slot_duration = request.POST.get('slot_duration')
            
            vc_end_date=vc_start_date
            

            if vc_end_date is not None and vc_start_time is not None and vc_start_date is not None and vc_end_time is not None and len(vc_end_date) > 1 and len(vc_start_time) > 1 and len(vc_end_time) > 1 and len(vc_start_date) > 1:
                vc_start_date = datetime.strptime(
                    vc_start_date, "%Y-%m-%d").date()
                vc_start_time = datetime.strptime(
                    vc_start_time, "%H:%M").time()

                # combine the date and time into a single datetime object
                vc_start_datetime = datetime.combine(
                    vc_start_date, vc_start_time)
                
                country = get_location(request)
                timezone1 = get_timezone(request)
                
                deftime=Defaulttimezoneinfluencer.objects.filter(userid=str(request.user.id))
                if deftime.exists():
                    deftime=deftime[0]
                    deftime.timezone=timezone1
                    deftime.save(update_fields=['timezone'])
                else:
                    deftime=Defaulttimezoneinfluencer()
                    deftime.userid=Allusers.objects.get(id=str(request.user.id))
                    deftime.timezone=timezone1
                    deftime.save()
                
                
                if country != 'India':
                    
                    vc_start_datetime=str(vc_start_datetime)
                    vc_start_datetime=convert_to_indian_time(vc_start_datetime,timezone1)
                    vc_start_datetime=datetime.strptime(vc_start_datetime, "%Y-%m-%d %H:%M:%S")
                    
                    
                    print("vc_start_datetime",vc_start_datetime)
                
                print("vc_start_datetime1",vc_start_datetime)
                vc_end_date = datetime.strptime(vc_end_date, "%Y-%m-%d").date()
                vc_end_time = datetime.strptime(vc_end_time, "%H:%M").time()

                # combine the date and time into a single datetime object
                vc_end_datetime = datetime.combine(vc_end_date, vc_end_time)
                
                
                if country != 'India':
                    vc_end_datetime=str(vc_end_datetime)
                    vc_end_datetime=convert_to_indian_time(vc_end_datetime,timezone1)
                    vc_end_datetime=datetime.strptime(vc_end_datetime, "%Y-%m-%d %H:%M:%S")
                    
                    
                    print("vc_end_datetime",vc_end_datetime)
                
                print("vc_end_datetime1",vc_end_datetime)
                




                durationslot = vc_end_datetime-vc_start_datetime

                print('duration', durationslot)
                print("vc_end_datetime1",vc_end_datetime,type(vc_end_datetime))
                
                slts=Slots.objects.filter(starttime=vc_start_datetime,influencerid=request.user.id)
                if slts.exists():
                    messages.warning(request,'Your slots of this date and time already exists.')
                else:
                    sslots = Slots(slottype='Video Chat', starttime=vc_start_datetime, influencerid=iset, slotduration=durationslot,
                                isactive=True, singleslotduration=slot_duration, slotperminprice=int(vc_price.increasedprice))
                    sslots.save()
                
                print('inserte slosst')
                
            if "deleteexistslots" in request.POST:     
                deleteexistslots = request.POST.get('deleteexistslots')
                if deleteexistslots==1 or deleteexistslots=='1':
                    Subslots.objects.filter(
                        isreferenced__in=[False, None],
                        isbooked__in=[False, None],
                        influencerid=str(request.user.id)
                    ).delete()
                
                    print("rahul",deleteexistslots)
                         
                
                
                
                

            frontlist = dict(request.POST)

            if "CheckboxGroup1" in frontlist:
                serve = frontlist["CheckboxGroup1"]
                ac.services = list(serve)
                ac.save(update_fields=['services'])
                # print("updaate serviceid")

            if "CheckboxGroup2" in frontlist:
                serve = frontlist["CheckboxGroup2"]
                ac.events = list(serve)
                ac.save(update_fields=['events'])

            brandtab = request.POST.get('brandtab')

            greetingtab = request.POST.get('greetingmess')

            shouttab = request.POST.get('shouttab')
            influenceracquisitiontab = request.POST.get(
                'influenceracquisitiontab')
            videochattab = request.POST.get('videochattab')
            stt = Servicetabtitle.objects.filter(influencerid=userid)
            if stt.exists():
                stt = stt[0]
                if brandtab is not None and len(brandtab) > 1:
                    stt.brandtag = brandtab
                    stt.save(update_fields=['brandtag'])
                    # print("update brandtag")
                if greetingtab is not None and len(greetingtab) > 1:
                    stt.greetingtag = greetingtab
                    stt.save(update_fields=['greetingtag'])
                    # print("update greetingtab")
                if shouttab is not None and len(shouttab) > 1:
                    stt.shouttag = shouttab
                    stt.save(update_fields=['shouttag'])
                    # print("update shouttag")
                if videochattab is not None and len(videochattab) > 1:
                    stt.videochattag = videochattab
                    stt.save(update_fields=['videochattag'])
                    # print("update videochattag")
                if influenceracquisitiontab is not None and len(influenceracquisitiontab) > 1:
                    stt.influenceracquasitiontag = influenceracquisitiontab
                    stt.save(update_fields=['influenceracquasitiontag'])
                    # print("update influenceracquasitiontag")
            else:
                stt1 = Servicetabtitle(influencerid=iset, brandtag=brandtab, greetingtag=greetingtab,
                                       shouttag=shouttab, videochattag=videochattab, influenceracquasitiontag=influenceracquisitiontab)
                stt1.save()
                # print("save services tabs.")

            basic_price = request.POST.get('bpprice')
            basic_del_time = request.POST.get('bpdt')
            exculsiveprice = request.POST.get('exculsiveprice')
            exclusivedeliverytime = request.POST.get('exclusivedeliverytime')
            basic_plan_perks = request.POST.get('bpplanperks')
            brevisiontimes = request.POST.get('brevisiontimes')

            stand_del_time = request.POST.get('sddt')
            stand_price = request.POST.get('sdprice')
            stand_plan_perks = request.POST.get('sdplanperks')
            standexclusivedeliverytime = request.POST.get(
                'standexclusivedeliverytime')
            standexculsiveprice = request.POST.get('standexculsiveprice')
            srevisiontimes = request.POST.get('srevisiontimes')

            pre_pr_del = request.POST.get('predt')
            pre_pr = request.POST.get('preprice')
            pre_plan_perks = request.POST.get('preplanperks')
            Premexclusivedeliverytime = request.POST.get(
                'Premexclusivedeliverytime')
            Premexculsiveprice = request.POST.get('Premexculsiveprice')
            previsiontimes = request.POST.get('previsiontimes')

            infoacqprice = request.POST.get('infoacqprice')
            # print("yt", ytshoutoutprice)
            imshoutoutprice = request.POST.get('imshoutoutprice')
            # print("im", imshoutoutprice)
            greetingprice = request.POST.get('greetingprice')
            # print("greting", greetingprice)
            videochat = request.POST.get('videochat')
            # print("video", videochat)

            basic_price1 = request.POST.get('bpprice1')
            basic_del_time1 = request.POST.get('bpdt1')
            exculsiveprice1 = request.POST.get('exculsiveprice1')
            exclusivedeliverytime1 = request.POST.get('exclusivedeliverytime1')
            basic_plan_perks1 = request.POST.get('bpplanperks1')
            brevisiontimes1 = request.POST.get('brevisiontimes1')

            stand_del_time1 = request.POST.get('sddt1')
            stand_price1 = request.POST.get('sdprice1')
            stand_plan_perks1 = request.POST.get('sdplanperks1')
            standexclusivedeliverytime1 = request.POST.get(
                'standexclusivedeliverytime1')
            standexculsiveprice1 = request.POST.get('standexculsiveprice1')
            srevisiontimes1 = request.POST.get('srevisiontimes1')

            pre_pr_del1 = request.POST.get('predt1')
            pre_pr1 = request.POST.get('preprice1')
            pre_plan_perks1 = request.POST.get('preplanperks1')
            Premexclusivedeliverytime1 = request.POST.get(
                'Premexclusivedeliverytime1')
            Premexculsiveprice1 = request.POST.get('Premexculsiveprice1')
            previsiontimes1 = request.POST.get('previsiontimes1')

            basic_price2 = request.POST.get('bpprice2')
            basic_del_time2 = request.POST.get('bpdt2')
            exculsiveprice2 = request.POST.get('exculsiveprice2')
            exclusivedeliverytime2 = request.POST.get('exclusivedeliverytime2')
            basic_plan_perks2 = request.POST.get('bpplanperks2')
            brevisiontimes2 = request.POST.get('brevisiontimes2')

            stand_del_time2 = request.POST.get('sddt2')
            stand_price2 = request.POST.get('sdprice2')
            stand_plan_perks2 = request.POST.get('sdplanperks2')
            standexclusivedeliverytime2 = request.POST.get(
                'standexclusivedeliverytime2')
            standexculsiveprice2 = request.POST.get('standexculsiveprice2')
            srevisiontimes2 = request.POST.get('srevisiontimes2')
            pre_pr_del2 = request.POST.get('predt2')
            pre_pr2 = request.POST.get('preprice2')
            pre_plan_perks2 = request.POST.get('preplanperks2')
            Premexclusivedeliverytime2 = request.POST.get(
                'Premexclusivedeliverytime2')
            Premexculsiveprice2 = request.POST.get('Premexculsiveprice2')
            previsiontimes2 = request.POST.get('previsiontimes2')

            sr = Services.objects.filter(subservice='Youtube Shoutout')
            if sr.exists():
                sr = sr[0]
                if basic_price2 is not None or basic_del_time2 is not None or basic_plan_perks2 is not None or exclusivedeliverytime2 is not None or exculsiveprice2 is not None:
                    p = PricingPlans.objects.filter(
                        usersid=id, plan_type='Basic', serviceid=sr)
                    if p.exists():
                        p = p[0]
                        if basic_price2 is not None and len(basic_price2) > 0:
                            p.planprice = basic_price2
                            p.save(update_fields=['planprice'])
                            print("update basic price")
                        if basic_del_time2 is not None and len(basic_del_time2) > 0:
                            p.deliverytime = basic_del_time2
                            p.save(update_fields=['deliverytime'])
                            print("update basic delivery time")

                        if exclusivedeliverytime2 is not None and len(exclusivedeliverytime2) > 0:
                            p.exclusivedeliverytime = exclusivedeliverytime2
                            p.save(update_fields=['exclusivedeliverytime'])
                            print("update basic price")
                        if exculsiveprice2 is not None and len(exculsiveprice2) > 0:
                            p.exculsiveprice = exculsiveprice2
                            p.save(update_fields=['exculsiveprice'])
                            print("update basic exculsiveprice")

                        if brevisiontimes2 is not None and len(brevisiontimes2) > 0:
                            p.revisiontimes = brevisiontimes2
                            p.save(update_fields=['revisiontimes'])
                            print("update basic revisiontimes")

                        if basic_plan_perks2 is not None and len(basic_plan_perks2) > 0:
                            p.planperks = list(basic_plan_perks2.split(","))
                            p.save(update_fields=['planperks'])
                            print("update basic planperks")
                    else:
                        pp = PricingPlans()
                        if len(basic_price2) > 0 and len(exculsiveprice2) > 0 and len(exclusivedeliverytime2) > 0 and len(basic_del_time2) > 0 and len(basic_plan_perks2) > 0:
                            pp.usersid = id
                            pp.plan_type = 'Basic'
                            pp.planprice = basic_price2
                            pp.deliverytime = basic_del_time2
                            pp.revisiontimes = brevisiontimes2
                            pp.exculsiveprice = exculsiveprice2
                            pp.serviceid = sr
                            pp.exclusivedeliverytime = exclusivedeliverytime2
                            pp.planperks = list(basic_plan_perks2.split(","))
                            pp.save()
                            print("Insert Basic plans")

                if stand_price2 is not None or stand_del_time2 is not None or stand_plan_perks2 is not None:
                    p = PricingPlans.objects.filter(
                        usersid=id, plan_type='Standard', serviceid=sr)
                    if p.exists():
                        p = p[0]
                        if stand_price2 is not None and len(stand_price2) > 0:
                            p.planprice = stand_price2
                            p.save(update_fields=['planprice'])
                            print("update Standard price")
                        if stand_del_time2 is not None and len(stand_del_time2) > 0:
                            p.deliverytime = stand_del_time2
                            p.save(update_fields=['deliverytime'])
                            print("update Standard delivery time")

                        if standexclusivedeliverytime2 is not None and len(standexclusivedeliverytime2) > 0:
                            p.exclusivedeliverytime = standexclusivedeliverytime2
                            p.save(update_fields=['exclusivedeliverytime'])
                            print("update basic price")
                        if standexculsiveprice2 is not None and len(standexculsiveprice2) > 0:
                            p.exculsiveprice = standexculsiveprice2
                            p.save(update_fields=['exculsiveprice'])
                            print("update basic exculsiveprice")

                        if srevisiontimes2 is not None and len(srevisiontimes2) > 0:
                            p.revisiontimes = srevisiontimes2
                            p.save(update_fields=['revisiontimes'])
                            print("update basic revisiontimes")

                        if stand_plan_perks2 is not None and len(stand_plan_perks2) > 0:
                            p.planperks = list(stand_plan_perks2.split(","))
                            p.save(update_fields=['planperks'])
                            print("update Standard planperks")
                    else:
                        pp = PricingPlans()
                        if len(stand_price2) > 0 and len(standexculsiveprice2) > 0 and len(standexclusivedeliverytime2) > 0 and len(stand_del_time2) > 0 and len(stand_plan_perks2) > 0:
                            pp.usersid = id
                            pp.plan_type = 'Standard'
                            pp.planprice = stand_price2
                            pp.deliverytime = stand_del_time2
                            pp.exculsiveprice = standexculsiveprice2
                            pp.revisiontimes = srevisiontimes2
                            pp.serviceid = sr
                            pp.exclusivedeliverytime = standexclusivedeliverytime2
                            pp.planperks = list(stand_plan_perks2.split(","))
                            pp.save()
                            print("Insert Standard plans")

                if pre_pr2 is not None or pre_pr_del2 is not None or pre_plan_perks2 is not None:
                    p = PricingPlans.objects.filter(
                        usersid=id, plan_type='Premium', serviceid=sr)
                    if p.exists():
                        p = p[0]
                        if pre_pr2 is not None and len(pre_pr2) > 0:
                            p.planprice = pre_pr2
                            p.save(update_fields=['planprice'])
                            print("update Premium price")
                        if pre_pr_del2 is not None and len(pre_pr_del2) > 0:
                            p.deliverytime = pre_pr_del2
                            p.save(update_fields=['deliverytime'])
                            print("update Premium delivery time")

                        if Premexclusivedeliverytime2 is not None and len(Premexclusivedeliverytime2) > 0:
                            p.exclusivedeliverytime = Premexclusivedeliverytime2
                            p.save(update_fields=['exclusivedeliverytime'])
                            print("update basic price")
                        if Premexculsiveprice2 is not None and len(Premexculsiveprice2) > 0:
                            p.exculsiveprice = Premexculsiveprice2
                            p.save(update_fields=['exculsiveprice'])
                            print("update basic exculsiveprice")

                        if previsiontimes2 is not None and len(previsiontimes2) > 0:
                            p.revisiontimes = previsiontimes2
                            p.save(update_fields=['revisiontimes'])
                            print("update basic revisiontimes")

                        if pre_plan_perks2 is not None and len(pre_plan_perks2) > 0:
                            p.planperks = list(pre_plan_perks2.split(","))
                            p.save(update_fields=['planperks'])
                            print("update Premium planperks")
                    else:
                        pp = PricingPlans()
                        if len(pre_pr2) > 0 and len(Premexculsiveprice2) > 0 and len(Premexclusivedeliverytime2) > 0 and len(pre_pr_del2) > 0 and len(pre_plan_perks2) > 0:
                            pp.usersid = id
                            pp.plan_type = 'Premium'
                            pp.planprice = pre_pr2
                            pp.deliverytime = pre_pr_del2
                            pp.exclusivedeliverytime = Premexclusivedeliverytime2
                            pp.exculsiveprice = Premexculsiveprice2
                            pp.revisiontimes = previsiontimes2
                            pp.serviceid = sr
                            pp.planperks = list(pre_plan_perks2.split(","))
                            pp.save()
                            print("Insert Premium plans")

            sr = Services.objects.filter(subservice='Instagram Shoutout')
            if sr.exists():
                sr = sr[0]
                if basic_price1 is not None or basic_del_time1 is not None or basic_plan_perks1 is not None or exclusivedeliverytime1 is not None or exculsiveprice1 is not None:
                    p = PricingPlans.objects.filter(
                        usersid=id, plan_type='Basic', serviceid=sr)
                    if p.exists():
                        p = p[0]
                        if basic_price1 is not None and len(basic_price1) > 0:
                            p.planprice = basic_price1
                            p.save(update_fields=['planprice'])
                            print("update basic price")
                        if basic_del_time1 is not None and len(basic_del_time1) > 0:
                            p.deliverytime = basic_del_time1
                            p.save(update_fields=['deliverytime'])
                            print("update basic delivery time")

                        if exclusivedeliverytime1 is not None and len(exclusivedeliverytime1) > 0:
                            p.exclusivedeliverytime = exclusivedeliverytime1
                            p.save(update_fields=['exclusivedeliverytime'])
                            print("update basic price")
                        if exculsiveprice1 is not None and len(exculsiveprice1) > 0:
                            p.exculsiveprice = exculsiveprice1
                            p.save(update_fields=['exculsiveprice'])
                            print("update basic exculsiveprice")

                        if brevisiontimes1 is not None and len(brevisiontimes1) > 0:
                            p.revisiontimes = brevisiontimes1
                            p.save(update_fields=['revisiontimes'])
                            print("update basic revisiontimes")

                        if basic_plan_perks1 is not None and len(basic_plan_perks1) > 0:
                            p.planperks = list(basic_plan_perks1.split(","))
                            p.save(update_fields=['planperks'])
                            print("update basic planperks")
                    else:
                        pp = PricingPlans()
                        if len(basic_price1) > 0 and len(exculsiveprice1) > 0 and len(exclusivedeliverytime1) > 0 and len(basic_del_time1) > 0 and len(basic_plan_perks1) > 0:
                            pp.usersid = id
                            pp.plan_type = 'Basic'
                            pp.planprice = basic_price1
                            pp.deliverytime = basic_del_time1
                            pp.revisiontimes = brevisiontimes1
                            pp.exculsiveprice = exculsiveprice1
                            pp.serviceid = sr
                            pp.exclusivedeliverytime = exclusivedeliverytime1
                            pp.planperks = list(basic_plan_perks1.split(","))
                            pp.save()
                            print("Insert Basic plans")

                if stand_price1 is not None or stand_del_time1 is not None or stand_plan_perks1 is not None:
                    p = PricingPlans.objects.filter(
                        usersid=id, plan_type='Standard', serviceid=sr)
                    if p.exists():
                        p = p[0]
                        if stand_price1 is not None and len(stand_price1) > 0:
                            p.planprice = stand_price1
                            p.save(update_fields=['planprice'])
                            print("update Standard price")
                        if stand_del_time1 is not None and len(stand_del_time1) > 0:
                            p.deliverytime = stand_del_time1
                            p.save(update_fields=['deliverytime'])
                            print("update Standard delivery time")

                        if standexclusivedeliverytime1 is not None and len(standexclusivedeliverytime1) > 0:
                            p.exclusivedeliverytime = standexclusivedeliverytime1
                            p.save(update_fields=['exclusivedeliverytime'])
                            print("update basic price")
                        if standexculsiveprice1 is not None and len(standexculsiveprice1) > 0:
                            p.exculsiveprice = standexculsiveprice1
                            p.save(update_fields=['exculsiveprice'])
                            print("update basic exculsiveprice")

                        if srevisiontimes1 is not None and len(srevisiontimes1) > 0:
                            p.revisiontimes = srevisiontimes1
                            p.save(update_fields=['revisiontimes'])
                            print("update basic revisiontimes")

                        if stand_plan_perks1 is not None and len(stand_plan_perks1) > 0:
                            p.planperks = list(stand_plan_perks1.split(","))
                            p.save(update_fields=['planperks'])
                            print("update Standard planperks")
                    else:
                        pp = PricingPlans()
                        if len(stand_price1) > 0 and len(standexculsiveprice1) > 0 and len(standexclusivedeliverytime1) > 0 and len(stand_del_time1) > 0 and len(stand_plan_perks1) > 0:
                            pp.usersid = id
                            pp.plan_type = 'Standard'
                            pp.planprice = stand_price1
                            pp.deliverytime = stand_del_time1
                            pp.exculsiveprice = standexculsiveprice1
                            pp.revisiontimes = srevisiontimes1
                            pp.serviceid = sr
                            pp.exclusivedeliverytime = standexclusivedeliverytime1
                            pp.planperks = list(stand_plan_perks1.split(","))
                            pp.save()
                            print("Insert Standard plans")

                if pre_pr1 is not None or pre_pr_del1 is not None or pre_plan_perks2 is not None:
                    p = PricingPlans.objects.filter(
                        usersid=id, plan_type='Premium', serviceid=sr)
                    if p.exists():
                        p = p[0]
                        if pre_pr1 is not None and len(pre_pr1) > 0:
                            p.planprice = pre_pr1
                            p.save(update_fields=['planprice'])
                            print("update Premium price")
                        if pre_pr_del1 is not None and len(pre_pr_del1) > 0:
                            p.deliverytime = pre_pr_del1
                            p.save(update_fields=['deliverytime'])
                            print("update Premium delivery time")

                        if Premexclusivedeliverytime1 is not None and len(Premexclusivedeliverytime1) > 0:
                            p.exclusivedeliverytime = Premexclusivedeliverytime1
                            p.save(update_fields=['exclusivedeliverytime'])
                            print("update basic price")
                        if Premexculsiveprice1 is not None and len(Premexculsiveprice1) > 0:
                            p.exculsiveprice = Premexculsiveprice1
                            p.save(update_fields=['exculsiveprice'])
                            print("update basic exculsiveprice")

                        if previsiontimes1 is not None and len(previsiontimes1) > 0:
                            p.revisiontimes = previsiontimes1
                            p.save(update_fields=['revisiontimes'])
                            print("update basic revisiontimes")

                        if pre_plan_perks1 is not None and len(pre_plan_perks1) > 0:
                            p.planperks = list(pre_plan_perks1.split(","))
                            p.save(update_fields=['planperks'])
                            print("update Premium planperks")
                    else:
                        pp = PricingPlans()
                        if len(pre_pr1) > 0 and len(Premexculsiveprice1) > 0 and len(Premexclusivedeliverytime1) > 0 and len(pre_pr_del1) > 0 and len(pre_plan_perks1) > 0:
                            pp.usersid = id
                            pp.plan_type = 'Premium'
                            pp.planprice = pre_pr1
                            pp.deliverytime = pre_pr_del1
                            pp.exclusivedeliverytime = Premexclusivedeliverytime1
                            pp.exculsiveprice = Premexculsiveprice1
                            pp.revisiontimes = previsiontimes1
                            pp.serviceid = sr
                            pp.planperks = list(pre_plan_perks1.split(","))
                            pp.save()
                            print("Insert Premium plans")

            if infoacqprice is not None and len(infoacqprice) > 1:
                sr = Services.objects.filter(
                    subservice='Event Collaboration')
                if sr.exists():
                    sr = sr[0]
                    pr = PricingPlans.objects.filter(
                        usersid=userid, serviceid=sr)
                    if pr.exists():
                        pr = pr[0]
                        pr.planprice = infoacqprice
                        pr.save(update_fields=['planprice'])
                        print("update imshoutout")
                    else:
                        pr = PricingPlans(
                            planprice=infoacqprice, usersid=id, serviceid=sr, plan_type='Event Collaboration', exculsiveprice=0)
                        pr.save()
                        print("save imshoutout")

            if greetingprice is not None and len(greetingprice) > 1:
                sr = Services.objects.filter(subservice='Greeting Messages')
                if sr.exists():
                    sr = sr[0]
                    pr = PricingPlans.objects.filter(
                        usersid=userid, serviceid=sr)
                    if pr.exists():
                        pr = pr[0]
                        pr.planprice = greetingprice
                        pr.save(update_fields=['planprice'])
                        print("update greeting service")
                    else:
                        pr = PricingPlans(
                            planprice=greetingprice, usersid=id, serviceid=sr, plan_type='Greeting Messages', exculsiveprice=0)
                        pr.save()
                        print("save greeting service")

            if videochat is not None and len(videochat) > 1:
                sr = Services.objects.filter(subservice='Video Chat')
                if sr.exists():
                    sr = sr[0]
                    pr = PricingPlans.objects.filter(
                        usersid=userid, serviceid=sr)
                    if pr.exists():
                        pr = pr[0]
                        pr.planprice = videochat
                        pr.save(update_fields=['planprice'])
                        print("update video chat")
                    else:
                        pr = PricingPlans(planprice=videochat,
                                          usersid=id, serviceid=sr, plan_type='Video Chat', exculsiveprice=0)
                        pr.save()
                        print("save video chat")

            sr1 = Services.objects.filter(subservice='Brand Promotion')
            if sr1.exists():
                sr1 = sr1[0]

            if basic_price is not None or basic_del_time is not None or basic_plan_perks is not None or exclusivedeliverytime is not None or exculsiveprice is not None:
                p = PricingPlans.objects.filter(
                    usersid=id, plan_type='Basic', serviceid=sr1)
                if p.exists():
                    p = p[0]
                    if basic_price is not None and len(basic_price) > 0:
                        p.planprice = basic_price
                        p.save(update_fields=['planprice'])
                        print("update basic price")
                    if basic_del_time is not None and len(basic_del_time) > 0:
                        p.deliverytime = basic_del_time
                        p.save(update_fields=['deliverytime'])
                        print("update basic delivery time")

                    if exclusivedeliverytime is not None and len(exclusivedeliverytime) > 0:
                        p.exclusivedeliverytime = exclusivedeliverytime
                        p.save(update_fields=['exclusivedeliverytime'])
                        print("update basic price")
                    if exculsiveprice is not None and len(exculsiveprice) > 0:
                        p.exculsiveprice = exculsiveprice
                        p.save(update_fields=['exculsiveprice'])
                        print("update basic exculsiveprice")

                    if brevisiontimes is not None and len(brevisiontimes) > 0:
                        p.revisiontimes = brevisiontimes
                        p.save(update_fields=['revisiontimes'])
                        print("update basic revisiontimes")

                    if basic_plan_perks is not None and len(basic_plan_perks) > 0:
                        p.planperks = list(basic_plan_perks.split(","))
                        p.save(update_fields=['planperks'])
                        print("update basic planperks")
                else:
                    pp = PricingPlans()
                    if len(basic_price) > 0 and len(exculsiveprice) > 0 and len(exclusivedeliverytime) > 0 and len(basic_del_time) > 0 and len(basic_plan_perks) > 0:
                        pp.usersid = id
                        pp.plan_type = 'Basic'
                        pp.planprice = basic_price
                        pp.deliverytime = basic_del_time
                        pp.revisiontimes = brevisiontimes
                        pp.exculsiveprice = exculsiveprice
                        pp.serviceid = sr1
                        pp.exclusivedeliverytime = exclusivedeliverytime
                        pp.planperks = list(basic_plan_perks.split(","))
                        pp.save()
                        print("Insert Basic plans")

            if stand_price is not None or stand_del_time is not None or stand_plan_perks is not None:
                p = PricingPlans.objects.filter(
                    usersid=id, plan_type='Standard', serviceid=sr1)
                if p.exists():
                    p = p[0]
                    if stand_price is not None and len(stand_price) > 0:
                        p.planprice = stand_price
                        p.save(update_fields=['planprice'])
                        print("update Standard price")
                    if stand_del_time is not None and len(stand_del_time) > 0:
                        p.deliverytime = stand_del_time
                        p.save(update_fields=['deliverytime'])
                        print("update Standard delivery time")

                    if standexclusivedeliverytime is not None and len(standexclusivedeliverytime) > 0:
                        p.exclusivedeliverytime = standexclusivedeliverytime
                        p.save(update_fields=['exclusivedeliverytime'])
                        print("update basic price")
                    if standexculsiveprice is not None and len(standexculsiveprice) > 0:
                        p.exculsiveprice = standexculsiveprice
                        p.save(update_fields=['exculsiveprice'])
                        print("update basic exculsiveprice")

                    if srevisiontimes is not None and len(srevisiontimes) > 0:
                        p.revisiontimes = srevisiontimes
                        p.save(update_fields=['revisiontimes'])
                        print("update basic revisiontimes")

                    if stand_plan_perks is not None and len(stand_plan_perks) > 0:
                        p.planperks = list(stand_plan_perks.split(","))
                        p.save(update_fields=['planperks'])
                        print("update Standard planperks")
                else:
                    pp = PricingPlans()
                    if len(stand_price) > 0 and len(standexculsiveprice) > 0 and len(standexclusivedeliverytime) > 0 and len(stand_del_time) > 0 and len(stand_plan_perks) > 0:
                        pp.usersid = id
                        pp.plan_type = 'Standard'
                        pp.planprice = stand_price
                        pp.deliverytime = stand_del_time
                        pp.exculsiveprice = standexculsiveprice
                        pp.revisiontimes = srevisiontimes
                        pp.serviceid = sr1
                        pp.exclusivedeliverytime = standexclusivedeliverytime
                        pp.planperks = list(stand_plan_perks.split(","))
                        pp.save()
                        print("Insert Standard plans")

            if pre_pr is not None or pre_pr_del is not None or pre_plan_perks is not None:
                p = PricingPlans.objects.filter(
                    usersid=id, plan_type='Premium', serviceid=sr1)
                if p.exists():
                    p = p[0]
                    if pre_pr is not None and len(pre_pr) > 0:
                        p.planprice = pre_pr
                        p.save(update_fields=['planprice'])
                        print("update Premium price")
                    if pre_pr_del is not None and len(pre_pr_del) > 0:
                        p.deliverytime = pre_pr_del
                        p.save(update_fields=['deliverytime'])
                        print("update Premium delivery time")

                    if Premexclusivedeliverytime is not None and len(Premexclusivedeliverytime) > 0:
                        p.exclusivedeliverytime = Premexclusivedeliverytime
                        p.save(update_fields=['exclusivedeliverytime'])
                        print("update basic price")
                    if Premexculsiveprice is not None and len(Premexculsiveprice) > 0:
                        p.exculsiveprice = Premexculsiveprice
                        p.save(update_fields=['exculsiveprice'])
                        print("update basic exculsiveprice")

                    if previsiontimes is not None and len(previsiontimes) > 0:
                        p.revisiontimes = previsiontimes
                        p.save(update_fields=['revisiontimes'])
                        print("update basic revisiontimes")

                    if pre_plan_perks is not None and len(pre_plan_perks) > 0:
                        p.planperks = list(pre_plan_perks.split(","))
                        p.save(update_fields=['planperks'])
                        print("update Premium planperks")
                else:
                    pp = PricingPlans()
                    if len(pre_pr) > 0 and len(Premexculsiveprice) > 0 and len(Premexclusivedeliverytime) > 0 and len(pre_pr_del) > 0 and len(pre_plan_perks) > 0:
                        pp.usersid = id
                        pp.plan_type = 'Premium'
                        pp.planprice = pre_pr
                        pp.deliverytime = pre_pr_del
                        pp.exclusivedeliverytime = Premexclusivedeliverytime
                        pp.exculsiveprice = Premexculsiveprice
                        pp.revisiontimes = previsiontimes
                        pp.serviceid = sr1
                        pp.planperks = list(pre_plan_perks.split(","))
                        pp.save()
                        print("Insert Premium plans")
            # #sys.stdout.close()
            return redirect(request.META['HTTP_REFERER'])
        return render(request, "Creator/service-plan.html", {'user_timezone':user_timezone,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'vc_slots': subsslots, 'vc_price': vc_price, 'gm_price': gm_price, 'event_price': event_price, 'ent': ent, 'active': request.user.is_authenticated, 'com': com, 'tot': tot, 'totalearn': totalearn, 'user': username, 'info': ac,  'ser': ser,'ser1':ser, 'basic': debasic, 'stand': destd, 'Prem': depre, 'sertag': stt123, 'kyc': kyc, 'noti': noti, 'notcount': conoti, 'basic1': debasic1, 'stand1': destd1, 'Prem1': depre1, 'basic2': debasic2, 'stand2': destd2, 'Prem2': depre2, })
    elif permissionname == None:
        messages.warning(
                        request, "Please enter your country to access this page")
        return HttpResponseRedirect("/Settings/")
    else:
        return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def Settings(request):
    ln = Languages.objects.all()
    cate = Categories.objects.all()
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    username = Allusers.objects.get(id=userid).email
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=userid)
    ac = ac[0]


    if ac.country is None or ac.country =='':
        messages.warning(
                        request, "Please, update your profile details and country.")
    
    #sys.stdout = open("settingsusers.txt", "a")

    platids = PlatformDetails.objects.filter(
        usersid=id).values_list('platformdetailid', flat=True)
    instpltformid = Platforms.objects.get(platform_name='Instagram').platformid
    insta = PlatformDetails.objects.filter(
        usersid=id, platformtype=instpltformid)
    instauser = ''
    if insta.exists():
        instauser = insta[0].platformcredential

    ytpltformid = Platforms.objects.get(platform_name='Youtube').platformid
    yt = PlatformDetails.objects.filter(usersid=id, platformtype=ytpltformid)

    if yt.exists():
        ytuser = yt[0].platformcredential
        print('yoyutube', ytuser)
    else:
        ytuser = ''

    tkplatformid = Platforms.objects.get(platform_name='Tiktok').platformid
    tk = PlatformDetails.objects.filter(usersid=id, platformtype=tkplatformid)

    if tk.exists():
        tkuser = tk[0].platformcredential
        print('tkuser', tkuser)
    else:
        tkuser = ''

    
    userprofilelink=PlatformProfileLink.objects.filter(
        usersid=id)
    
    you = userprofilelink.filter(platformtype='Youtube')
    if you.exists():
        you = you[0].profilelink
    else:
        you = ''

    tik = userprofilelink.filter(platformtype='Tiktok')
    if tik.exists():
        tik = tik[0].profilelink
    else:
        tik = ''

    twi = userprofilelink.filter(platformtype='Twitter')
    if twi.exists():
        twi = twi[0].profilelink
    else:
        twi = ''

    fb = userprofilelink.filter(platformtype='Facebook')
    if fb.exists():
        fb = fb[0].profilelink
    else:
        fb=''

    ins = userprofilelink.filter(platformtype='Instagram')
    if ins.exists():
        ins = ins[0].profilelink
    else:
        ins = ''
    
    
    twictlink = userprofilelink.filter(platformtype='Twitch')
    if twictlink.exists():
        twictlink = twictlink[0].profilelink
    else:
        twictlink = ''
    
    linklink = userprofilelink.filter(platformtype='Linkedin')
    if linklink.exists():
        linklink = linklink[0].profilelink
    else:
        linklink = ''
    
    Snapchatlink = userprofilelink.filter(platformtype='Snapchat')
    if Snapchatlink.exists():
        Snapchatlink = Snapchatlink[0].profilelink
    else:
        Snapchatlink = ''
    
        
    
    
    
        
    

    kyc = InfluencerSettings.objects.get(influencer_userid=id).kyc
    totalearn = request.session.get('totalearn', None)
    tot = request.session.get('tot', None)
    com = request.session.get('com', None)

    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()

    exch = ExchangeRates.objects.all()

    print("categoriesid", ac.categories)

    why = Whychooseme.objects.filter(
        categoryid__in=ac.categories).order_by('whychoosemeid')
    abo = Aboutme.objects.filter(
        categoryid__in=ac.categories).order_by('aboutmeid')
    shortds = Shortdescription.objects.filter(
        categoryid__in=ac.categories).order_by('shortdescriptionid')

    gig = Rulesgig.objects.all().order_by('rulesid')

    qno = Influencerquestions.objects.filter(influencerid=userid)

    if permissionname == 'influencer_permission':
        if request.method == 'POST':
            langlist = dict(request.POST)
            fe = request.POST.get("fname")
            image = request.FILES.get("avatar")
            image1 = request.FILES.get("avatar1")
            lan = request.POST.get("language")
            
            mob = request.POST.get("phone")
            des_title = request.POST.get("tag")
            short_des = request.POST.get("short_desIntro")
            Skills = request.POST.get("Skills")
            country = request.POST.get("country")
            
            
            
        
            
            email = request.POST.get("email")
            instagram = request.POST.get("instagram")
            youtube = request.POST.get("youtube")
            tiktok = request.POST.get("tiktok")
            address = request.POST.get("address")
            aboutme = request.POST.get("aboutme")
            state = request.POST.get("state")
            city = request.POST.get("city")
            channellink = request.POST.get("channellink")

            print("data", request.POST)
            
            
            
            if "OTP" in request.POST:
                comOTP = request.POST.get("OTP")
                
                emailotp = request.session.get('emailotp', None)
                emailverify = request.session.get('emailverify', None)
                
                if comOTP == emailotp:
                    if emailverify is not None and len(emailverify) > 0  :
                        au = Allusers.objects.get(id=userid)
                        au.email = emailverify
                        au.save(update_fields=['email'])
                        
                        emaset=InfluencerSettings.objects.get(influencer_userid=userid)
                        emaset.email_verified=True
                        emaset.save()
                else:
                    messages.warning(
                        request, "OTP mismtached, please enter correct otp!...")
                
                
                
            
            
            
            
            
            
            if 'whyques' in request.POST:
                whyques = request.POST['whyques']
                whytext = request.POST['whytext']
                whytext1 = request.POST['whytext1']
                whytext2 = request.POST['whytext2']
                whytext3 = request.POST['whytext3']
                whytext4 = request.POST['whytext4']
                selectid=request.POST['whychoosemeid']
                wh = []
                wh.extend([whyques, whytext, whytext1,
                          whytext2, whytext3, whytext4])
                cho = Whychooseselected(choosetext=wh,selectid=selectid)
                cho.save()
                choid = cho.whychooseselectedid
                if choid is not None and choid > 0:
                    ac.chooseme = choid
                    ac.save(update_fields=['chooseme'])
                    print('insert whlist')
                wh.clear()
            if 'question' in request.POST:
                question = request.POST['question']
                rulesforgig1 = request.POST['rulesforgig1']
                rulesforgig2 = request.POST['rulesforgig2']
                rulesforgig3 = request.POST['rulesforgig3']
                rulesforgig4 = request.POST['rulesforgig4']
                rulesforgig5 = request.POST['rulesforgig5']
                rulesforgig6 = request.POST['rulesforgig6']
                rulesforgig7 = request.POST['rulesforgig7']
                rulesforgig8 = request.POST['rulesforgig8']
                rulesforgig9 = request.POST['rulesforgig9']
                heading = request.POST['heading']
                subheading = request.POST['subheading']
                subheading1 = request.POST['subheading1']
                ru = []
                ru.extend([question, heading, subheading, rulesforgig1, rulesforgig2,
                          rulesforgig3, rulesforgig4, rulesforgig5, subheading1, rulesforgig6, rulesforgig7, rulesforgig8, rulesforgig9])
                rle = Gigsselected(gigtext=ru)
                rle.save()
                rlid = rle.gigsselectedid
                if rlid is not None and rlid > 0:
                    ac.rulesforgig = rlid
                    ac.save(update_fields=['rulesforgig'])
                    print('insert rulesforgig')
                ru.clear()

            if 'ques1' in request.POST:
                ques1 = request.POST['ques1']
                qu = Influencerquestions.objects.filter(
                    influencerid=userid, question__icontains=ques1)
                if qu.exists():
                    pass
                else:
                    usr = InfluencerProfile.objects.get(
                        influencer_userid=userid)
                    uq = Influencerquestions(influencerid=usr, question=ques1)
                    uq.save()

            if 'rulesforgig11' in request.POST:
                rulesforgig11 = request.POST['rulesforgig11']
                selectid=request.POST['aboutmeid']
                print("text", rulesforgig11)
                abou = Aboutselected(abouttext=rulesforgig11,selectid=selectid)
                abou.save()

                aboid = abou.aboutselectedid
                if aboid is not None and aboid > 0:
                    ac.aboutme = aboid
                    ac.save(update_fields=['aboutme'])
                    print('insert aboutme')

            if 'shortdes' in request.POST:
                shortdes = request.POST['shortdes']
                selectid=request.POST['shortdesid']
                
                print("text", shortdes)
                abou = Shortdesselected(shortdestext=shortdes,selectid=selectid)
                abou.save()
                aboid = abou.shortdesselectedid
                if aboid is not None and aboid > 0:
                    ac.short_description = aboid
                    ac.save(update_fields=['short_description'])
                    print('insert short_description')

            frontlist = dict(request.POST)
            if "row-check12" in frontlist:
                categ = frontlist["row-check12"]
                ac.categories = list(categ)
                ac.save(update_fields=['categories'])

            if channellink is not None and len(channellink) > 1:
                ppl = PlatformProfileLink.objects.filter(
                    usersid=id, platformtype='Youtube')
                if ppl.exists():
                    ppl = ppl[0]
                    ppl.profilelink = channellink
                    ppl.save(update_fields=['profilelink'])
                    # print("update youtube link")
                else:
                    ppl = PlatformProfileLink(
                        platformtype='Youtube', usersid=id, profilelink=channellink)
                    ppl.save()
                    # print("Save youtube link")

            instagramlink = request.POST.get("instagramlink")
            if instagramlink is not None and len(instagramlink) > 1:
                ppl = PlatformProfileLink.objects.filter(
                    usersid=id, platformtype='Instagram')
                if ppl.exists():
                    ppl = ppl[0]
                    ppl.profilelink = instagramlink
                    ppl.save(update_fields=['profilelink'])
                    # print("update instgram link")
                else:
                    ppl = PlatformProfileLink(
                        platformtype='Instagram', usersid=id, profilelink=instagramlink)
                    ppl.save()
                    # print("Save instagram link")

            sys.stdout = open("walletpur.txt", "a")
            
            print("data",request.POST)
            
            facebooklink = request.POST.get("facebooklink")
            if facebooklink is not None and len(facebooklink) > 0:
                ppl = PlatformProfileLink.objects.filter(
                    usersid=id, platformtype='Facebook')
                if ppl.exists():
                    ppl = ppl[0]
                    ppl.profilelink = facebooklink
                    ppl.save(update_fields=['profilelink'])
                    print("update facebook link")
                else:
                    ppl = PlatformProfileLink(
                        platformtype='Facebook', usersid=id, profilelink=facebooklink)
                    ppl.save()
                    print("Save facebook link")



            Linkedinlink = request.POST.get("Linkedinlink")
            if Linkedinlink is not None and len(Linkedinlink) > 0:
                ppl = PlatformProfileLink.objects.filter(
                    usersid=id, platformtype='Linkedin')
                if ppl.exists():
                    ppl = ppl[0]
                    ppl.profilelink = Linkedinlink
                    ppl.save(update_fields=['profilelink'])
                    print("update Linkedin link")
                else:
                    ppl = PlatformProfileLink(
                        platformtype='Linkedin', usersid=id, profilelink=Linkedinlink)
                    ppl.save()
                    print("Save Linkedin link")
                    
            
            
            Twitchlink = request.POST.get("Twitchlink")
            if Twitchlink is not None and len(Twitchlink) > 0:
                ppl = PlatformProfileLink.objects.filter(
                    usersid=id, platformtype='Twitch')
                if ppl.exists():
                    ppl = ppl[0]
                    ppl.profilelink = Twitchlink
                    ppl.save(update_fields=['profilelink'])
                    print("update Twitch link")
                else:
                    ppl = PlatformProfileLink(
                        platformtype='Twitch', usersid=id, profilelink=Twitchlink)
                    ppl.save()
                    print("Save Twitch link")
                    
                    
            Snapchatlink = request.POST.get("Snapchatlink")
            if Snapchatlink is not None and len(Snapchatlink) > 0:
                ppl = PlatformProfileLink.objects.filter(
                    usersid=id, platformtype='Snapchat')
                if ppl.exists():
                    ppl = ppl[0]
                    ppl.profilelink = Snapchatlink
                    ppl.save(update_fields=['profilelink'])
                    print("update Snapchat link")
                else:
                    ppl = PlatformProfileLink(
                        platformtype='Snapchat', usersid=id, profilelink=Snapchatlink)
                    ppl.save()
                    print("Save Snapchat link")



            tiktoklink = request.POST.get("tiktoklink")
            if tiktoklink is not None and len(tiktoklink) > 1:
                ppl = PlatformProfileLink.objects.filter(
                    usersid=id, platformtype='Tiktok')
                if ppl.exists():
                    ppl = ppl[0]
                    ppl.profilelink = tiktoklink
                    ppl.save(update_fields=['profilelink'])
                    # print("update tiktok link")
                else:
                    ppl = PlatformProfileLink(
                        platformtype='Tiktok', usersid=id, profilelink=tiktoklink)
                    ppl.save()
                    # print("Save tiktok link")

            twitterlink = request.POST.get("twitterlink")
            if twitterlink is not None and len(twitterlink) > 1:
                ppl = PlatformProfileLink.objects.filter(
                    usersid=id, platformtype='Twitter')
                if ppl.exists():
                    ppl = ppl[0]
                    ppl.profilelink = twitterlink
                    ppl.save(update_fields=['profilelink'])
                    # print("update twitter link")
                else:
                    ppl = PlatformProfileLink(
                        platformtype='Twitter', usersid=id, profilelink=twitterlink)
                    ppl.save()
                    # print("Save twitter link")

            if "Language" in langlist:
                Language = langlist["Language"]
                ac.language = list(Language)
                ac.save(update_fields=['language'])
                print("update languages", Language)

                print("rahul barawal", Language)

            if instagram is not None and len(instagram) > 0:
                pltformid = Platforms.objects.get(
                    platform_name='Instagram').platformid
                pd = PlatformDetails.objects.filter(
                    usersid=id, platformtype=pltformid)
                if pd.exists():
                    pd = pd[0]
                    pd.platformcredential = instagram
                    pd.save(update_fields=['platformcredential'])
                    print("instgram username update")
                else:
                    dp = PlatformDetails()
                    dp.usersid = id
                    dp.platformtype = pltformid
                    dp.platformcredential = instagram
                    dp.additiontime = datetime.now()
                    dp.save()
                    print("insert instagram username")
          
            
            if ac:
                ac.fullname = fe
                ac.desc_title = des_title
                ac.skills = Skills
                ac.profileimage = image
                ac.mobile = mob
                
                
                ac.address = address
                ac.aboutme = aboutme
                ac.state = state
                ac.city = city
                ac.profileimage1 = image1
                if state is not None and len(state) > 0:
                    ac.save(update_fields=['state'])
                    # print("update state")

                if mob is not None and len(mob) > 0:
                    ac.save(update_fields=['mobile'])
                    # print("update mobile")
                if city is not None and len(city) > 0:
                    ac.save(update_fields=['city'])
                    # print("update city")
                if address is not None and len(address) > 0:
                    ac.save(update_fields=['address'])
                    # print("update address")
                if aboutme is not None and len(aboutme) > 0:
                    ac.save(update_fields=['aboutme'])
                    # print("update aboutme")
                if image is not None and len(image) > 0:
                    ac.save(update_fields=['profileimage'])

                    # print("update image")
                if image1 is not None and len(image1) > 0:
                    ac.save(update_fields=['profileimage1'])
                if Skills is not None and len(Skills) > 0:
                    ac.save(update_fields=['skills'])
                    # print("update skills")
                    
                
                print('currency',country)
                print('ac.country',ac.country)
                
                    
                if ac.country is None or ac.country == '':
                                            
                    if country=='India':
                        #curr = request.POST.get("currency")
                        curr='INR'
                    
                    elif country!='India' and country != '' and country is not None :
                        curr='USD'
                    else:
                        curr=None
                
                    if curr is not None and len(curr) > 0:
                        ac.currency = curr
                        ac.save(update_fields=['currency'])
                        
                        clientpayout, created = ClientPayout.objects.get_or_create(clientid=ac.influencer_userid, defaults={
                            'remaining_balance_bank':0, 'successful_withdrawal_bank':0, 'hold_bank':0,
                        
                            })
                        clientpayout.currency = curr #request.user.clientprofile.currency
                        clientpayout.save()
                        
                        
                        print("update currency")
                        
                    
                if short_des is not None and len(short_des) > 0:
                    stds = Shortdesselected.objects.get(
                        shortdesselectedid=ac.short_description)
                    stds.shortdestext = short_des
                    stds.save()
                    aboid = stds.shortdesselectedid
                    if aboid is not None and aboid > 0:
                        ac.short_description = aboid
                        ac.save(update_fields=['short_description'])
                    # print("update short_description")
                if des_title is not None and len(des_title) > 0:
                    ac.save(update_fields=['desc_title'])
                    # print("update desc_title")
                ac.country = country
                if country is not None and len(country) > 0:
                    ac.save(update_fields=['country'])
                    # print("update country")
                if fe is not None and len(fe) > 0:
                    ac.save(update_fields=['fullname'])
                    # print("update fullname")
                if platids.exists():
                    ac.platformdetails = list(platids)
                    if platids is not None and len(platids) > 0:
                        ac.save(update_fields=['platformdetails'])
                        print("paltform insert")
            # print("image", image, fe, lan,  mob,
            #       des_title, short_des, Skills, country, email)
            return redirect(request.META['HTTP_REFERER'])
        stds = Shortdesselected.objects.get(
            shortdesselectedid=ac.short_description)
        ac.short_description = stds.shortdestext
        
        atds = Aboutselected.objects.get(
            aboutselectedid=ac.aboutme)
        
        wcds = Whychooseselected.objects.get(
            whychooseselectedid=ac.chooseme)
        
        selectlangids=ac.language
        
        
        languages_dict = {lang.languageid: lang.languages for lang in Languages.objects.all()}
        ac.language = [languages_dict.get(i) for i in ac.language if languages_dict.get(i)]
        zipped_list = zip(selectlangids, ac.language)
    
        return render(request, "Creator/settings.html", {'zipped_list':zipped_list,
          'linklink':linklink, 'Snapchatlink':Snapchatlink,                    'twictlink':twictlink, 'wcds':wcds,'atds':atds,'stds':stds,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'shortds': shortds, 'qno': qno, 'abo': abo, 'gig': gig, 'why': why, 'exch': exch, 'user': username, 'info': ac, 'insta': instauser, 'yt': ytuser, 'tk': tkuser, 'kyc': kyc, 'lan': ln, 'ytlink': you, 'tiklink': tik, 'twilink': twi, 'fblink': fb, 'inslink': ins, 'totalearn': totalearn, 'tot': tot, 'com': com, 'noti': noti, 'notcount': conoti, 'active': request.user.is_authenticated, 'cate': cate, })

@login_required(login_url='/login/')
def Overview(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.select_related('influencer_userid').filter(influencer_userid=userid)
    ac = ac[0]
    
    totalearn = request.session.get('totalearn', None)
    tot = request.session.get('tot', None)
    com = request.session.get('com', None)
    pan = request.session.get('pan', None)
    can = request.session.get('can', None)
    act = request.session.get('act', None)

    kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc

    inforder = Orders.objects.select_related(
        'clientid', 'serviceid', 'influencerid', 'orderstatus').filter(influencerid=userid, paymentstatus=True).order_by('-ordersid')

    lang = ac.language
    plat = ac.platformdetails
    ac.aboutme = Aboutselected.objects.get(
        aboutselectedid=ac.aboutme).abouttext
    ac.short_description = Shortdesselected.objects.get(
        shortdesselectedid=ac.short_description).shortdestext
    whychoose = Whychooseselected.objects.get(
        whychooseselectedid=str(ac.chooseme))
    gis = Gigsselected.objects.get(gigsselectedid=str(ac.rulesforgig))

    lang1 = []
    for i in lang:
        ln = Languages.objects.filter(languageid=i)
        if ln.exists():
            ln = ln[0]
            lang1.append(str(ln.languages))

    plt = []
    if plat is None:
        plat = ''
    else:
        for j in plat:
            pt = PlatformDetails.objects.filter(platformdetailid=j)
            if pt.exists():
                pt = pt[0]
                plt.append((str(pt.platformtype), str(pt.platformcredential)))

    pro = PlatformProfileLink.objects.filter(usersid=userid)
   

    # #sys.stdout = open("pitch.txt", "a")
    array = []
    array1 = []
    array2 = []
    mon = get_monthly_orders(inforder)
    print("data", mon)

    for i in mon:
        array.append(i['total_orders'])
        array1.append(i['total_finalamt']+i['total_finalamtafterdiscount'])
        array2.append(i['month'])

    # array=[5500, 7500, 6000, 7800, 2200, 8500, 8800, 5500, 7500, 6000, 7800, 2200]
    # array1=[5500, 7500, 6000, 7800, 2200, 8500, 8800, 5500, 7500, 6000, 7800, 2200]
    # array2=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if permissionname == 'influencer_permission':

        return render(request, "Creator/overview.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'gis': gis, 'whychoose': whychoose, 'active': request.user.is_authenticated, 'monthname': array2, 'revenue': array1, 'completed_tasks': array, 'act': act, 'pan': pan, 'can': can, 'totalearn': totalearn, 'tot': tot, 'com': com, 'info': ac, 'kyc': kyc, 'order': inforder, 'plt': plt, 'lang': lang1, 'pro': pro, })
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Statements(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=userid)
    ac = ac[0]
    totalearn = request.session.get('totalearn', None)
    tot = request.session.get('tot', None)
    com = request.session.get('com', None)
    kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc
    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()

    if permissionname == 'influencer_permission':

        return render(request, "Creator/statement.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'totalearn': totalearn, 'tot': tot, 'com': com, 'info': ac, 'kyc': kyc, 'noti': noti, 'notcount': conoti, 'active': request.user.is_authenticated})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Referrals(request):
    user = request.user.id
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=userid)
    ac = ac[0]
    totalearn = request.session.get('totalearn', None)
    tot = request.session.get('tot', None)
    com = request.session.get('com', None)
    kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc
    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    if ac.currency is None:
        ac.currency = 'INR'
    
    exrate = ExchangeRates.objects.get(countery_abbrevation=ac.currency).rates
    print("rated", exrate)
    ref = UserReferral.objects.get(user=user)
    succredit = float(ref.successful_referral_count*exrate)
    print('credit', succredit)
    pencredit = ref.potential_referral_count*exrate
    try:
        clientpayout=ClientPayout.objects.get(clientid=userid)
        currency=clientpayout.currency
        if currency is None or currency =='':
            permissionname=None
                   
    except:
        permissionname=permissionname
        
        
    
    

    if permissionname == 'influencer_permission':
        clientid=Allusers.objects.get(id=request.user.id)
        clientpayout, created = ClientPayout.objects.get_or_create(clientid=clientid, defaults={'remaining_balance_bank':0, 'successful_withdrawal_bank':0, 'hold_bank':0,})
        if clientpayout.currency is None or clientpayout.currency == '':
            clientpayout.currency=request.user.influencerprofile.currency
            clientpayout.save()
        return render(request, "Creator/referral.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'pencredit': pencredit, 'succredit': succredit, 'ref': ref, 'active': request.user.is_authenticated, 'totalearn': totalearn, 'tot': tot, 'com': com, 'info': ac, 'kyc': kyc, 'noti': noti, 'notcount': conoti, })
    elif permissionname == None:
        messages.warning(
                        request, "Please enter your country to access this page")
        return HttpResponseRedirect("/Settings/")
    else:
        return HttpResponseRedirect("/")





@login_required(login_url='/login/')
def Generatecoupon(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=userid)
    ac = ac[0]
    totalearn = request.session.get('totalearn', None)
    tot = request.session.get('tot', None)
    com = request.session.get('com', None)
    kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc
    
    if ac.currency is None:
        ac.currency = 'INR'     
    
    servicename=Services.objects.all()
    if permissionname == 'influencer_permission':
        
        showcode=Couponcodes.objects.filter(influencerid=userid).order_by('-couponcodesid')
        
        if request.method=='POST':
            sys.stdout = open("ainfluencerdata.txt", "a")
            if "opcopeid" in request.POST:
                opcopeid=request.POST.get('opcopeid')
                cpstus=request.POST.get('cpstus')
                
                print('data',cpstus,type(cpstus))
                showcode1=Couponcodes.objects.get(couponcodesid=opcopeid)
                if cpstus=='True':
                    showcode1.activestatus=False
                else:
                    showcode1.activestatus=True
                showcode1.save(update_fields=['activestatus'])
                print('upadte status')            
            else:
                couponname=request.POST.get('couponname')
                codelimit=request.POST.get('codelimit')
                couponterm=request.POST.get('couponterm')
                discount=request.POST.get('discount')
                servicenam=request.POST.get('servicename')
                expiredateandtime=request.POST.get('expiredateandtime')
                
                ccode=Couponcodes.objects.filter(couponterms=couponterm)
                if ccode.exists():
                    messages.warning(
                                request, 'This couponcode is already taken, choose another one.')
                else:
                    cded=Couponcodes()
                    cded.couponname=couponname
                    cded.codeusedlimit=codelimit
                    cded.endtime=expiredateandtime
                    cded.influencerid=InfluencerSettings.objects.get(influencer_userid=str(request.user.id))
                    cded.serviceid=Services.objects.get(serviceid=servicenam)
                    cded.coupondiscount=discount
                    cded.activestatus=True
                    cded.couponterms=couponterm
                    cded.totalcodeused=0
                    cded.starttime=timezone.now()
                    cded.save()
                    

                
                    
                    
                
                
                
                
                
                
                
        
            
            
            
            
        
        return render(request, "Creator/couponcode.html", {'showcode':showcode,'servicename':servicename,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name,  'active': request.user.is_authenticated, 'totalearn': totalearn, 'tot': tot, 'com': com, 'info': ac, 'kyc': kyc,})
    else:
        return HttpResponseRedirect("/")





def check_coupon_term(request):
    coupon_term = request.GET.get('coupon_term', '')
    # Check the coupon term in your database or logic here
    ccode=Couponcodes.objects.filter(couponterms__icontains=coupon_term)
    if ccode.exists():
        response_data = {'valid': False}
    else:
        response_data = {'valid': True}
    return JsonResponse(response_data)









@login_required(login_url='/login/')
def Login_Logs(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=userid)
    ac = ac[0]
    totalearn = request.session.get('totalearn', None)
    tot = request.session.get('tot', None)
    com = request.session.get('com', None)

    lg = LoginIP.objects.filter(userid=userid).order_by('-LoginIPid')
    kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc

    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()

    if permissionname == 'influencer_permission':

        return render(request, "Creator/log.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'active': request.user.is_authenticated, 'totalearn': totalearn, 'tot': tot, 'com': com, 'info': ac, 'lg': lg, 'kyc': kyc, 'noti': noti, 'notcount': conoti, })

@login_required(login_url='/login/')
def SEO(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=userid)
    ac = ac[0]
    totalearn = request.session.get('totalearn', None)
    tot = request.session.get('tot', None)
    com = request.session.get('com', None)

    paid = Pages.objects.get(pagename='Service').pageid
    pseo = Seo_Settings.objects.filter(
        page=str(paid), influencerid=str(userid))
    kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc

    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()

    if permissionname == 'influencer_permission':
        #sys.stdout = open("pitch.txt", "a")
        if request.method == 'POST':
            title = request.POST.get("title")
            discription = request.POST.get("discription")
            keyword = request.POST.get("keyword")
            if pseo.exists():
                pseo = pseo[0]
                if title is not None and len(title) > 0:
                    pseo.title = title
                    pseo.save(update_fields=['title'])
                if discription is not None and len(discription) > 0:
                    pseo.description = discription
                    pseo.save(update_fields=['description'])
                if keyword is not None and len(keyword) > 0:
                    pseo.keyword = keyword
                    pseo.save(update_fields=['keyword'])
            else:
                paid = Pages.objects.get(pagename='Service')
                inobj = InfluencerSettings.objects.get(
                    influencer_userid=str(userid))
                obj = Seo_Settings(influencerid=inobj, title=title,
                                   description=discription, keyword=keyword, page=paid)
                obj.save()

            print("date", pseo)
            print("fsdf", title, keyword, discription)
            return redirect(request.META['HTTP_REFERER'])
        #sys.stdout.close()
        return render(request, "Creator/seo.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'active': request.user.is_authenticated, 'totalearn': totalearn, 'tot': tot, 'com': com, 'info': ac, 'infoseo': pseo, 'kyc': kyc, 'noti': noti, 'notcount': conoti, })

@login_required(login_url='/login/')
def OrderDetails(request):
    userid = request.user.id
    
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'
    
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=userid)
    ac = ac[0]
    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    #sys.stdout = open("=ptcasting.txt", "a")

    orderid = request.session.get('ODRID')
    paymentdet = Payments.objects.filter(ordersid=orderid)
    order_det = Orders.objects.filter(ordersid=orderid, paymentstatus=True)

    re = Ordercancelreasons.objects.filter(
        orderid=orderid, usersid=userid)
    ras = re
    chtme = OrderChat.objects.filter(orderid=orderid).order_by('date')

    if order_det[0].subslotid is not None:

        sabslot = Subslots.objects.get(subslotid=str(order_det[0].subslotid.subslotid))
        zoome=zoomeet.objects.get(orderid=orderid)
    else:
        sabslot = ''
        zoome= ''
        
        
    ordreq=Ordersrequirements.objects.filter(ordersid=orderid)

    qno = Orderrequirementquestions.objects.filter(orderid=orderid)

    if permissionname == 'influencer_permission':

        if request.method == 'POST':
            if "acceptorder" in request.POST:
                orid = request.POST.get("acceptorder")
                print("orderidaccept:", orid)
                acc = Orders.objects.filter(ordersid=orid, influencerid=userid)
                
                if acc.exists():
                    acc = acc[0]
                    ostid = Orderstatus.objects.filter(status='Active')
                    if ostid.exists():
                        ostid = ostid[0]
                        acc.orderstatus = ostid
                        acc.acceptancedate = timezone.now()
                        acc.save(update_fields=[
                            'orderstatus', 'acceptancedate'])
                        
                        
                        if acc.serviceid.serviceid==2:
                            link=zoomeet.objects.get(orderid=orid)
                            client_send_meet_mail(link.meet_link,acc)
                            influencer_send_meet_mail(link.meet_link,acc)
                    
                            send_customer_email(key='client/agency-orderapprovedbyinfluencer',user_email=acc.clientid.email,
                    client=acc.clientid.username,influencer=acc.influencerid.influencer_userid.username,order_id=acc.ordersid,service_type=acc.serviceid.servicename,
                order_start_date=datetime.now().strftime('%Y-%m-%d'),order_end_date=datetime.now().strftime('%Y-%m-%d'),rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None) 
                            
                            send_customer_email(key='influencer-orderapprovedbyinfluencer',user_email=acc.influencerid.influencer_userid.email,
                    client=acc.clientid.username,influencer=acc.influencerid.influencer_userid.username,order_id=acc.ordersid,service_type=acc.serviceid.servicename,
                order_start_date=datetime.now().strftime('%Y-%m-%d'),order_end_date=datetime.now().strftime('%Y-%m-%d'),rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)     
                            
                    
                        # Thread(target=lambda: existing_user(request, name=acc.clientid.username, user_type='existing_user', email_add=acc.clientid.email, template_name='order-acceptance-by-influencer.html',
                        #        subject='Exciting News! Your Order Has Been Accepted by '+acc.influencerid.fullname, order_no=acc.ordersid, influencer_name=acc.influencerid.fullname, completion_date=get_date_from_days(acc.planid.deliverytime))).start()
                        
                        else:
                        
                            send_customer_email(key='client/agency-orderapprovedbyinfluencer',user_email=acc.clientid.email,
                    client=acc.clientid.username,influencer=acc.influencerid.influencer_userid.username,order_id=acc.ordersid,service_type=acc.serviceid.servicename,
                order_start_date=datetime.now().strftime('%Y-%m-%d'),order_end_date=get_date_from_days(acc.planid.deliverytime),rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None) 
                            
                            send_customer_email(key='influencer-orderapprovedbyinfluencer',user_email=acc.influencerid.influencer_userid.email,
                    client=acc.clientid.username,influencer=acc.influencerid.influencer_userid.username,order_id=acc.ordersid,service_type=acc.serviceid.servicename,
                order_start_date=datetime.now().strftime('%Y-%m-%d'),order_end_date=get_date_from_days(acc.planid.deliverytime),rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)     
                            
                            
                        
                        send_customer_email(key='influencer-neworderchat',user_email=acc.influencerid.influencer_userid.email,
                   client=acc.clientid.username,influencer=acc.influencerid.influencer_userid.username,order_id=acc.ordersid,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None) 
                        
                        
                        send_customer_email(key='client-neworderchat',user_email=acc.clientid.email,
                   client=acc.clientid.username,influencer=acc.influencerid.influencer_userid.username,order_id=acc.ordersid,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None) 
                        
                        
                        if acc.clientid.roles=='client':
                            sendusernotification(user=acc.clientid.id,key='user-orderapproved',RM_Name=None,Influencer_Name=acc.influencerid.influencer_userid.username,Product_Name=acc.serviceid.servicename,Decline_Reason=None,Order_Id=acc.ordersid)
                        
                        if acc.clientid.roles=='agency':
                
                            sendagencynotification(user=acc.clientid.id,key='agency-orderapproved',castingcallid=None,RM_Name=None,Influencer_Name=acc.influencerid.influencer_userid.username,Product_Name=acc.serviceid.servicename,Decline_Reason=None,Order_Id=acc.ordersid)            
                        
                        
                        sendRMnotification(key='rm-influenceracceptsorder',RM_Name=None,client_type=None,client_Name=acc.clientid.username,rmid=acc.rmid,Influencer_Name=acc.influencerid.influencer_userid.username,Order_ID=acc.ordersid,reason=None,Order_Stage=None)
            
                        sendInfluencernotification(user=acc.influencerid.influencer_userid.id,key='influencer-orderaccepted',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=acc.ordersid,reason=None)
            
                        
                        print("update order status", ostid)

                
                
            

            if "reason" in request.POST:
                reason = request.POST.get("reason")
                ostid = Orderstatus.objects.get(status='Cancelled')
                ordid = Orders.objects.filter(ordersid=orderid)
                if ordid.exists():
                    ordid = ordid[0]
                    res = Ordercancelreasons(
                        orderid=ordid, reason=reason, usersid=ac)
                    res.save()
                    print("Save reaon")
                    ordid.orderstatus = ostid
                    ordid.cancelleddate = timezone.now()
                    ordid.save(update_fields=[
                                'orderstatus', 'cancelleddate'])
                    
                    clientid=ordid.clientid
                    clientpayout, created = ClientPayout.objects.get_or_create(clientid=clientid, defaults={
                        'remaining_balance_bank':0, 'successful_withdrawal_bank':0, 'hold_bank':0,
                    
                        })
                    
                    payments=Payments.objects.get(ordersid=str(ordid.ordersid))
                    
                    requested_currency =payments.ordersid.paymentcurrency
                    if requested_currency == 'INR':
                        if ordid.iscouponapplied==True:
                            clientpayout.remaining_balance_bank += ordid.finalamtafterdiscount
                            
                            newprice=ordid.finalamtafterdiscount
                            
                        else:
                            clientpayout.remaining_balance_bank += payments.amountpaid  
                            newprice=payments.amountpaid  
                        clientpayout.currency=requested_currency
                        clientpayout.save()
                        clientpayouthistory = ClientPayoutHistory(clientid=clientid, paymentid=payments,requested_currency=requested_currency,
                        wallet_transaction_amount=int(newprice),isrefund_balance=True,isrefund_hold=False,remark='Cancel Order Refund')
                        clientpayouthistory.save()
                        payments.is_refunded=True
                        payments.save()
                        
                        
                        
                        
                    # elif requested_currency == 'USD': # check for paypal payment webhook problem
                    #     clientpayout.remaining_balance_usd = pays.amountpaid
                    #     clientpayout.save()
                    print("update orderstatus with reasion save")
                    
                    
                    send_customer_email(key='client-orderdeclinebyinfluencer',user_email=ordid.clientid.email,
                   client=ordid.clientid.username,influencer=ordid.influencerid.influencer_userid.username,order_id=ordid.ordersid,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)   
                    
                    send_customer_email(key='influencer-orderdeclinebyinfluencer',user_email=ordid.influencerid.influencer_userid.email,
                   client=ordid.clientid.username,influencer=ordid.influencerid.influencer_userid.username,order_id=ordid.ordersid,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)   
                    
                    if ordid.clientid.roles=='client':
                        Thread(target=lambda:sendusernotification(user=ordid.clientid.id,key='user-purchasedecline',RM_Name=None,Influencer_Name=ordid.influencerid.influencer_userid.username,Product_Name=ordid.serviceid.servicename,Decline_Reason=reason,Order_Id=ordid.ordersid)).start()
                    
                    if ordid.clientid.roles=='agency':
                        Thread(target=lambda:sendagencynotification(user=ordid.clientid.id,key='agency-purchasedecline',castingcallid=None,RM_Name=None,Influencer_Name=ordid.influencerid.influencer_userid.username,Product_Name=ordid.serviceid.servicename,Decline_Reason=reason,Order_Id=ordid.ordersid)).start()            
                    
                    
                        
                    Thread(target=lambda:sendRMnotification(key='rm-influencerdeclinesorder',RM_Name=None,client_type=None,client_Name=ordid.clientid.username,rmid=ordid.rmid,Influencer_Name=ordid.influencerid.influencer_userid.username,Order_ID=ordid.ordersid,reason=reason,Order_Stage=None)).start()
            

            if "content" in request.POST:
                mess = request.POST.get('content')
                if mess is not None and len(mess) > 0:
                    ch = OrderChat(userid=id, text=mess, orderid=order_det[0])
                    ch.save()
                    print("Save chat")

        return render(request, "Creator/orders-details.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'zoome':zoome,'channel_name': channel_name, 'sabslot': sabslot, 'qno': qno, 'pymethod': paymentdet, 're': ras, 'chtme': chtme, 'order': order_det, 'info': ac,  'noti': noti, 'notcount': conoti,'ordreq':ordreq })
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Pitching_List(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    ac = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=userid)
    ac = ac[0]
    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    if permissionname == 'influencer_permission':
        phdet = PitchingCastingCall.objects.filter(influencerid=userid)
        val = phdet.values('pitchingCastingCallid', 'castingcallid__creationdate', 'castingcallid__brandname',
                           'castingcallid__posttitle', 'approved', 'date', 'castingcallid__postdescription')
        phdet_json = json.dumps(list(val), default=str)
        return render(request, "Creator/pitchinglist.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'phdet_json': phdet_json, 'info': ac,  'noti': noti, 'notcount': conoti, 'phdet': phdet})
    return HttpResponseRedirect("/")





@login_required(login_url='/login/')
def Brandpitch(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    id = Allusers.objects.filter(id=userid)
    id = id[0]
    ins = InfluencerSettings.objects.filter(influencer_userid=id)
    noti = Notifications.objects.filter(
        touserid=userid).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    if ins.exists():
        ins = ins[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    callid = request.session.get('callid', None)
    calid = Casting_Call.objects.filter(castingcallid=callid)
    if calid.exists():
        calid = calid[0]
        clientid = calid.clientid
        id1 = Allusers.objects.filter(id=str(clientid))
        id1 = id1[0]
    if permissionname == 'influencer_permission':
        sys.stdout = open("pitch.txt", "a")
        if request.method == 'POST':
            
            file = request.FILES.get("file-upload-input")
            pitchtext = request.POST.get("pitchtext")

            print("file", file)
            print("Text", pitchtext)
            print("callid", calid)
            try:
                
                if file is not None or pitchtext:
                    print('file',file)
                    
                    print('pitxh',pitchtext)
                    pt = PitchingCastingCall(
                        castingcallid=calid, influencerid=ins, pitchtext=pitchtext, pitchingfile=file)
                    pt.save()
                    
                    Thread(target=lambda:sendagencynotification(user=calid.clientid.id,key='agency-newpitchalert',castingcallid=calid,RM_Name=None,Influencer_Name=request.user.username,Product_Name=None,Decline_Reason=None,Order_Id=None)).start()            
                    sendInfluencernotification(user=request.user.id,key='influencer-castingcallpitched',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=calid,reason=None)
                    
                    send_customer_email(key='influencer-pitchsubmitted',user_email=request.user.email,
                        client=request.user.username,influencer=None,order_id=None,service_type=None,
                    order_start_date=None,order_end_date=None,rm=None,casting_call_id=callid,brief_pitch=None,decline_reson=None) 
                    
                    send_customer_email(key='agency-newpitchrecived',user_email=calid.clientid.email,
                        client=calid.clientid.username,influencer=None,order_id=None,service_type=None,
                    order_start_date=None,order_end_date=None,rm=None,casting_call_id=callid,brief_pitch=None,decline_reson=None) 
                    print('send mail')
                    
                    messages.success(
                                request, 'Your response is successfully submitted. After approval, you will be notified.')
                    
        
                else:
                    messages.warning(
                                request, 'Your response is not submitted. Please, try again with new data.')

            
            except:
                messages.warning(
                            request, 'Your response is not submitted. Please, try again after some time.')

            
                     
                
                
            return redirect(request.META['HTTP_REFERER'])

        #sys.stdout.close()
        return render(request, "Creator/brandpitch.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'noti': noti, 'notcount': conoti, })
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Blogs_Home_Creator(request, cate=None):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    username = request.user.email
    ac = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    ac = ac[0]
    kyc = InfluencerSettings.objects.get(influencer_userid=request.user.id).kyc

    blog = Blog.objects.all()
    if cate is not None:
        blog = Blog.objects.filter(blog_categories__icontains=cate)

    return render(request, "Creator/bloghome.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'info': ac, 'user': username, 'kyc': kyc, "allblog": blog})

@login_required(login_url='/login/')
def Blogs_Post_Creator(request, name):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    username = request.user.email
    ac = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    ac = ac[0]
    kyc = InfluencerSettings.objects.get(influencer_userid=request.user.id).kyc

    # name = name.replace('-', ' ')
    print(name)
    base_url = "{0}://{1}{2}".format(request.scheme,
                                     request.get_host(), request.path)
    print("Url", base_url)

    blog = Blog.objects.all()
    bcate = BlogCategory.objects.all()
    blog1 = blog.order_by('-date').values()[0:5]
    bldet = Blog.objects.filter(url_structure__icontains=name)[0]
    content = Blogcontent.objects.filter(
        blog=str(bldet.blogid)).order_by('blogcontentid')
    if content.exists():
        content = content
    else:
        content = ''
    bl = BlogComments.objects.filter(blog=bldet, isapproved=True)
    num = len(bl)

    return render(request, "Creator/blogdetails.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'info': ac, 'user': username, 'kyc': kyc, 'content': content, 'det': bldet, "blogdeatils": blog, 'comm': bl, 'rc': blog1, 'num': num, 'cate': bcate, 'link': base_url})


logger = logging.getLogger()
fh = logging.FileHandler('creator_view_log.txt')
logger.addHandler(fh)

@login_required(login_url='/login/')
def Add_webstories(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname = 'None'
        image = 'None'

    username = request.user.email
    ac = InfluencerProfile.objects.filter(influencer_userid=request.user.id)
    ac = ac[0]
    kyc = InfluencerSettings.objects.get(influencer_userid=request.user.id).kyc
    
    stories=Webstory.objects.filter(userid=userid,isapproved=True).order_by('-webstoryid')
    
    if request.method=='POST':

        title = request.POST.getlist("image_title")  # Assuming these fields might have multiple values
        caption = request.POST.getlist("image_caption")
        photos = request.FILES.getlist("photo")
        thumbfile = request.FILES.get("avatar")
        thumbtext = request.POST.get("thumb_title")

        
        print('details',title,caption,request.POST)
        # Check if required fields are not blank before proceeding
        if not thumbfile or not thumbtext or not title or not caption or not photos:
            messages.warning(request, 'Please fill in all the required fields.')
        else:
            avaiwest = Webstory.objects.filter(thumnailtitle=str(thumbtext))
            if avaiwest.exists():
                messages.warning(request, 'The webstory title is already available, choose another one.')
            else:
                webstor = Webstory()
                webstor.userid = Allusers.objects.get(id=str(userid))
                webstor.thumbnail = thumbfile
                webstor.thumnailtitle = thumbtext
                webstor.title = title
                webstor.caption = caption
                webstor.save()

                # Save each associated photo in the Webstoryfiles model
                strid = []
                for photo_file in photos:
                    storyid = Webstoryfiles.objects.create(webstoryfiles=photo_file)
                    strid.append(int(storyid.webstoryfilesid))
                websto = Webstory.objects.get(webstoryid=webstor.webstoryid)
                if len(strid) > 0:
                    websto.filesid = strid
                websto.save()
                
                
                
                
                kycuserid=Allusers.objects.filter(roles='kyc')
                
                
                Thread(target=lambda:sendInfluencernotification(user=request.user.id,key='influencer-webstory',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None)).start()
                
                
                
                for i in kycuserid:
                    print("user",i.id)
                    Thread(target=lambda:sendkycmanagernotification(user=i.id,key='kyc-webstoryverification',influencer_user_name=request.user.username,client_name=None)).start()
                    print('execute')
                
                send_customer_email(key='influencer-webstoryadded',user_email=request.user.email,
                   client=None,influencer=request.user.username,order_id=None,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)
                
                print('Webstory saved successfully')
            
            
                
                
                messages.success(
                            request, 'Your webstory is submitted. After approval, it shows on our platform.')            
        
    return render(request, "Creator/add-webstory.html",{'stories':stories,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name': channel_name, 'info': ac, 'user': username, 'kyc': kyc})

@csrf_exempt
def Webhook1(request):
    data = json.loads(request.body)
    # print(data)
    with open('webhook.txt', 'w') as f:
        f.write(str(data))




def generate_random_otp(length=6):
    """Generate a random OTP of the specified length."""
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def check_email(request):
    if request.method == 'POST':
        email = request.POST.get('address', None)
        if email is not None:
            try:
                user = Allusers.objects.get(email__icontains=email)
                return JsonResponse({'exists': True})
            except Allusers.DoesNotExist:
                
                otp = generate_random_otp()
                
                
                send_customer_email(key='user-sendmailotp',user_email=email,client=request.user.username,influencer=None,order_id=None,service_type=None,order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None,pward=None,otp=otp)
                
                request.session['emailotp'] = otp
                request.session['emailverify'] = email
                
                return JsonResponse({'exists': False})
    return JsonResponse({'error': 'Invalid request'})