from mainapp.enanddc import encrypt, decrypt
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from mainapp.models import *
from Admin.models import *
from Creator.models import *
from .models import *
from django.conf import settings
from django.db.models import Sum
# Create your views here.
import sys, json, os, uuid
from mainapp.models import Rmprofile, Accountprofile
from django.shortcuts import render, HttpResponseRedirect
from mainapp.models import *
from Admin.models import *
from RM.models import *
from agora_chat.models import *
from Creator.models import *
from Client.models import *
import sys
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required(login_url='/login/')
def advertiser_offer(request):
    sys.stdout = open("offerpost.txt", "a")
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'agency_permission':
        
        print(request.method, permissionname)
        user = request.user
        userid = request.user.id
        try:
            channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
            unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
            if unread_messages > 0:
                unread_status = True
            else:
                unread_status = False
            rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
        
            rmname = rmid.rmid.rmprofile.name
            image = rmid.rmid.rmprofile.profilepic
        except:
            channel_name = 'None'
            unread_status = False
            image='none'
            rmname='None'
        print(request.GET.get('source'))

        agencysettinginstance = AgencySettings.objects.get(asettingsuserid=request.user.id) #request.user.id

        if request.method=='POST':
            sys.stdout = open("offerpost.txt", "a")
            
            datapost = request.POST#.decode('utf-8')  # Decode the bytes to a string
            print('datapost:',datapost)
            data=dict(datapost)
            print('newdata:', data)
            avatar_file = request.FILES.get('avatar')
            
            # agencysettinginstance = AgencySettings.objects.get(asettingsuserid=request.user.id) #request.user.id

            if 'deleteflagofferid' in request.POST:
                
                deleteflagofferid=request.POST.get('deleteflagofferid')
                advertiseroffer = AdvertiserOffer.objects.get(offerid=deleteflagofferid)
                advertiseroffer.isremoved= True
                advertiseroffer.save()
                print('delete execute')

            elif request.POST.get('addnew') and avatar_file :
                
                print('imagefile',avatar_file)
                # Generate a unique filename using uuid
                unique_filename = str(uuid.uuid4()) + os.path.splitext(avatar_file.name)[1]
                # Define the desired directory to save the file
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'affiliatemedia')
                # Create the directory if it doesn't exist
                os.makedirs(upload_dir, exist_ok=True)
                # Create the file path
                file_path = os.path.join(upload_dir, unique_filename)
                    
                # Save the file to the desired directory
                with open(file_path, 'wb') as destination:
                    for chunk in avatar_file.chunks():
                        destination.write(chunk)

                file_path_for_html = '/media/affiliatemedia/'+unique_filename
            
                # agencysettinginstance = AgencySettings.objects.get(asettingsuserid=request.user.id) #request.user.id
                
                addnewoffer = AdvertiserOffer(userid=agencysettinginstance, name=data['name'][0],
                server_ip=data['serverip'][0],location=data['geo'][0],category=data['category'][0],
                model=data['model'][0],productlink=data['productlink'][0],price=data['price'][0],
                payout=data['payout'][0], rmid=rmid, image=file_path_for_html)
                addnewoffer.save()

                # offeridinstance = AdvertiserOffer.objects.get(offerid = addnewoffer.pk)
                #create/initialise wallet for the specific offerid
                platformpayout=PlatformPayout(offerid=addnewoffer.pk, userid=agencysettinginstance)
                platformpayout.save()

            elif request.POST.get('addnew') and not avatar_file:
                
                # agencysettinginstance = AgencySettings.objects.get(asettingsuserid=request.user.id) #request.user.id
                
                addnewoffer = AdvertiserOffer(userid=agencysettinginstance, name=data['name'][0],
                server_ip=data['serverip'][0],location=data['geo'][0],category=data['category'][0],
                model=data['model'][0],productlink=data['productlink'][0],price=data['price'][0],
                payout=data['payout'][0], rmid=rmid)
                addnewoffer.save()
                print('addnewoffer.pk :', addnewoffer.pk )
                # print('addnewoffer.id :',addnewoffer.id)
                # offeridinstance = AdvertiserOffer.objects.get(offerid = addnewoffer.pk)
                #create/initialise wallet for the specific offerid
                platformpayout=PlatformPayout(offerid=addnewoffer.pk, userid=agencysettinginstance)
                platformpayout.save()
        
        advertiseroffers = AdvertiserOffer.objects.filter(userid=agencysettinginstance, isremoved=False) #filter by usersid=request.user
        return render(request, "advertiser/advertiser_offer.html",{'result':advertiseroffers,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def advertiser_instruction(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'agency_permission':
        user = request.user
        userid = request.user.id
        try:
            channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
            unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
            if unread_messages > 0:
                unread_status = True
            else:
                unread_status = False
            rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
        
            rmname = rmid.rmid.rmprofile.name
            image = rmid.rmid.rmprofile.profilepic
        except:
            channel_name = 'None'
            unread_status = False
            image='none'
            rmname='None'
        return render(request, "advertiser/instruction.html",{'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,})
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def advertiser_withdrawal_request(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'agency_permission':
        user = request.user
        userid = request.user.id
        try:
            channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
            unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
            if unread_messages > 0:
                unread_status = True
            else:
                unread_status = False
            rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
        
            rmname = rmid.rmid.rmprofile.name
            image = rmid.rmid.rmprofile.profilepic
        except:
            channel_name = 'None'
            unread_status = False
            image='none'
            rmname='None'
        
        if 'approveflag_platform_payout_request_id' in request.POST:
            sys.stdout = open("offerpost.txt", "a")
            print('full2',request.POST)
            approveflag_platform_payout_request_id = request.POST.get('approveflag_platform_payout_request_id')
            transaction_amount=float(request.POST.get('transaction_amount'))
            transaction_screenshot = request.FILES.get('transaction_screenshot')
            unique_filename = str(uuid.uuid4()) + os.path.splitext(transaction_screenshot.name)[1]
                # Define the desired directory to save the file
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'affiliatemedia')
            # Create the directory if it doesn't exist
            os.makedirs(upload_dir, exist_ok=True)
            # Create the file path
            file_path = os.path.join(upload_dir, unique_filename)
                
            # Save the file to the desired directory
            with open(file_path, 'wb') as destination:
                for chunk in transaction_screenshot.chunks():
                    destination.write(chunk)

            file_path_for_html = '/media/affiliatemedia/'+unique_filename

            platformpayoutrequest = PlatformPayoutRequest.objects.get(id=approveflag_platform_payout_request_id)
            platformpayoutrequest.transaction_amount = transaction_amount
            platformpayoutrequest.transaction_screenshot = file_path_for_html
            platformpayoutrequest.advertiser_action = True
            platformpayoutrequest.save()

            platformpayout =PlatformPayout.objects.get(offerid=platformpayoutrequest.for_offer_id)
            print('hold_bank:',platformpayout.hold_bank)
            platformpayout.hold_bank-= transaction_amount
            platformpayout.successful_withdrawal_bank+= transaction_amount
            platformpayout.save()
        
        advertiseridobj = Allusers.objects.get(id=request.user.id)
        platformpayoutrequest = PlatformPayoutRequest.objects.filter(advertiserid=advertiseridobj, isremoved=False)
        return render(request, "advertiser/withdrawal_request.html",{'platformpayoutrequest':platformpayoutrequest,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,})
    return HttpResponseRedirect('/')
#############################################################################

@login_required(login_url='/login/')
def rm_advertiser_approval(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        sys.stdout = open("offerpost.txt", "a")
        print(1111111111111)
        if request.method == 'POST':
            if 'approveflagofferid' in request.POST:
                print('full:', request.POST)
                approveflagofferid=request.POST.get('approveflagofferid')
                platform_margin = float(request.POST.get('platform_margin'))
                print('approveflagofferid1',approveflagofferid)
                alloffers = AdvertiserOffer.objects.all()
                print(22,alloffers)
                advertiseroffer = AdvertiserOffer.objects.get(offerid=approveflagofferid)
                affiliate_payout = advertiseroffer.payout - ((platform_margin/100)*advertiseroffer.payout)

                
                advertiseroffer.platform_margin = platform_margin
                advertiseroffer.affiliate_payout = affiliate_payout
                advertiseroffer.isapproved = True
                advertiseroffer.save()
                print('offer approved is now True')

            if 'isapproved' in request.POST:
                hiddenisapproved=request.POST.get('isapproved')
                
                print('hiddenisapproved:',hiddenisapproved)

        alloffers = AdvertiserOffer.objects.all()#filter(userid=request.user.id)
        context = {'result':alloffers, 'min_margin_limit':1,'max_margin_limit':50}
        return render(request, "rm/rm_advertiser_approval.html", context=context)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def rm_affiliate_payout_request(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        sys.stdout = open("offerpost.txt", "a")
        print('testttt0')
        if 'approveflag_affiliate_payout_request_id' in request.POST:
            sys.stdout = open("offerpost.txt", "a")
            approveflag_affiliate_payout_request_id=request.POST.get('approveflag_affiliate_payout_request_id')
            affiliateid= request.POST.get('hidden_affiliateid')
            print('full',request.POST)
            print('testttt',approveflag_affiliate_payout_request_id,affiliateid)
            affiliateidobj = Allusers.objects.get(id = affiliateid)
            affiliatepayoutrequest = AffiliatePayoutRequest.objects.get(affiliateid=affiliateidobj, id=approveflag_affiliate_payout_request_id)
            affiliatepayoutrequest.rm_action = True
            affiliatepayoutrequest.save()

            # if affiliatepayoutrequest.requested_method == 'Bank Withdrawal':
            #     affiliatepayout =AffiliatePayout.objects.get(affiliateid=affiliateidobj)
            #     print('hold_bank:',affiliatepayout.hold_bank)
            #     affiliatepayout.hold_bank+= affiliatepayoutrequest.requested_amount
            #     affiliatepayout.save()
            
        affiliatepayoutrequest = AffiliatePayoutRequest.objects.filter(assigned_rm=request.user).order_by('-id')
        context = {'result':affiliatepayoutrequest}
        return render(request, "rm/rm_affiliate_payout_request.html", context=context)
    return HttpResponseRedirect('/')
###########################################################################

@login_required(login_url='/login/')
def account_affiliate_payout_request(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission':
        sys.stdout = open("offerpost.txt", "a")
        print('testttt0')
        if 'approveflag_affiliate_payout_request_id' in request.POST:
            sys.stdout = open("offerpost.txt", "a")
            approveflag_affiliate_payout_request_id=request.POST.get('approveflag_affiliate_payout_request_id')
            affiliateid= request.POST.get('hidden_affiliateid')
            transaction_amount=float(request.POST.get('transaction_amount'))
            transaction_screenshot = request.FILES.get('transaction_screenshot')
            unique_filename = str(uuid.uuid4()) + os.path.splitext(transaction_screenshot.name)[1]
                # Define the desired directory to save the file
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'affiliatemedia')
            # Create the directory if it doesn't exist
            os.makedirs(upload_dir, exist_ok=True)
            # Create the file path
            file_path = os.path.join(upload_dir, unique_filename)
                
            # Save the file to the desired directory
            with open(file_path, 'wb') as destination:
                for chunk in transaction_screenshot.chunks():
                    destination.write(chunk)

            file_path_for_html = '/media/affiliatemedia/'+unique_filename
            print('full',request.POST, request.FILES)
            print('testttt',approveflag_affiliate_payout_request_id,affiliateid)
            
            affiliateidobj = Allusers.objects.get(id = affiliateid)
            affiliatepayoutrequest = AffiliatePayoutRequest.objects.get(affiliateid=affiliateidobj, id=approveflag_affiliate_payout_request_id, rm_action=True)
                
            if affiliatepayoutrequest.requested_method == 'Bank Withdrawal':
                affiliatepayout =AffiliatePayout.objects.get(affiliateid=affiliateidobj)
                print('hold_bank:',affiliatepayout.hold_bank)
                affiliatepayout.hold_bank-= transaction_amount
                affiliatepayout.successful_withdrawal_bank+= transaction_amount
                affiliatepayout.save()

                affiliatepayoutrequest.transaction_amount+= transaction_amount
                affiliatepayoutrequest.transaction_screenshot = file_path_for_html
                affiliatepayoutrequest.account_action = True
                affiliatepayoutrequest.save()

        affiliatepayoutrequest = AffiliatePayoutRequest.objects.filter(assigned_account=request.user, rm_action=True).order_by('-id')
        context = {'result':affiliatepayoutrequest}
        return render(request, "account/account_affiliate_payout_request.html", context=context)
    return HttpResponseRedirect('/')
############################################################################

@login_required(login_url='/login/')
def manager_affiliate_payout_request(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'manager_permission':
        sys.stdout = open("offerpost.txt", "a")
        if request.method == 'POST':
            if 'assignroleflag_affiliate_payout_request_id' in request.POST:
                print('full:',request.POST)
                assign_rm = request.POST.get('assign_rm')
                assign_account = int(request.POST.get('assign_account'))
                hidden_affiliateid=int(request.POST.get('hidden_affiliateid'))
                assignroleflag_affiliate_payout_request_id= request.POST.get('assignroleflag_affiliate_payout_request_id')
                affiliateidobj = Allusers.objects.get(id=hidden_affiliateid).id
                affiliatepayoutrequest = AffiliatePayoutRequest.objects.get(affiliateid=affiliateidobj, id=assignroleflag_affiliate_payout_request_id)
                
                assign_rmobj = Allusers.objects.get(id=assign_rm)
                affiliatepayoutrequest.assigned_rm = assign_rmobj

                assign_accountobj = Allusers.objects.get(id=assign_account)
                affiliatepayoutrequest.assigned_account = assign_accountobj
                affiliatepayoutrequest.save()

        affiliatepayoutrequest = AffiliatePayoutRequest.objects.all().order_by('-id')
        rmprofile=Rmprofile.objects.all()
        accountprofile=Accountprofile.objects.all()
        print('rmprofile:',rmprofile,'accountprofile:',accountprofile)
        context = {'affiliatepayoutrequest':affiliatepayoutrequest, 'rmprofile':rmprofile, 'accountprofile':accountprofile}
        return render(request, "manager/manager_affiliate_payout_request.html", context=context)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def platform_request_advertiser_payout(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        sys.stdout = open("offerpost.txt", "a")

        if request.method == 'POST':
            if 'request_balance_flag' in request.POST:
                print('full:',request.POST)
                offerid = request.POST.get('request_balance_flag')
                remaining_balance = float(request.POST.get('hidden_remaining_balance'))
                requested_amount = float(request.POST.get('requested_amount'))
                request_from_rm = request.POST.get('hidden_request_from_rm')
                print('offerid:, requested_amount:', offerid,requested_amount,type(offerid),type(requested_amount))
                

                advertiseroffer= AdvertiserOffer.objects.get(offerid=offerid)
                advertiseridobj=advertiseroffer.userid.asettingsuserid
                productname=advertiseroffer.name

                platformpayout=PlatformPayout.objects.get(offerid=offerid)
                platformpayout.hold_bank+= requested_amount
                platformpayout.save()
                assigned_rm = Allusers.objects.get(id=request_from_rm)
                platformpayoutrequest=PlatformPayoutRequest(assigned_rm =assigned_rm ,advertiserid=advertiseridobj,for_offer_id=offerid, productname=productname, requested_amount=requested_amount,remaining_balance_on_dateofrequest=remaining_balance)
                platformpayoutrequest.save()

            if request.method == 'POST':
                if 'removeflag_requestid' in request.POST:
                    removeflag_requestid = request.POST.get('removeflag_requestid')
                    offerid = request.POST.get('hidden_for_offer_id')
                    requested_amount = float(request.POST.get('hidden_requested_amount'))
                    print('3postvals',removeflag_requestid,offerid,requested_amount,type(offerid), type(requested_amount))
                    
                    platformpayoutrequest=PlatformPayoutRequest.objects.get(id=removeflag_requestid)
                    platformpayoutrequest.isremoved=True
                    platformpayoutrequest.save()

                    platformpayout=PlatformPayout.objects.get(offerid=offerid)
                    platformpayout.hold_bank-= requested_amount
                    platformpayout.save()
        #this is working too
        all_offer_wallet_details = []
        affiliate_offers = AffiliateWebhook.objects.values('utm_affiliate_id', 'utm_offerid').annotate(total_payout=Sum('payout'))
        print('affiliate_offers:',affiliate_offers)
        for entry in affiliate_offers:
            print('entry',entry)
            offerid = entry['utm_offerid']
            try:
                advertiseroffer= AdvertiserOffer.objects.get(offerid=offerid)
                advertisername = advertiseroffer.userid.asettingsuserid.username
                productname = advertiseroffer.name
                assigned_rm = advertiseroffer.rmid.rmid
                payout = advertiseroffer.payout
            except:
                continue
            # print('offerid,advertiserid,productname',offerid, advertiserid, productname)
            platform_payout = PlatformPayout.objects.get(offerid=offerid)
            print('platform_payout:',platform_payout)

            if platform_payout:
                
                entry['successful_withdrawal_bank'] = platform_payout.successful_withdrawal_bank
                entry['hold_bank'] = platform_payout.hold_bank
                entry['remaining_balance'] = entry['total_payout']-(platform_payout.successful_withdrawal_bank+platform_payout.hold_bank)
                entry['advertisername'] = advertisername
                entry['payout'] = payout
                entry['productname'] = productname
                entry['assigned_rm'] = assigned_rm

            else:
                entry['successful_withdrawal_bank'] = 0  # Default value if no match found
                entry['hold_bank'] = 0  # Default value if no match found
                entry['assigned_rm'] = assigned_rm
            all_offer_wallet_details.append(entry)

            #this is working too
    #     platform_payout_subquery = PlatformPayout.objects.filter(
    #     offerid=OuterRef('offerid')
    #     ).values('successful_withdrawal_bank', 'hold_bank')[:1]

    #     # print('platform_payout_subquery:',platform_payout_subquery)

    #     all_offer_wallet_details = AffiliateWebhook.objects.values('utm_affiliate_id', 'utm_offerid').annotate(
    #     total_payout=Sum('payout'),
    #     successful_withdrawal_bank=Subquery(platform_payout_subquery.values('successful_withdrawal_bank')),
    #     hold_bank=Subquery(platform_payout_subquery.valu  es('hold_bank'))
    # )
        print('all_offer_wallet_details : ',all_offer_wallet_details)
        print("+++++++++++++++++++++++++++++++++++")

        # PlatformPayout=PlatformPayout
        platformpayoutrequest = PlatformPayoutRequest.objects.filter(isremoved=False)
        rmprofile=Rmprofile.objects.all()
        accountprofile=Accountprofile.objects.all()
        # print('rmprofile:',rmprofile,'accountprofile:',accountprofile)
        context = {'all_offer_wallet_details':all_offer_wallet_details, 'platformpayoutrequest':platformpayoutrequest, 'rmprofile':rmprofile, 'accountprofile':accountprofile}
        return render(request, "rm/rm_request_advertiser_payout.html", context=context)

def platform_request_advertiser_payout_history(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        if request.method == 'POST':
            if 'removeflag_requestid' in request.POST:
                removeflag_requestid = request.POST.get('removeflag_requestid')
                offerid = request.POST.get('hidden_for_offer_id')
                requested_amount = float(request.POST.get('hidden_requested_amount'))
                print('3postvals',removeflag_requestid,offerid,requested_amount,type(offerid), type(requested_amount))
                
                platformpayoutrequest=PlatformPayoutRequest.objects.get(id=removeflag_requestid)
                if platformpayoutrequest.advertiser_action == False:#advertiser hasn't sent money till now
                    platformpayoutrequest.isremoved=True
                    platformpayoutrequest.save()

                    platformpayout=PlatformPayout.objects.get(offerid=offerid)
                    platformpayout.hold_bank-= requested_amount
                    platformpayout.save()

        platformpayoutrequest = PlatformPayoutRequest.objects.filter(isremoved=False)
        return render(request, "rm/rm_request_advertiser_payout_history.html", context={'platformpayoutrequest':platformpayoutrequest})
    return HttpResponseRedirect('/')
###########################################################################

@login_required(login_url='/login/')
def affiliate_payout(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'client_permission' or permissionname == 'influencer_permission':
        sys.stdout = open("offerpost.txt", "a")
        
        
        userid = request.user.id
        rmid=None
        try:
            channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
            unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
            print('dfdsf',unread_messages)
            if unread_messages > 0:
                unread_status = True
            else:
                unread_status = False
            
            if request.user.roles=='client'    :
                rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
                rmname = rmid.rmid.rmprofile.name
                image = rmid.rmid.rmprofile.profilepic
            if request.user.roles=='influencer'    :
                rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
                rmname = rmid.rmid.rmprofile.name
                image = rmid.rmid.rmprofile.profilepic
            
            print('rmid',rmid)
        except:
            channel_name = 'None'
            unread_status = False
            image='none'
            rmname='None'
        
        print('payouts1')
        payouts = AffiliateWebhook.objects.filter(utm_affiliate_id=request.user.id, status=True).values_list("affiliate_payout")
        total_payout = 0.0
        total_payout_usd = 0.0
        for tuple_value in payouts:
            if tuple_value[0] is not None:
                total_payout += tuple_value[0]
        print('payouts:',total_payout)
        affiliateobj=Allusers.objects.get(id=request.user.id)
        print(333,affiliateobj)
        # affiliatepayout = AffiliatePayout.objects.get(affiliateid=affiliateobj)

        affiliatepayout, created = AffiliatePayout.objects.get_or_create(affiliateid=affiliateobj, defaults={
        'remaining_balance_bank':0, 'successful_withdrawal_bank':0, 'hold_bank':0,
        'remaining_balance_usdt':0, 'successful_withdrawal_usdt':0, 'hold_usdt':0,
        'remaining_balance_btc':0, 'successful_withdrawal_btc':0, 'hold_btc':0
        })

        # successful_withdrawal_bank= affiliatepayout.successful_withdrawal_bank
        # hold_bank= affiliatepayout.hold_bank
        # remaining_balance_bank= total_payout-(successful_withdrawal_bank+hold_bank)
        # context={'total_bank':total_payout, 
        #          'successful_withdrawal_bank':successful_withdrawal_bank, 
        #          'hold_bank':hold_bank,
        #          'remaining_balance_bank':remaining_balance_bank
        #          }
        role=request.user.roles
        if role=='client' and request.user.clientprofile.country=='India':
            requested_currency='INR'
            min_rerquest_limit=500
        elif role=='agency' and request.user.agencyprofile.country=='India':
            requested_currency='INR'
            min_rerquest_limit=500
        elif role=='influencer' and request.user.influencerprofile.country=='India':
            requested_currency='INR'
            min_rerquest_limit=500
        else:
            requested_currency='USD'
            min_rerquest_limit=5

        if request.method == 'POST' and 'payout_request' in request.POST:
            print('payout_request request.POST', request.POST)
            print(request.POST.get('payout_request'))

            if request.POST.get('method') == 'Bank Withdrawal':
                requested_amount= float(request.POST.get('requested_amount'))
                successful_withdrawal_bank= affiliatepayout.successful_withdrawal_bank
                hold_bank= affiliatepayout.hold_bank
                remaining_balance_bank= total_payout-(successful_withdrawal_bank+hold_bank)
                print('requested_amount',requested_amount)
                if requested_amount <= remaining_balance_bank:
                    print('amountBank:',request.POST.get('requested_amount'))
                    addnew_affiliatepayoutrequest=AffiliatePayoutRequest(affiliateid=affiliateobj,
                                                                        assigned_rm=Allusers.objects.get(id=rmid.rmid.id),
                                                                        assigned_account=Allusers.objects.get(id=19359),
                                                                        requested_method='Bank Withdrawal',
                                                                        requested_currency=requested_currency,
                                                                        requested_amount=requested_amount,
                                                                        status=False) #status=False means hold
                    addnew_affiliatepayoutrequest.save()
                    #     print('hold_bank:',affiliatepayout.hold_bank)
                    affiliatepayout.hold_bank+= requested_amount
                    affiliatepayout.save()
                else:
                    #show this msg on front end 
                    print('max amount that you can request is your remaining balance')
                    
                    #send withdrawal request to RM for approval
            elif request.POST.get('method') == 'BTC Withdrawal':
                if float(request.POST.get('amount')) <= remaining_balance_bank:
                    print('amountBTC:',request.POST.get('amount'))
                    #send withdrawal request to RM for approval
            elif request.POST.get('method') == 'USDT Withdrawal':
                if float(request.POST.get('amount')) <= remaining_balance_bank:
                    print('amountUSDT:',request.POST.get('amount'))
                    #send withdrawal request to RM for approval
            # if remaining_balance_bank


        affiliatepayout=AffiliatePayout.objects.get(affiliateid=affiliateobj)
        successful_withdrawal_bank= affiliatepayout.successful_withdrawal_bank
        hold_bank= affiliatepayout.hold_bank
        remaining_balance_bank= total_payout-(successful_withdrawal_bank+hold_bank)
        remaining_balance_bank= total_payout-(successful_withdrawal_bank+hold_bank)

        affiliatepayoutrequest= AffiliatePayoutRequest.objects.filter(affiliateid=affiliateobj).order_by('-id')
        context={'requested_currency':requested_currency,
                 'total_bank':total_payout, 
                'successful_withdrawal_bank':successful_withdrawal_bank, 
                'hold_bank':hold_bank,
                'remaining_balance_bank':remaining_balance_bank,
                'minimum_platform_limit':300,
                'affiliatepayoutrequest': affiliatepayoutrequest,
                'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,
                
                }
        return render(request, "affiliate/affiliate_payout.html",context=context)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def affiliate_offer(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'client_permission' or permissionname == 'influencer_permission':
        sys.stdout = open("offerpost.txt", "a")
        userid = request.user.id
        print('Raul')
        try:
            channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
            unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
            if unread_messages > 0:
                unread_status = True
            else:
                unread_status = False
            
            if request.user.roles=='client'    :
                rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
                rmname = rmid.rmid.rmprofile.name
                image = rmid.rmid.rmprofile.profilepic
            if request.user.roles=='influencer'    :
                rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
                rmname = rmid.rmid.rmprofile.name
                image = rmid.rmid.rmprofile.profilepic
            
            print('rmid345345',rmid)
        except:
            channel_name = 'None'
            unread_status = False
            image='none'
            rmname='None'

        if 'appliedofferid' in request.POST:
            
            data = request.POST#.decode('utf-8')  # Decode the bytes to a string
            print('askapprovaldata:',data)
            affiliateid = request.POST.get('affiliateid')
            appliedofferid = request.POST.get('appliedofferid')
            source = request.POST.get('source')
            lead_cap = request.POST.get('lead_cap')
            message1 = request.POST.get('message')

            affiliateidobj = Allusers.objects.get(id=affiliateid)
            appliedofferidobj = AdvertiserOffer.objects.get(offerid=appliedofferid)

            try:
                # Try to retrieve the existing record with the specified parameters
                RmAffiliateOfferApplication.objects.get(affiliateid=affiliateidobj, offerid=appliedofferidobj)
            
            except RmAffiliateOfferApplication.DoesNotExist:
                # If the record doesn't exist, create a new one
                utm_offerid = appliedofferidobj.offerid
                productlink_updatedutm = appliedofferidobj.productlink+f'?utm_source=influencerhiring&utm_affiliate_id={request.user.id}&utm_offerid={utm_offerid}'
                productlink_updatedutm_newdomain = f'mynewdomain.com/?utm_source=influencerhiring&utm_affiliate_id={request.user.id}&utm_offerid={utm_offerid}'
                #RmAffiliateOfferApplication use this common table in new domain to keep count and then redirect to offerid.productlink
                new_application = RmAffiliateOfferApplication(
                    affiliateid=affiliateidobj,
                    offerid=appliedofferidobj,
                    productlink_updatedutm = productlink_updatedutm,
                    traffic_source=source,
                    expected_volume_of_leads=lead_cap,
                    optional_message=message1
                )
                new_application.save()
                
        # productlink_updatedutm = RmAffiliateOfferApplication.objects.filter(affiliateid=affiliateidobj, offerid=appliedofferidobj)
        affiliateoffers = AdvertiserOffer.objects.filter(isapproved=True, isremoved=False)
        result = {'result':affiliateoffers,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name}
        return render(request, "affiliate/affiliate_offer.html", context=result)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def affiliate_campaign(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'client_permission' or permissionname == 'influencer_permission':
        sys.stdout = open("offerpost.txt", "a")
        user = request.user
        userid = request.user.id
        try:
            channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
            unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
            print('dfdsf',unread_messages)
            if unread_messages > 0:
                unread_status = True
            else:
                unread_status = False
            
            if request.user.roles=='client'    :
                rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
                rmname = rmid.rmid.rmprofile.name
                image = rmid.rmid.rmprofile.profilepic
            if request.user.roles=='influencer'    :
                rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
                rmname = rmid.rmid.rmprofile.name
                image = rmid.rmid.rmprofile.profilepic
            
            print('rmid',rmid)
        except:
            channel_name = 'None'
            unread_status = False
            image='none'
            rmname='None'
        print('jljljljljlljljl', channel_name,userid,rmname, image)
        print(11,request.method)
        if request.method=='POST':
            # sys.stdout = open("offerpost.txt", "a")
            datapost = request.POST#.decode('utf-8')  # Decode the bytes to a string
            print('datapost:',datapost)
            data=dict(datapost)
            print('newdata:', data)
            avatar_file = request.FILES.get('avatar')
            if 'deleteflagofferid' in request.POST:
                
                deleteflagofferid=request.POST.get('deleteflagofferid')
                affiliateid = request.POST.get('affiliateid')
                # affiliateidobj = ClientSettings.objects.get(csettingsuserid=request.user.id)
                affiliateidobj = Allusers.objects.get(id=request.user.id)

                offeridobj = AdvertiserOffer.objects.get(offerid=deleteflagofferid)
                
                image = RmAffiliateOfferApplication.objects.get(affiliateid=affiliateidobj, offerid=offeridobj)
                image.delete()
                print('delete execute')

        offers_qs = RmAffiliateOfferApplication.objects.filter(affiliateid=request.user.id, isapproved=False)
        
        print('offers_qs',offers_qs)

        for i in offers_qs:
        #     pass
            print(444,i.productlink_updatedutm)
        return render(request, "affiliate/affiliate_campaign.html", {'offers_qs':offers_qs,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,})
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def affiliate_lead(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'client_permission' or permissionname == 'influencer_permission':
        sys.stdout = open("offerpost.txt", "a")
        
        userid = request.user.id
        try:
            channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
            unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
            print('dfdsf',unread_messages)
            if unread_messages > 0:
                unread_status = True
            else:
                unread_status = False
            
            if request.user.roles=='client'    :
                rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
                rmname = rmid.rmid.rmprofile.name
                image = rmid.rmid.rmprofile.profilepic
            if request.user.roles=='influencer'    :
                rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
                rmname = rmid.rmid.rmprofile.name
                image = rmid.rmid.rmprofile.profilepic
            
            print('rmid',rmid)
        except:
            channel_name = 'None'
            unread_status = False
            image='none'
            rmname='None'
            
        affiliateleads = AffiliateWebhook.objects.filter(utm_affiliate_id=request.user.id)
        result = {'result':affiliateleads,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name}
        return render(request, "affiliate/affiliate_lead.html", context=result)
    return HttpResponseRedirect('/')


import uuid
# @login_required(login_url='/login/')
@csrf_exempt
def affiliate_webhook(request):
    sys.stdout = open("offerpost.txt", "a")
    if request.method == 'POST':
        uuid1 = uuid.uuid4()
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            current_ip = x_forwarded_for.split(',')[0]
        else:
            current_ip = request.META.get('REMOTE_ADDR')
        port = request.META['SERVER_PORT']
        print("IP", current_ip, port,type(current_ip))
        data = json.loads(request.body)
        full_url = request.build_absolute_uri()
        print('full url:',full_url)
        utm_source = data['utm_source']
        utm_affiliate_id = data['utm_affiliate_id']
        utm_offerid = int(data['utm_offerid'])
        remaining_offer_details=AdvertiserOffer.objects.get(offerid=utm_offerid)
        payout = remaining_offer_details.payout
        affiliate_payout = remaining_offer_details.affiliate_payout
        server_ip = remaining_offer_details.server_ip
        print('server_ip',server_ip)
        if current_ip == server_ip:#only whitelisted ip allowed
            status=True
            print("yes, request from whitelist ip" )
            lead = AffiliateWebhook(uuid=uuid1, utm_source =utm_source, utm_affiliate_id=utm_affiliate_id, utm_offerid=utm_offerid, payout=payout, affiliate_payout=affiliate_payout, server_ip=server_ip, status=status)
            lead.save()
        else:
            status=False
            print("noooooooo")
            lead = AffiliateWebhook(uuid=uuid1, utm_source =utm_source, utm_affiliate_id=utm_affiliate_id, utm_offerid=utm_offerid, payout=payout, affiliate_payout=affiliate_payout, server_ip=server_ip, status=status)
            lead.save()
        
        print(utm_source,utm_affiliate_id,utm_offerid,'lead saved')
        return HttpResponse(status=200)

@login_required(login_url='/login/')
def affiliate_bankdetail(request):
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'client_permission' or permissionname == 'influencer_permission':
        sys.stdout = open("offerpost.txt", "a")
        userid = request.user.id
        try:
            channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
            unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
            print('dfdsf',unread_messages)
            if unread_messages > 0:
                unread_status = True
            else:
                unread_status = False
            
            if request.user.roles=='client'    :
                rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
                rmname = rmid.rmid.rmprofile.name
                image = rmid.rmid.rmprofile.profilepic
            if request.user.roles=='influencer'    :
                rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
                rmname = rmid.rmid.rmprofile.name
                image = rmid.rmid.rmprofile.profilepic
            if request.user.roles=='agency'    :
                rmid = AgencyProfile.objects.get(client_userid=request.user.id).rmid
                rmname = rmid.rmid.username
                image = rmid.rmid.rmprofile.profilepic
            
            print('rmid',rmid)
        except:
            channel_name = 'None'
            unread_status = False
            image='none'
            rmname='None'
        id = Allusers.objects.filter(id=userid)
        id=id[0]
        permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
            userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
        
        accoun = Useraccounts.objects.filter(usersid=id)
        if accoun.exists():
            accoun = accoun[0]
            accno = decrypt(accoun.accountnumber)
            print("account", accno, accoun.accountnumber)
        else:
            accno = ''

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
        
        
        if permissionname == 'client_permission' or permissionname == 'agency_permission' :
            if request.method == 'POST':
                sys.stdout = open("earningsdetails.txt", "a")
                
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
                # send_customer_email(key='influencer-kycvarificationrequest',user_email=request.user.email,client=None,influencer=request.user.username,order_id=None,service_type=None,
                # order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)

                # sendkycmanagernotification(user=103899,key="kyc-influencervarification",influencer_user_name=request.user.username,client_name=None)

                return redirect(request.META['HTTP_REFERER'])
        return render(request, "affiliate/affiliate_bankdetail.html",{'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'pass': depass, 'pan': depan, 'addhar': deaddhar, 'cancel': decan,'account': accoun, 'accnum': accno})
    return HttpResponseRedirect('/')

##############################################



'''
def advertisers_offers(request):
    return render(request, "advertisers/advertisers_offers.html")


def advertisers_instructions(request):
    return render(request, "advertisers/instructions.html")


def advertisers_withdrawal_request(request):
    return render(request, "advertisers/withdrawal_requests.html")

#############################################################################

##########################################

'''