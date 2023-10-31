from django.shortcuts import render, HttpResponseRedirect
from mainapp.models import *
from Admin.models import *
from whatsapp_login.models import Whatsappuser
from agora_chat.models import *
from Account.models import *
from Creator.models import *
from mainapp.views import *
from django.contrib import auth, messages
from .models import *
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect
from random import randint
from django.db.models import Count
from mainapp.enanddc import decrypt
from inappnotifications.views import *
from threading import Thread
from django.utils import timezone
from io import BytesIO
import logging
from django.contrib.auth.hashers import make_password
import sys
from django.db.models import F
from django.core.paginator import Paginator
# Create your views here.
import xhtml2pdf.pisa as pisa
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
import markdown
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from RM.models import *
from django.contrib.auth.decorators import login_required


def SendRMreview(request,feedratevalue,feedmess):
    if request.user.roles=='influencer':
        rmid=request.user.InfluencerSettings.mappings.mappedtoid.rmid
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
    return HttpResponse(status=200)


@csrf_exempt
def getunreadmessagecount(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
    except:
        channel_name = 'None'
        unread_status = False
    return JsonResponse({'status':unread_status})


@login_required(login_url='/login/')
def User_Dashboard(request):
    #sys.stdout = open("user-cliendt-dashboared-chat.txt", "a")
    user = request.user.id
    username = request.user.username
    
    print('this is the uyser',user)
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    noti = Notifications.objects.filter(
        touserid=user).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()

    # user=95773
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    
    

    order = Orders.objects.select_related(
        'influencerid', 'orderstatus', 'serviceid').filter(clientid=user, paymentstatus=True).order_by('-ordersid')
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    act = order.filter(orderstatus__in=[6,7]).count()
    request.session['acti'] = act
    tot = order.count()
    kyc = ClientSettings.objects.get(csettingsuserid=user)
    brand = order.filter(serviceid=1).count()
    gm = order.filter(serviceid=4).count()
    vcs = order.filter(serviceid=2).count()
    ss = order.filter(serviceid=3).count()+order.filter(serviceid=7).count()
    ina = order.filter(serviceid=5).count()

    paginator = Paginator(order, 10)

    # request.session['userdet']=client_details
    
    page_obj=None

    if permissionname == 'client_permission':
        if request.method == 'GET':
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
        
        
        #sys.stdout = open("ptdt.txt", "a")
        
        
        
        
        
        
        if request.method == 'POST':
            
            print("details",request.POST)
        

            
            if 'companyname' in request.POST:   
                companyname = request.POST.get("companyname")
                companyemail = request.POST.get("companyemail")
                websitelink = request.POST.get("websitelink")
                income = request.FILES.get("income")
                gst = request.FILES.get("gst")
                print('certificate',income, gst)
                
                un=UnverifedAgencyDetails()
                un.clientid=id
                un.comapanyname=companyname
                un.email=companyemail
                un.link=websitelink
                un.itrcertficate=income
                un.gstcertificate=gst
                un.applied=True
                un.save()
                print('excdute')
                
                kycuserid=Allusers.objects.filter(roles='kyc')
        
                for i in kycuserid:
                    print("user",i.id)
        
                    Thread(target=lambda:sendkycmanagernotification(user=i.id,key='kyc-clienttoagency/brand',influencer_user_name=None,client_name=request.user.username)).start()
                    print('execute')
                    
                send_customer_email(key='client-rolechangedtoagencyrequested',user_email=request.user.email,
                   client=request.user.username,influencer=None,order_id=None,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None) 
                
        
            
            if 'feedratevalue' in request.POST:
                feedratevalue=request.POST.get('feedratevalue')
                feedmess=request.POST.get('feedmess')
                Thread(target=lambda:SendRMreview(request,feedratevalue,feedmess)).start()
                print('execute reviews')
                
 

        return render(request, "User/index.html", {'order1':order,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'noti': noti, 'notcount': conoti, 'userdet': client_details, 'order': page_obj, 'com': com, 'tot': tot, 'can': can, 'pan': pan, 'kyc': kyc, 'act': act, 'brand': brand, 'gm': gm, 'vcs': vcs, 'ss': ss, 'ina': ina})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Completed_Project(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    noti = Notifications.objects.filter(
        touserid=user).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()

    # user=95773
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    order = Orders.objects.select_related(
        'influencerid', 'clientid', 'orderstatus', 'serviceid').filter(clientid=user, paymentstatus=True).order_by('-ordersid')
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    tot = order.count()
    if permissionname == 'client_permission':
        if 'feedratevalue' in request.POST:
            feedratevalue=request.POST.get('feedratevalue')
            feedmess=request.POST.get('feedmess')
            Thread(target=lambda:SendRMreview(request,feedratevalue,feedmess)).start()
            print('execute reviews')

        return render(request, "User/complete-project.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'noti': noti, 'notcount': conoti, 'userdet': client_details, 'order': order, 'com': com, 'tot': tot, 'can': can, 'pan': pan})
    return HttpResponseRedirect("/")

#################################### 
### complete project api response function ###########

def Completed_Project_api(request):
    user = request.user.id
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    # user=95773
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    order = Orders.objects.select_related(
        'influencerid', 'clientid', 'orderstatus', 'serviceid').filter(clientid=user, paymentstatus=True).order_by('-ordersid')
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    tot = order.count()
    if permissionname == 'client_permission':
        if 'feedratevalue' in request.POST:
            feedratevalue=request.POST.get('feedratevalue')
            feedmess=request.POST.get('feedmess')
            Thread(target=lambda:SendRMreview(request,feedratevalue,feedmess)).start()
            print('execute reviews')
        
        order_values = [{'id':i['ordersid'], 'date':i['orderdate'], 'influencer':i['influencerid_id'], 'service type':i['serviceid_id'],'Orders Value':i['orderamt'],'Orders Status':'Completed'} for i in order.values() if i['orderstatus_id'] == 1]
        return JsonResponse({'data':order_values})
    return HttpResponseRedirect("/")

############### api function end#############

@login_required(login_url='/login/')
def Pending_Project(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    noti = Notifications.objects.filter(
        touserid=user).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()

    # user=95773
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    order = Orders.objects.select_related(
        'influencerid', 'clientid', 'orderstatus', 'serviceid').filter(clientid=user, paymentstatus=True).order_by('-ordersid')
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    tot = order.count()
    act = request.session.get('acti', None)
    if permissionname == 'client_permission':
        if 'feedratevalue' in request.POST:
            feedratevalue=request.POST.get('feedratevalue')
            feedmess=request.POST.get('feedmess')
            Thread(target=lambda:SendRMreview(request,feedratevalue,feedmess)).start()
            print('execute reviews')
        return render(request, "User/pending-project.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'sct': act, 'noti': noti, 'notcount': conoti, 'userdet': client_details, 'order': order, 'com': com, 'tot': tot, 'can': can, 'pan': pan})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Cancel_Project(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    noti = Notifications.objects.filter(
        touserid=user).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()

    # user=95773
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    order = Orders.objects.select_related(
        'influencerid', 'clientid', 'orderstatus', 'serviceid').filter(clientid=user, paymentstatus=True).order_by('-ordersid')
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    tot = order.count()
    act = request.session.get('acti', None)

    if permissionname == 'client_permission':
        if 'feedratevalue' in request.POST:
            feedratevalue=request.POST.get('feedratevalue')
            feedmess=request.POST.get('feedmess')
            Thread(target=lambda:SendRMreview(request,feedratevalue,feedmess)).start()
            print('execute reviews')
        return render(request, "User/cancel-project.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'act': act, 'noti': noti, 'notcount': conoti, 'userdet': client_details, 'order': order, 'com': com, 'tot': tot, 'can': can, 'pan': pan})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Active_Project(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    noti = Notifications.objects.filter(
        touserid=user).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    act = request.session.get('acti', None)
    # user=95773
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    order = Orders.objects.select_related(
        'influencerid', 'clientid', 'orderstatus', 'serviceid').filter(clientid=user, paymentstatus=True).order_by('-ordersid')
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    tot = order.count()

    if permissionname == 'client_permission':
        if 'feedratevalue' in request.POST:
            feedratevalue=request.POST.get('feedratevalue')
            feedmess=request.POST.get('feedmess')
            Thread(target=lambda:SendRMreview(request,feedratevalue,feedmess)).start()
            print('execute reviews')

        return render(request, "User/active-orders.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'act': act, 'noti': noti, 'notcount': conoti, 'userdet': client_details, 'order': order, 'com': com, 'tot': tot, 'can': can, 'pan': pan})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Activities(request):

    client_details = request.session.get('userdet')

    return render(request, "User/activity.html")


# def GroupChats(request):
#     user = request.user.id
#     client_details = ClientProfile.objects.select_related(
#         'client_userid').filter(client_userid=user)
#     id = Allusers.objects.filter(id=user)
#     id = id[0]
#     permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
#         userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    
    
#     act = request.session.get('acti', None)
    
#     noti = Notifications.objects.filter(
#         touserid=user).order_by('-notificationid')
#     conoti = noti.filter(notificationstatus=False).count()
    
    
#     if permissionname == 'client_permission':
    
#         return render(request, "User/groupchat.html",{'act': act,'userdet':client_details,'noti': noti, 'notcount': conoti,})
#     return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Client_Referral(request):
    #sys.stdout = open("ptdt.txt", "a")
    sys.stdout = open("offerpost1212", "a")
    print(11)
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    
    
    act = request.session.get('acti', None)
    
    
    
    if client_details[0].country =='India' or client_details[0].country ==None:
        curs1='INR'
    else:
        curs1='USD'
    

    
    exrate=ExchangeRates.objects.get(countery_abbrevation=curs1).rates
    # print("rated",exrate)
    ref=UserReferral.objects.get(user=user)
    succredit=float(ref.successful_referral_count*exrate)
    # print('credit',succredit)
    pencredit=ref.potential_referral_count*exrate
    
    
    try:
        
        # clientpayout=ClientPayout.objects.get(clientid=request.user.id)
        # currency=clientpayout.currency
        print('userid',request.user.id)
        clientprofile=ClientProfile.objects.get(client_userid=request.user.id)
        # currency=clientprofile.currency
        print('clientprofile.currency',clientprofile.currency)
        if clientprofile.currency is None or clientprofile.currency =='':
            permissionname=None

        # elif (clientprofile.currency is not None or clientprofile.currency !='') and clientpayout.currency is None or clientpayout.currency == '':
        #     pass               
    except:
        permissionname=None
        
    
    
    print('permissionname',permissionname)
    if permissionname == 'client_permission':
    
        return render(request, "User/referrals.html",{'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'pencredit':pencredit,'succredit':succredit,'ref':ref,'act': act,'userdet':client_details,})
    elif permissionname == None:
        messages.warning(
                        request, "Please enter your country to access this page")
        return HttpResponseRedirect("/Profile-Setting/")
    else:
        return HttpResponseRedirect("/")


def htmltopdf(html,orderid):
    # Generate PDF from the rendered HTML
    pdf_file = BytesIO()
    pisa.CreatePDF(html, dest=pdf_file)
    pdf_file.seek(0)
    inv=Invoices.objects.get(ordersid=orderid)
    filename='INV-'+str(inv.invoiceid)+str(inv.invoicedate)+'.pdf'
    invi=Invoices.objects.filter(ordersid=orderid,invoicename=filename)
    if invi.exists():
        pass
    else:
        inv.invoicename=filename
        inv.document.save(filename, ContentFile(pdf_file.getvalue()))
        inv.save()
        

# @ratelimit(key='ip', rate='5/m', block=True)
# @ratelimit(key='ip', rate='3/m', block=True)


    
@login_required(login_url='/login/')
def Orders_Invoice1(request,orderid=None):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    

    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    act = request.session.get('acti', None)
    
    if orderid is None:
        orderid = request.session.get('INVID')
    else:
        orderid=decrypt(orderid)
    
    pay=Payments.objects.filter(ordersid=orderid)
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=str(pay[0].ordersid.clientid.id))

    template = 'User/invoice.html'
    context = {
        'pay': pay,
        'act': act,
        'userdet': client_details,
        
    }
    html = render_to_string(template, context)
    # htmltopdf(html,orderid)
    
        
    # if permissionname == 'client_permission':
        
    
    return render(request, "User/invoice.html",{'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'pay':pay,'act': act,'userdet':client_details,})
    # return HttpResponseRedirect("/")
    



from django.db import connection


def Clientinfluencerqnandans(order_id, influencer_id, service_id):
    # Fetch matching rows from Orderrequirementquestions and Influencerquestions
    query = """
    -- Fetch matching rows from Client_orderrequirementquestions and Client_influencerquestions
    SELECT
        "Client_orderrequirementquestions"."orderrequirementquestionsid",
        "Client_orderrequirementquestions"."answer",
        "Client_influencerquestions"."influencerquestionsid",
        "Client_influencerquestions"."influencerid",
        "Client_influencerquestions"."serviceid",
        "Client_influencerquestions"."question",
        "Client_influencerquestions"."subheading",
        "Client_orderrequirementquestions"."orderid",
        "Client_orderrequirementquestions"."date"
    FROM
        "Client_orderrequirementquestions"
    INNER JOIN
        "Client_influencerquestions" ON ("Client_orderrequirementquestions"."question" = "Client_influencerquestions"."influencerquestionsid")
    WHERE
        "Client_orderrequirementquestions"."orderid" = %s
        AND "Client_influencerquestions"."influencerid" = %s
        AND "Client_influencerquestions"."serviceid" = %s

    UNION

    -- Fetch existing rows from Client_influencerquestions not matching with Client_orderrequirementquestions
    SELECT
        NULL AS "orderrequirementquestionsid",
        NULL AS "answer",
        "Client_influencerquestions"."influencerquestionsid",
        "Client_influencerquestions"."influencerid",
        "Client_influencerquestions"."serviceid",
        "Client_influencerquestions"."question",
        "Client_influencerquestions"."subheading",
        NULL AS "orderid",
        NULL AS "date"
    FROM
        "Client_influencerquestions"
    LEFT JOIN
        "Client_orderrequirementquestions" ON ("Client_orderrequirementquestions"."question" = "Client_influencerquestions"."influencerquestionsid")
    WHERE
        ("Client_orderrequirementquestions"."orderid" IS NULL
        AND "Client_influencerquestions"."influencerid" = %s
        AND "Client_influencerquestions"."serviceid" = %s);
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [order_id, influencer_id, service_id, influencer_id, service_id])
        results = cursor.fetchall()

    return results

    

    









@login_required(login_url='/login/')
def OrdersDetails(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    orderid = request.session.get('ODRID')
    order_details = Orders.objects.select_related(
        'clientid', 'serviceid', 'influencerid', 'orderstatus').filter(ordersid=orderid, paymentstatus=True)
    
    
    
    paymentdet = Payments.objects.filter(ordersid=orderid)
    print("data",paymentdet)
    cltdet = ClientProfile.objects.get(
        client_userid=int(user))  # order_details[0].clientid.id
    act = request.session.get('acti', None)
    # print("user", user, cltdet, order_details, orderid, paymentdet)
    chtme=OrderChat.objects.filter(orderid=orderid).order_by('date')
    noti = Notifications.objects.filter(
        touserid=user).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()
    
    red=OrderResponse.objects.filter(orderid=orderid)
    shrew=InfluencersReview.objects.filter(orderid=str(orderid))
    if shrew.exists():
        shrew=shrew[0]
    else:
        shrew=''
    
    
    
    
    # Retrieve a random entry by ordering the queryset randomly and selecting the first element
    random_review = Defaultreviews.objects.filter(serviceid=str(order_details[0].serviceid.serviceid)).order_by('?')[0]
    
    # ques=Influencerquestions.objects.filter(influencerid=str(order_details[0].influencerid.influencer_userid),serviceid=str(order_details[0].serviceid))
    
    
    
    ques=Clientinfluencerqnandans(orderid,order_details[0].influencerid.influencer_userid.id,order_details[0].serviceid.serviceid)
    
    
    if permissionname == 'client_permission':
        if request.method == 'POST':
            print("data",request.POST)
            mess=request.POST.get('content')
            if mess is not None and len(mess) > 0:
                ch=OrderChat(userid=id,text=mess,orderid=order_details[0])
                ch.save()
                print("Save chat")
                
            
            
                
            if 'acceptorder' in request.POST:
                acceptorder=request.POST.get('acceptorder')
                if  acceptorder=='':
                    if order_details.exists():
                        osid=Orderstatus.objects.get(status='Completed')
                        order_details=order_details[0]
                        order_details.completedate = timezone.now()
                        order_details.orderstatus=osid
                        order_details.isresponseapprovedbyclient=True
                        order_details.save(update_fields=['isresponseapprovedbyclient','orderstatus', 'completedate'])
                        
                        
                        
                        clientid=order_details.influencerid.influencer_userid
                        clientpayout, created = ClientPayout.objects.get_or_create(clientid=clientid, defaults={
                        'remaining_balance_bank':0, 'successful_withdrawal_bank':0, 'hold_bank':0,
                    
                        })
                    
                        payments=Payments.objects.get(ordersid=str(order_details.ordersid))
                        
                        sys.stdout = open("ptdt.txt", "a")
                        print('order',order_details.iscouponapplied,type(order_details.iscouponapplied))
                        
                        
                        requested_currency =payments.ordersid.paymentcurrency
                        if requested_currency == 'INR':
                            
                            if order_details.iscouponapplied:
                                newprice=order_details.planid.planprice-order_details.totaldiscount
                                clientpayout.remaining_balance_bank +=  newprice
                                print('execute ifeer')
                            else:
                            
                                clientpayout.remaining_balance_bank += order_details.planid.planprice
                                newprice=order_details.planid.planprice
                                print('execute ielsee')
                                
                            clientpayout.currency=requested_currency
                            clientpayout.save()
                            clientpayouthistory = ClientPayoutHistory(clientid=clientid, paymentid=payments,requested_currency=requested_currency,wallet_transaction_amount=int(newprice),isrefund_balance=True,isrefund_hold=False,remark='Order Completed')
                            clientpayouthistory.save()
                            payments.is_refunded=True
                            
                                    
                        Thread(target=lambda:sendusernotification(user=order_details.clientid.id,key='user-orderaccepted',RM_Name=None,Influencer_Name=order_details.influencerid.influencer_userid.username,Product_Name=order_details.serviceid.servicename,Decline_Reason=None,Order_Id=order_details.ordersid)).start()
                        
                        Thread(target=lambda:sendRMnotification(key='rm-influencerordercompleted',RM_Name=None,client_type=None,client_Name=order_details.clientid.username,rmid=order_details.rmid,Influencer_Name=order_details.influencerid.influencer_userid.username,Order_ID=order_details.ordersid,reason=None,Order_Stage=None)).start()

                        Thread(target=lambda:sendInfluencernotification(user=order_details.influencerid.influencer_userid.id,key='influencer-ordercompleted',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=order_details.ordersid,reason=None)).start()
                        send_customer_email(key='influencer-ordercompleted',user_email=order_details.influencerid.influencer_userid.email,
                   client=order_details.clientid.username,influencer=order_details.influencerid.influencer_userid.username,order_id=order_details.ordersid,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)   
                        
                        send_customer_email(key='client-ordercompleted',user_email=order_details.clientid.email,
                   client=order_details.clientid.username,influencer=order_details.influencerid.influencer_userid.username,order_id=order_details.ordersid,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)   
                        
                        
                                    
                        print("approved ok")
            frontlist = dict(request.POST)
            if 'answer' in frontlist:
                answer = frontlist["answer"]
                questionid = frontlist["questionid"]

                print(answer,type(answer))
                for i in range(len(questionid)):
                    if answer[i] != '':
                        print('qn',questionid[i])
                        print('ans',answer[i])
                        qnre=Orderrequirementquestions.objects.filter(question=str(questionid[i]),orderid=orderid)
                        if qnre.exists():
                            qnre=qnre[0]
                            qnre.answer=answer[i]
                            qnre.save(update_fields=['answer'])
                        else:
                            qno=Influencerquestions.objects.get(influencerquestionsid=questionid[i])
                            ords=Orders.objects.get(ordersid=orderid)
                            re=Orderrequirementquestions(answer=answer[i],question=qno,orderid=ords)
                            re.save()
             
                
            
            
            if 'cancelorder' in request.POST:
                reason=request.POST.get('reason')
                if order_details.exists():
                    order_details=order_details[0]
                    order_details.isresponseapprovedbyclient=False
                    order_details.save(update_fields=['isresponseapprovedbyclient'])
                re=Ordercancelreasons.objects.filter(orderid=str(order_details.ordersid),clientid=str(request.user.id))
                if re.exists():
                    re=re[0]
                    re.reason=reason
                    re.save(update_fields=['reason'])
                    print('up rea')
                else:
                    cls=Allusers.objects.get(id=str(request.user))
                    re = Ordercancelreasons(
                    orderid=order_details, reason=reason, clientid=cls)
                    re.save()
                    print('single reason')
                print("cancelled",reason)

                # Thread(target=lambda:sendusernotification(user=order_details.clientid.id,key='user-revieworder',RM_Name=None,Influencer_Name=order_details.influencerid.influencer_userid.username,Product_Name=order_details.serviceid.servicename,Decline_Reason=None,Order_Id=order_details.ordersid)).start()
                        
                Thread(target=lambda:sendRMnotification(key='rm-userdeclineorder',RM_Name=None,client_type=None,client_Name=order_details.clientid.username,rmid=order_details.rmid,Influencer_Name=order_details.influencerid.influencer_userid.username,Order_ID=order_details.ordersid,reason=reason,Order_Stage=None)).start()

                Thread(target=lambda:sendInfluencernotification(user=order_details.influencerid.influencer_userid.id,key='influencer-orderdecline',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=order_details.ordersid,reason=reason)).start()
                
                send_customer_email(key='influencer-orderdeclinedbyuser',user_email=order_details.influencerid.influencer_userid.email,
                   client=order_details.clientid.username,influencer=order_details.influencerid.influencer_userid.username,order_id=order_details.ordersid,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=reason)   

            
            if 'feedratevalue' in request.POST:
                feedratevalue=request.POST.get('feedratevalue')
                feedname=request.POST.get('feedname')
                feedmess=request.POST.get('feedmess')
                feedordid=request.POST.get('feedordid')
                feedctid=request.POST.get('feedctid')
                feedinid=request.POST.get('feedinid')
                
                
                
                inrew=InfluencersReview.objects.filter(orderid=str(feedordid))
                if inrew.exists():
                    inrew=inrew[0]
                    inrew.review_message=feedmess
                    inrew.name=feedname
                    inrew.rating=int(feedratevalue)
                    inrew.isapproved=False
                    inrew.save(update_fields=['review_message','name','rating','isapproved'])
                    print('update reqview')
                else:
                    inrew=InfluencersReview()
                    inrew.clientid=Allusers.objects.get(id=feedctid)
                    inrew.influencerid=InfluencerSettings.objects.get(influencer_userid=str(feedinid))
                    inrew.orderid=Orders.objects.get(ordersid=feedordid)
                    inrew.review_message=feedmess
                    inrew.name=feedname
                    inrew.rating=int(feedratevalue)
                    inrew.isapproved=False
                    inrew.save()
                    print('save review')
                    
                send_customer_email(key='influencer-clientgivefeedback',user_email=inrew.influencerid.influencer_userid.email,
                   client=inrew.clientid.username,influencer=inrew.influencerid.influencer_userid.username,order_id=None,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)
                kycids=Allusers.objects.filter(roles='kyc')
                for i in kycids:
                    Thread(target=lambda:sendkycmanagernotification(user=i.id,key='kyc-influencerreview',influencer_user_name=None,client_name=None)).start()
            return redirect(request.META['HTTP_REFERER'])
        return render(request, "User/Orders-details.html", {'random_review':random_review,'shrew':shrew,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'ques':ques,'userdet':client_details,'noti': noti, 'notcount': conoti, 'order': order_details, 'pymethod': paymentdet, 'cli': cltdet, 'act': act,'chtme':chtme,'res':red})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Setting(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    cltdet = ClientProfile.objects.select_related('client_userid').filter(
        client_userid=int(user))
    
    if cltdet[0].country is None or cltdet[0].country =='':
        messages.warning(
                        request, "Please, update your profile details and country.")
    
        
        
    
    
    orid = Orders.objects.filter(clientid=str(user),paymentstatus=True).last()
    logs = LoginIP.objects.filter(
        userid=user).order_by('-LoginIPid')[0:3]
    act = request.session.get('acti', None)
    
    exch = ExchangeRates.objects.all().order_by('country')
    langes=Languages.objects.all()
    
    if permissionname == 'client_permission':
        if request.method == 'POST':




            if "OTP" in request.POST:
                comOTP = request.POST.get("OTP")
                
                emailotp = request.session.get('emailotp', None)
                emailverify = request.session.get('emailverify', None)
                
                if comOTP == emailotp:
                    if emailverify is not None and len(emailverify) > 0  :
                        
                        id.email = emailverify
                        id.save(update_fields=['email'])
                        
                        emaset=ClientSettings.objects.get(csettingsuserid=user)
                        emaset.email_verified=True
                        emaset.save()
                else:
                    messages.warning(
                        request, "OTP mismtached, please enter correct otp!...")
                        
                        
                    


            if 'profile_phone' in request.POST:

                profile_phone = request.POST.get('profile_phone')

                print("profile", profile_phone)
                pclnt = ClientProfile.objects.get(client_userid=str(user))
                if profile_phone is not None and len(profile_phone) > 1:
                    pclnt.mobile = profile_phone
                    print('up phone')
                pclnt.save()

            elif 'new_password' in request.POST and 'confirm_password' in request.POST:

                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')

                print("new pass", new_password)
                print("sdfds", confirm_password)
                if new_password is not None and len(new_password) > 0 and new_password == confirm_password:
                    id.password = make_password(new_password)
                    appuser=Whatsappuser.objects.filter(clientid=str(id.username))
                    if appuser.exists():
                        appuser=appuser[0]
                        appuser.access_id=new_password
                        appuser.secret_id=id.password
                        appuser.save(update_fields=['access_id','secret_id'])
                    id.save(update_fields=['password'])
                    update_session_auth_hash(request, id)
                                    
                    
            
                    
                           
                    print("up password")

            else:
                image = request.FILES.get("avatar")
                name = request.POST.get("name")
                emailaddress = request.POST.get("emailaddress")
                phone = request.POST.get("phone")
                country = request.POST.get("country")
                language = request.POST.get("language")
                timezone = request.POST.get("timezone")
                pin = request.POST.get('pin')
                address = request.POST.get('address')
                
                
                        
                
                

                pclnt = ClientProfile.objects.get(client_userid=str(user))
                
                if pclnt.country is None or pclnt.country == '' :
                    if country=='India':
                        # currnecy=request.POST.get('currnecy')
                        currnecy='INR'
                    elif country!='India' and country != '' and country is not None :
                        currnecy='USD'
                    else:
                        currnecy=None
                
                    if currnecy is not None and len(currnecy) > 1:
                        pclnt.currency = currnecy
                        print('up currnecy')
                    
                        clientpayout, created = ClientPayout.objects.get_or_create(clientid=cltdet[0].client_userid, defaults={
                            'remaining_balance_bank':0, 'successful_withdrawal_bank':0, 'hold_bank':0,
                        
                            })
                        clientpayout.currency = currnecy #request.user.clientprofile.currency
                        clientpayout.save()
                
                
                
                if image is not None and len(image) > 1:
                    pclnt.profileimage = image
                    print('up image')
                if name is not None and len(name) > 1:
                    pclnt.fullname = name
                    print('up name')

                if phone is not None and len(phone) > 1:
                    pclnt.mobile = phone
                    print('up phonr')

                if country is not None and len(country) > 1:
                    pclnt.country = country
                    print('up country')

                if language is not None and len(language) > 1:
                    pclnt.language = language
                    print('up lanuaguage')

                if timezone is not None and len(timezone) > 1:
                    pclnt.timezone = timezone
                    print('up timezone')

                if pin is not None and len(pin) > 1:
                    pclnt.postalcode = pin
                    print('up pin')

                if address is not None and len(address) > 1:
                    pclnt.address = address

                    print("up address")

                
                    print("up email id")
                pclnt.save()

                print("api", image, name, emailaddress, phone,
                      country, language, timezone, pin, address)
            return redirect(request.META['HTTP_REFERER'])

        
        return render(request, "User/settings.html", {'langes':langes,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'exch':exch,'act': act, 'cltdet': cltdet, "orid": orid, 'log': logs, 'userdet': cltdet})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Pitching_Detail(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    noti = Notifications.objects.filter(
        touserid=user).order_by('-notificationid')
    conoti = noti.filter(notificationstatus=False).count()

    infoid = request.session.get('pitchinfoid')
    pitchid = request.session.get('pitchid')
    callid = request.session.get('callid')

    call = Casting_Call.objects.get(castingcallid=callid)
    pitch = PitchingCastingCall.objects.get(pitchingCastingCallid=pitchid)
    infl = InfluencerProfile.objects.get(influencer_userid=infoid)
    email = Allusers.objects.get(id=infoid).email

    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    act = request.session.get('acti', None)
    if permissionname == 'agency_permission':
        #sys.stdout = open("ptdt.txt", "a")
        if request.method == 'POST':
            canel = request.POST.get("cancelorder")
            if canel is not None:
                pt = PitchingCastingCall.objects.filter(
                    pitchingCastingCallid=canel)
                if pt.exists():
                    pt = pt[0]
                    pt.approved = False
                    pt.save(update_fields=['approved'])
                    print("not approved")
            acce = request.POST.get("acceptorder")
            if acce is not None:
                pt = PitchingCastingCall.objects.filter(
                    pitchingCastingCallid=acce)
                if pt.exists():
                    pt = pt[0]
                    pt.approved = True
                    pt.save(update_fields=['approved'])
                    print("update approved")
                    
            print("cancel", canel)
            print("accep", acce)

        print("Infoid", infoid, pitchid, callid)
        #sys.stdout.close()
        return render(request, "User/pitching-details.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'noti': noti, 'notcount': conoti, 'call': call, 'pitch': pitch, 'info': infl, 'email': email, 'userdet': client_details, 'act': act})
    return HttpResponseRedirect("/")



@login_required(login_url='/login/')
def My_Wishlist(request):
    user = request.user
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    wh=Wishlist.objects.filter(clientid=str(user.id))
    t1=[]
    for i in wh:
        info=InfluencerProfile.objects.get(influencer_userid=str(i.influencerid))
        t=(info.profileimage,info.influencer_userid.username,info.fullname,Shortdescription.objects.get(
                        shortdescriptionid=info.short_description).shortdestext,info.currency,)
        pri=PricingPlans.objects.get(usersid=str(i.influencerid),plan_type='Basic',serviceid=1).increasedprice
        t=t+(str(pri),i.wishlistid)
        t1.append(t)
    return render(request, "User/wishlist.html",{'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'wh':t1,'userdet': client_details})

@login_required(login_url='/login/')
def MyCart(request):
    user = request.user
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    wh=Cart.objects.filter(clientid=str(user.id))
    t1=[]
    for i in wh:
        info=InfluencerProfile.objects.get(influencer_userid=str(i.influencerid))
        t=(info.profileimage,info.influencer_userid.username,info.fullname,Shortdescription.objects.get(
                        shortdescriptionid=info.short_description).shortdestext,info.currency,)
        pri=PricingPlans.objects.get(usersid=str(i.influencerid),plan_type='Basic',serviceid=1).increasedprice
        t=t+(str(pri),i.Cartid)
        t1.append(t)
    return render(request, "User/mycart.html",{'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'wh':t1,'userdet': client_details})



@login_required(login_url='/login/')
def Blogs_Home_User(request, cate=None):
    user = request.user
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    blog = Blog.objects.all()
    act = request.session.get('acti', None)
    if cate is not None:
        blog = Blog.objects.filter(blog_categories__icontains=cate)
    
    if 'feedratevalue' in request.POST:
        feedratevalue=request.POST.get('feedratevalue')
        feedmess=request.POST.get('feedmess')
        Thread(target=lambda:SendRMreview(request,feedratevalue,feedmess)).start()
        print('execute reviews')

    return render(request, "User/bloghome.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'act': act, "allblog": blog, 'userdet': client_details})
    # return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Blogs_Post_User(request, name):
    user = request.user
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid
      
        rmname = rmid.rmid.rmprofile.name
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    # name = name.replace('-', ' ')
    print(name)
    base_url = "{0}://{1}{2}".format(request.scheme,
                                     request.get_host(), request.path)
    print("Url", base_url)

    act = request.session.get('acti', None)
    blog = Blog.objects.all()
    bcate = BlogCategory.objects.all()
    blog1 = blog.order_by('-date').values()[0:5]
    bldet = Blog.objects.filter(url_structure__icontains=name)[0]
    print("sdagf", bldet)
    
    content=Blogcontent.objects.filter(blog=str(bldet.blogid)).order_by('blogcontentid')
    if content.exists():
        content=content
    else:
        content=''
    bl = BlogComments.objects.filter(blog=bldet, isapproved=True)
    num = len(bl)
    print("number", num)
    client_details = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=user)
    return render(request, "User/blogdetails.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'content':content,'det': bldet, "blogdeatils": blog, 'comm': bl, 'rc': blog1, 'num': num, 'cate': bcate, 'link': base_url, 'userdet': client_details, 'act': act})



def generate_password1(length):     
    characters = string.ascii_letters + string.digits + string.punctuation 
    password = ''.join(random.choice(characters) for i in range(length)) 
    return password



def Actypeid(request):
    sys.stdout = open('Actypeid_33.txt', 'a')
    if request.method == 'POST':
        #sys.stdout = open("services21345.txt", "a")
        print("rahyul", request.POST.get('actype'), request.POST)

        actype = request.POST.get('actype')
        cursor = connection.cursor()

        roles='client'
        cursor.execute('call usersroleupdation(%s,%s,%s)',
                       (request.user.id, roles, actype))
        country = request.POST.get('country')
        
        

        if country=='India':
            currency='INR'
        elif country!='India' and country != '' and country is not None :
            currency='USD'
        else:
            currency=None
        
        # currency = request.POST.get('currency')
        mob=None
        if actype == 'client':
            user = ClientProfile.objects.get(
                client_userid=str(request.user.id))
            user.country = country
            user.currency = currency
            user.save()
            #######################################################################

            clientpayout, created = ClientPayout.objects.get_or_create(clientid=user.client_userid, defaults={
                        'remaining_balance_bank':0, 'successful_withdrawal_bank':0, 'hold_bank':0,
                       
                        })
        
            clientpayout.currency = currency #request.user.clientprofile.currency
            clientpayout.save()
            #######################################################################
            RM_Name = user.rmid.rmid.username
            rmid = user.rmid.rmid.id
            sendusernotification(user=user.client_userid.id,key='user-registration',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=None)
            sendusernotification(user=user.client_userid.id,RM_Name=RM_Name,Influencer_Name=None,Product_Name=None,Decline_Reason=None,key='user-assignrm',Order_Id=None)
            sendRMnotification(key='rm-assignuserinfluorbrand',RM_Name=RM_Name,client_type=user.client_userid.roles,client_Name=user.client_userid.username,rmid=rmid,Influencer_Name=None,Order_ID=None,reason=None,Order_Stage=None)
            mangeids=Allusers.objects.filter(roles='manager')
            for i in mangeids:
                sendmanagernotification(user=i.id,key='manager-newuserregistered',client_id=user.client_userid.id,client_name=user.client_userid.username,influencer_name=None)

            mob=request.user.clientprofile.mobile
            print('this is mobile no. of user client',mob)
            
            send_customer_email(key='client-newrmassigned',user_email=user.client_userid.email,
                client=user.client_userid.username,influencer=None,order_id=None,service_type=None,
        order_start_date=None,order_end_date=None,rm=RM_Name,casting_call_id=None,brief_pitch=None,decline_reson=None) 
            
            
        if actype == 'agency':
            user = AgencyProfile.objects.get(
                agency_userid=str(request.user.id))
            user.country = country
            user.currency = currency
            user.save()
            RM_Name = request.user.agencyprofile.rmid.rmid.username
            rmid = user.rmid.rmid.id
            
            sendusernotification(user=user.agency_userid.id,key='user-registration',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=None)
            sendusernotification(user=user.agency_userid.id,RM_Name=RM_Name,Influencer_Name=None,Product_Name=None,Decline_Reason=None,key='user-assignrm',Order_Id=None)
            sendRMnotification(key='rm-assignuserinfluorbrand',RM_Name=RM_Name,client_type=user.agency_userid.roles,client_Name=user.agency_userid.username,rmid=rmid,Influencer_Name=None,Order_ID=None,reason=None,Order_Stage=None)
            mangeids=Allusers.objects.filter(roles='manager')
            for i in mangeids:
                sendmanagernotification(user=i.id,key='manager-newuserregistered',client_id=user.agency_userid.id,client_name=user.agency_userid.username,influencer_name=None)
            
            mob=request.user.agencyprofile.mobile
            
            send_customer_email(key='client-newrmassigned',user_email=user.agency_userid.email,
                client=user.agency_userid.username,influencer=None,order_id=None,service_type=None,
        order_start_date=None,order_end_date=None,rm=RM_Name,casting_call_id=None,brief_pitch=None,decline_reson=None) 
            


        if actype == 'influencer':
            user = InfluencerProfile.objects.get(
                influencer_userid=str(request.user.id))
            user.country = country
            user.currency = currency
            user.save()
            sendInfluencernotification(user=user.influencer_userid.id,key='influencer-registration',RM_Name=None,Influencer_Name=user.influencer_userid.username,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None)
            sendInfluencernotification(user=user.influencer_userid.id,key='influencer-profileupdate',RM_Name=None,Influencer_Name=user.influencer_userid.username,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None)

            mob=request.user.influencerprofile.mobile

            RM_Name = Rmtoinfluencermappings.objects.get(mappedid=str(user.influencer_userid.id)).mappedtoid.rmid.username

                        
            send_customer_email(key='client-newrmassigned',user_email=user.influencer_userid.email,
                client=user.influencer_userid.username,influencer=None,order_id=None,service_type=None,
        order_start_date=None,order_end_date=None,rm=RM_Name,casting_call_id=None,brief_pitch=None,decline_reson=None) 
                    
            

        pro = Allusers.objects.get(id=str(request.user.id))
        pro.profilestatus = True
        pward = generate_password1(8)
        send_customer_email(key='user-mailusernamepassword',user_email=pro.email,client=pro.username,influencer=None,order_id=None,service_type=None,order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None,pward=pward)
        haspass=make_password(pward)
        pro.password=haspass
        pro.save()
        update_session_auth_hash(request, pro)
        
        
        appuser=Whatsappuser.objects.filter(clientid=str(pro.username))
        if appuser.exists():
            appuser=appuser[0]
            appuser.access_id=pward
            appuser.secret_id=haspass
            appuser.save(update_fields=['access_id','secret_id'])
        
        
        print('execute')

        ##############################################################
        generate_referral_id = UserReferral(
        user=pro, referral_id='CPA'+pro.username+'_'+str(int(time.time())), potential_referral_count_detail={'all': []})
        generate_referral_id.save()
        ##############################################################

        ip_add = get_client_ip(request)
        ln = LoginIP(userid=request.user.id, username=request.user.username, IP_Address=ip_add, location=get_location(
                    request), sessionkey=request.session.session_key, device=request.META.get('HTTP_USER_AGENT', ''))
        ln.save()
        
        
        new_user(request, pro.username, 'new_user', pro.email,
            'new-user-registration.html', 'Welcome to '+pro.username, None)


        cursor.close()
        if mob is not None or '':
            username=request.user.username
            pward=Whatsappuser.objects.get(clientid=str(request.user.username)).access_id
            password_user_id = f"""🌟 Welcome to Influencer Hiring! 🌟\n\nTo get started quickly, you can use the temporary credentials below to log in:\nuser id- {username} (This is your unique identifier and cannot be changed)\npassword- {pward}\n\n🔒 Please, set your email and password immediately once you log in to ensure your account's security."""
            send_msg_whatsapp(mob,password_user_id)
        # sys.stdout.close()
        return HttpResponse({'Result': 'Savedid'}, status=200)
    


logger = logging.getLogger()
fh = logging.FileHandler('client_view_log.txt')
logger.addHandler(fh)
