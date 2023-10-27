from django.contrib import messages
from inappnotifications.views import *
from django.shortcuts import render, HttpResponseRedirect
from mainapp.models import *
from whatsapp_login.views import Whatsappuser
from django.contrib.auth import update_session_auth_hash
from Admin.models import *
from RM.models import *
from random import randint
from django.db.models import Count
from agora_chat.models import *
from Account.models import *
from threading import Thread
from Creator.models import *
from Client.models import *
from django.shortcuts import redirect
from mainapp.enanddc import decrypt
from django.utils import timezone
from itertools import zip_longest
from io import BytesIO
import logging
from django.contrib.auth.hashers import make_password
import sys
from django.db.models import F
import xhtml2pdf.pisa as pisa
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
import markdown
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required




def testing(request):
    mangeids=Allusers.objects.filter(roles='manager')
    for i in mangeids:
        Thread(target=lambda:sendmanagernotification(user=i.id,key='manager-newuserregistered',client_id=None,client_name=None,influencer_name=None)).start()
    return HttpResponse('Manmohan Pagla hai')



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
def agency_dashboard(request):
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
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
        print('rmid name',rmid)
        rmname = rmid
        print('rm name',rmname)
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
    
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
    
    order = Orders.objects.select_related(
        'influencerid', 'orderstatus', 'serviceid').filter(clientid=user, paymentstatus=True).order_by('-ordersid')
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    act = order.filter(orderstatus__in=[6,7]).count()
    request.session['acti'] = act
    tot = order.count()
    kyc = AgencySettings.objects.get(asettingsuserid=user)
    brand = order.filter(serviceid=1).count()
    gm = order.filter(serviceid=4).count()
    vcs = order.filter(serviceid=2).count()
    ss = order.filter(serviceid=3).count()+order.filter(serviceid=7).count()
    ina = order.filter(serviceid=5).count()
    if permissionname == 'agency_permission':
                
        if 'feedratevalue' in request.POST:
            feedratevalue=request.POST.get('feedratevalue')
            feedmess=request.POST.get('feedmess')
                        
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
        return render(request, "index.html", {'order1':order,'order':order,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name, 'userdet': client_details,  'com': com, 'tot': tot, 'can': can, 'pan': pan, 'kyc': kyc, 'act': act, 'brand': brand, 'gm': gm, 'vcs': vcs, 'ss': ss, 'ina': ina})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def completed_project(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
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
   
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
    order = Orders.objects.select_related(
        'influencerid', 'clientid', 'orderstatus', 'serviceid').filter(clientid=user, paymentstatus=True).order_by('-ordersid')
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    tot = order.count()
    if permissionname == 'agency_permission':

        return render(request, "complete-project.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'userdet': client_details, 'order': order, 'com': com, 'tot': tot, 'can': can, 'pan': pan})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def pending_project(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
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
    
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
    order = Orders.objects.select_related(
        'influencerid', 'clientid', 'orderstatus', 'serviceid').filter(clientid=user, paymentstatus=True).order_by('-ordersid')
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    tot = order.count()
    act = request.session.get('acti', None)
    if permissionname == 'agency_permission':
        return render(request, "pending-project.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'sct': act, 'userdet': client_details, 'order': order, 'com': com, 'tot': tot, 'can': can, 'pan': pan})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def cancel_project(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
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
    

    
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
    order = Orders.objects.select_related(
        'influencerid', 'clientid', 'orderstatus', 'serviceid').filter(clientid=user, paymentstatus=True).order_by('-ordersid')
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    tot = order.count()
    act = request.session.get('acti', None)

    if permissionname == 'agency_permission':
        return render(request, "cancel-project.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'act': act, 'userdet': client_details, 'order': order, 'com': com, 'tot': tot, 'can': can, 'pan': pan})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def active_project(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
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
    
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
    order = Orders.objects.select_related(
        'influencerid', 'clientid', 'orderstatus', 'serviceid').filter(clientid=user, paymentstatus=True).order_by('-ordersid')
    com = order.filter(orderstatus=1).count()
    can = order.filter(orderstatus=3).count()
    pan = order.filter(orderstatus=5).count()
    tot = order.count()

    if permissionname == 'agency_permission':

        return render(request, "active-orders.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'act': act, 'userdet': client_details, 'order': order, 'com': com, 'tot': tot, 'can': can, 'pan': pan})
    return HttpResponseRedirect("/")



@login_required(login_url='/login/')
def client_referral(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    act = request.session.get('acti', None)
    if client_details[0].country =='India' or client_details[0].country ==None:
        curs1='INR'
    else:
        curs1=client_details[0].currency  
        
        
    exrate=ExchangeRates.objects.get(countery_abbrevation=curs1).rates
    print("rated",exrate)
    ref=UserReferral.objects.get(user=user)
    succredit=float(ref.successful_referral_count*exrate)
    print('credit',succredit)
    pencredit=ref.potential_referral_count*exrate
    
    try:
        clientpayout=ClientPayout.objects.get(clientid=request.user.id)
        currency=clientpayout.currency
        if currency is None or currency =='':
            permissionname=None
                   
    except:
        permissionname=None
    
    
    if permissionname == 'agency_permission':
    
        return render(request, "referrals.html",{'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'pencredit':pencredit,'succredit':succredit,'ref':ref,'act': act,'userdet':client_details})
    elif permissionname == None:
        messages.warning(
                        request, "Please enter your country to access this page")
        return HttpResponseRedirect("/profile_setting/")
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
def orders_invoice(request,orderid=None):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
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
    

    template = 'invoice.html'
    context = {
        'pay': pay,
        'act': act,
        'userdet': client_details,
       
    }
    html = render_to_string(template, context)
    # htmltopdf(html,orderid)
    
        
    if permissionname == 'agency_permission':
        
    
        return render(request, "invoice.html",{'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'pay':pay,'act': act,'userdet':client_details})
    return HttpResponseRedirect("/")



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
def ordersdetail(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
    id = Allusers.objects.filter(id=user)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    orderid = request.session.get('ODRID')
    order_details = Orders.objects.select_related(
        'clientid', 'serviceid', 'influencerid', 'orderstatus').filter(ordersid=orderid, paymentstatus=True)
    
    
    ques=Clientinfluencerqnandans(orderid,order_details[0].influencerid.influencer_userid.id,order_details[0].serviceid.serviceid)
    
    
    paymentdet = Payments.objects.filter(ordersid=orderid)
    print("data",paymentdet)
    cltdet = AgencyProfile.objects.get(
        agency_userid=int(user))  # order_details[0].clientid.id
    act = request.session.get('acti', None)
    # print("user", user, cltdet, order_details, orderid, paymentdet)
    chtme=OrderChat.objects.filter(orderid=orderid).order_by('date')
    
    
    shrew=InfluencersReview.objects.filter(orderid=str(orderid))
    if shrew.exists():
        shrew=shrew[0]
    else:
        shrew=''
    
    
    random_review = Defaultreviews.objects.filter(serviceid=str(order_details[0].serviceid.serviceid)).order_by('?')[0]
        
    red=OrderResponse.objects.filter(orderid=orderid)
    
    if permissionname == 'agency_permission':
        #sys.stdout = open("ptdt.txt", "a")
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
                        
                        requested_currency =payments.ordersid.paymentcurrency
                        if requested_currency == 'INR':
                            
                            
                            if order_details.iscouponapplied:
                                newprice=order_details.planid.planprice-order_details.totaldiscount
                                clientpayout.remaining_balance_bank +=  newprice
                                print('execute ifeer')
                            else:
                            
                            
                                clientpayout.remaining_balance_bank += order_details.planid.planprice
                                newprice=order_details.planid.planprice
                            clientpayout.currency=requested_currency
                            clientpayout.save()
                            clientpayouthistory = ClientPayoutHistory(clientid=clientid, paymentid=payments,requested_currency=requested_currency,wallet_transaction_amount=int(newprice),isrefund_balance=True,isrefund_hold=False,remark='Order Completed')
                            clientpayouthistory.save()
                            payments.is_refunded=True
                            payments.save()
                            
                        
                        
                        
                        
                        
                        
                        Thread(target=lambda:sendagencynotification(user=request.user.id,key='agency-orderaccepted',castingcallid=None,RM_Name=None,Influencer_Name=order_details.influencerid.influencer_userid.username,Product_Name=order_details.serviceid.servicename,Decline_Reason=None,Order_Id=order_details.ordersid)).start()            
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
                    
                kycids=Allusers.objects.filter(roles='kyc')
                for i in kycids:
                    Thread(target=lambda:sendkycmanagernotification(user=i.id,key='kyc-castingcallverification',influencer_user_name=None,client_name=None)).start()
            
                send_customer_email(key='influencer-clientgivefeedback',user_email=inrew.influencerid.influencer_userid.email,
                   client=inrew.clientid.username,influencer=inrew.influencerid.influencer_userid.username,order_id=None,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)   
            return redirect(request.META['HTTP_REFERER'])
        return render(request, "Orders-details.html", {'random_review':random_review,'shrew':shrew,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'ques':ques,'userdet':client_details,'order': order_details, 'pymethod': paymentdet, 'cli': cltdet, 'act': act,'chtme':chtme,'res':red})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def setting(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
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
    cltdet = AgencyProfile.objects.select_related('agency_userid').filter(
        agency_userid=int(user))
    orid = Orders.objects.filter(clientid=str(user),paymentstatus=True).last()
    logs = LoginIP.objects.filter(
        userid=user).order_by('-LoginIPid')[0:3]
    act = request.session.get('acti', None)
    
    exch=ExchangeRates.objects.all().order_by('country')
    langes=Languages.objects.all()
    
    docs=UnverifedAgencyDetails.objects.filter(clientid=str(user))
    if docs.exists():
        docs=docs[0]
    else:
        docs=''
    
    if cltdet[0].country is None or cltdet[0].country =='':
        messages.warning(
                        request, "Please, update your profile details and country.")
    
    
    if permissionname == 'agency_permission':
        # sys.stdout = open("ptdt.txt", "a")
        if request.method == 'POST':
            print('resdf',request.POST)
            
            
            
            if "OTP" in request.POST:
                comOTP = request.POST.get("OTP")
                
                emailotp = request.session.get('emailotp', None)
                emailverify = request.session.get('emailverify', None)
                
                if comOTP == emailotp:
                    if emailverify is not None and len(emailverify) > 0  :
                        
                        id.email = emailverify
                        id.save(update_fields=['email'])
                        emaset=AgencySettings.objects.get(asettingsuserid=user)
                        emaset.email_verified=True
                        emaset.save()
                
                else:
                    messages.warning(
                        request, "OTP mismtached, please enter correct otp!...")
                        
                        
                        
                        
                        
            
            
            if 'profile_phone' in request.POST:

                profile_phone = request.POST.get('profile_phone')

                print("profile", profile_phone)
                pclnt = AgencyProfile.objects.get(agency_userid=str(user))
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
                    
                    
                    
            elif 'changeskycdoc'  in request.POST:
                print('rahul')
                gstcertificate=request.FILES.get('gstcertificate')
                incomecertificate=request.FILES.get('incomecertificate')
                companyname=request.POST.get('companyname')
                emailaddress=request.POST.get('emailaddress1')
                websitelink=request.POST.get('websitelink')
                if docs:
                    if emailaddress:
                        docs.email=emailaddress
                        docs.save(update_fields=['email'])
                        
                    if websitelink:
                        docs.link=websitelink
                        docs.save(update_fields=['link'])   
                        
                    if gstcertificate:
                        docs.gstcertificate=gstcertificate
                        docs.save(update_fields=['gstcertificate'])
                        
                    if incomecertificate:
                        docs.itrcertficate=incomecertificate
                        docs.save(update_fields=['itrcertficate'])
                    if companyname:
                        docs.comapanyname=companyname
                        docs.save(update_fields=['comapanyname'])           
                    
                    print('upadte docs')

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
                

                pclnt = AgencyProfile.objects.get(agency_userid=str(user))
                
                if pclnt.country is None or pclnt.country == '':
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
                        
                        clientpayout, created = ClientPayout.objects.get_or_create(clientid=cltdet[0].agency_userid, defaults={
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

                if emailaddress is not None and len(emailaddress) > 0:
                    checkmail=Allusers.objects.filter(email=emailaddress)
                    if checkmail.exists():
                        messages.warning(
                        request, "This email is already used. Choose another one.")
                    else:
                        id.email = emailaddress
                        id.save(update_fields=['email'])
                    print("up email id")
                pclnt.save()

                print("api", image, name, emailaddress, phone,
                      country, language, timezone, pin, address)

        #sys.stdout.close()
        return render(request, "settings.html", {'docs':docs,'langes':langes,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'exch':exch,'act': act, 'cltdet': cltdet, "orid": orid, 'log': logs, 'userdet': cltdet})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def pitching_detail(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
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
    

    infoid = request.session.get('pitchinfoid')
    pitchid = request.session.get('pitchid')
    callid = request.session.get('callid')

    call = Casting_Call.objects.get(castingcallid=callid)
    pitch = PitchingCastingCall.objects.get(pitchingCastingCallid=pitchid)
    infl = InfluencerProfile.objects.get(influencer_userid=infoid)
    email = Allusers.objects.get(id=infoid).email

    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
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
                    sendInfluencernotification(user=pt.influencerid.influencer_userid.id,key='influencer-castingcallpitchdeclined',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=pt.castingcallid.castingcallid,reason=None)
                    
                    print("not approved")
                    
                    
            acce = request.POST.get("acceptorder")
            if acce is not None:
                pt = PitchingCastingCall.objects.filter(
                    pitchingCastingCallid=acce)
                if pt.exists():
                    pt = pt[0]
                    pt.approved = True
                    pt.save(update_fields=['approved'])
                    
                    sendInfluencernotification(user=pt.influencerid.influencer_userid.id,key='influencer-castingcallpitchapproved',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=pt.castingcallid.castingcallid,reason=None)
                    print("update approved")
                    
            print("cancel", canel)
            print("accep", acce)
            return redirect(request.META['HTTP_REFERER'])

        print("Infoid", infoid, pitchid, callid)
        #sys.stdout.close()
        return render(request, "pitching-details.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'call': call, 'pitch': pitch, 'info': infl, 'email': email, 'userdet': client_details, 'act': act})
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def view_casting_call_pitching(request):
    user = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
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
    #sys.stdout = open("=ptcasting.txt", "a")
    print("user", user)
    use = Casting_Call.objects.filter(clientid=user)
    print("data1", use)
    ptdata = []
    for i in use:
        ptdat = PitchingCastingCall.objects.filter(
            castingcallid=int(i.castingcallid))
        for j in ptdat:
            pro = InfluencerProfile.objects.get(
                influencer_userid=str(j.influencerid))
            usnem=Allusers.objects.get(id=str(j.influencerid))
            tp = ()
            tp = tp+(j,)
            tp = tp+(str(i.posttitle),)
            tp = tp+(str(pro.fullname),)
            tp = tp+(str(pro.profileimage),)
            tp = tp+(str(usnem.username),)
            ptdata.append(tp)

    print("data2", ptdata, type(ptdata))
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)

    #sys.stdout.close()
    if permissionname == 'agency_permission':

        return render(request, "casting-call-details.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'act': act, 'ptdata': ptdata, 'userdet': client_details})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def castingcall(request):
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    cls = id
    cate1 = CastingCallCategories.objects.all()
    
    plat=Platforms.objects.all()
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=userid)
    act = request.session.get('acti', None)
    
    if request.method == "POST":
        posttiltle = request.POST.get("posttiltle")
        brandlogo = request.FILES.get("brandlogo")
        bandbanner = request.FILES.get("bandbanner")
        productimage = request.FILES.get("productimage")
        brandname = request.POST.get("brandname")
        requiredplat = request.POST.get("requiredplat")
        start_date = request.POST.get("start_date")
        compensation = request.POST.get("compensation")
        postdes = request.POST.get("postdes")

        categpryid = request.POST.get("categpryid")
        keywords = request.POST.get("keywords")

        ques = dict(request.POST)
        title = list(ques["fname"])
        des = list(ques["lname"])
        countr=list(ques["country"])

        castingcatid = CastingCallCategories.objects.filter(
            castingcallcategorieid=categpryid)
        if castingcatid.exists():
            castingcatid = castingcatid[0]

        cc=Casting_Call.objects.filter(posttitle=posttiltle)
        if cc.exists():
            messages.warning(
                        request, 'The casting call title is already available, choose another one.')
            
        else:

            cc = Casting_Call(allcountry=countr,clientid=cls, postkeyword=keywords, brandlogo=brandlogo, brandbanner=bandbanner, productimage=productimage, posttitle=posttiltle,
                            brandname=brandname, requiredplatform=requiredplat, compensation=compensation, postdescription=(postdes), categoryid=castingcatid, expirydate=start_date)
            cc.save()
            
            
            kycids=Allusers.objects.filter(roles='kyc')
            for i in kycids:
                sendkycmanagernotification(user=i.id,key='kyc-castingcallverification',influencer_user_name=None,client_name=None)
            
            Thread(target=lambda:sendagencynotification(user=request.user.id,key='agency-castingcallsubmission',castingcallid=None,RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=None)).start()        

        
            send_customer_email(key='agency-castingcallsubmitted',user_email=request.user.email,
                   client=request.user.username,influencer=None,order_id=None,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=cc.castingcallid,brief_pitch=None,decline_reson=None) 
                        
                
    

            cc1 = Casting_Call.objects.filter(castingcallid=cc.castingcallid)
            if cc1.exists():
                cc1 = cc1[0]

            for i in range(0, len(title)):
                ccqn = Callcastingquestions(
                    callcastid=cc1, title=title[i], des=des[i], clientid=cls)
                ccqn.save()


            messages.success(
                        request, 'Your casting call is submitted. After approval, it shows on our platform.') 
        # return redirect(request.META['HTTP_REFERER'])
                   
         
    
    return render(request, "casting-call.html", {'platform':plat,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'act': act, 'cat': cate1, 'userdet': client_details})


@login_required(login_url='/login/')
def totalcastingcall(request):
    sys.stdout = open("totalcalling.txt", "a")
    userid = request.user.id
    try:
        channel_name = single_chat.objects.filter(user=userid, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid
      
        rmname = rmid
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    result1 = Casting_Call.objects.select_related('categoryid').annotate(
        categoryname=F('categoryid__categoryname')
    ).filter(clientid=userid).order_by('-castingcallid').values('categoryname', 'castingcallid', 'brandlogo', 'brandbanner', 'productimage', 'posttitle', 'approvedby', 'creationdate', 'cardcolor', 'approved', 'expirydate', 'brandname', 'postdescription', 'requiredplatform', 'compensation')
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=userid)
    act = request.session.get('acti', None)
    callcate=CastingCallCategories.objects.all()
    callpat=Platforms.objects.all()
    
    if request.method == "POST":
        
        if "ccid1" in request.POST:
            postid = request.POST.get("ccid1")
            calqn=Callcastingquestions.objects.filter(callcastid=postid)
            calqn.delete()
            caldel = Casting_Call.objects.get(castingcallid=postid)
            caldel.delete()
        
        if "changeapproved" in request.POST:
            # print("data",request.POST)
            
            postid = request.POST.get("changeapproved")
            caldel = Casting_Call.objects.get(castingcallid=postid)

            # Check and update fields only if they are not blank
            productimage = request.FILES.get("productimage")
            if productimage:
                caldel.productimage = productimage

            bannerimage = request.FILES.get("bannerimage")
            if bannerimage:
                caldel.brandbanner = bannerimage

            brandimage = request.FILES.get("brandimage")
            if brandimage:
                print('brand',brandimage)
                caldel.brandlogo = brandimage
                print('change brandlogo')

            brandname = request.POST.get("brandname")
            if brandname:
                caldel.brandname = brandname

            postcategory = request.POST.get("postcategory")
            if postcategory:
                caldel.categoryid = CastingCallCategories.objects.get(castingcallcategorieid=postcategory)

            postkeywords = request.POST.get("postkeywords")
            if postkeywords:
                caldel.postkeyword = postkeywords

            expirydte = request.POST.get("expirydte")
            if expirydte:
                caldel.expirydate = expirydte

            platformdet = request.POST.get("platformdet")
            if platformdet:
                caldel.requiredplatform = platformdet

            compensat = request.POST.get("compensat")
            if compensat:
                caldel.compensation = compensat

            posttitle = request.POST.get("posttitle")
            if posttitle:
                caldel.posttitle = posttitle

            postdescription = request.POST.get("postdescription")
            if postdescription:
                caldel.postdescription = postdescription

            caldel.save()
            # print('chnges successfuly')/
            
            frontlist = request.POST
            country=frontlist.getlist('country')

            if len(country) >0:
                caldel.country=country
            caldel.save()
            
            
            
            
            list1=frontlist.getlist('question-text')
            lust2=frontlist.getlist('answer-text')
           
            # print(list1,type(list1))
            if len(list1) > 0 and len(lust2) > 0:
                calqn=Callcastingquestions.objects.filter(callcastid=postid)
                calqn.delete()
                for a, b in zip_longest(list1,lust2):
                    # print(a, b)
                    savecallqn=Callcastingquestions()
                    savecallqn.callcastid=Casting_Call.objects.get(castingcallid=postid)
                    savecallqn.clientid=Allusers.objects.get(id=str(request.user.id))
                    if a is not None:
                        savecallqn.title=a
                    if b is not None:
                        savecallqn.des=b
                    savecallqn.save()
                    # print('save')

    #sys.stdout.close()
    return render(request, "total-casting-call.html", {'callpat':callpat,'callcate':callcate,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'act': act, 'det': result1, 'userdet': client_details})


@login_required(login_url='/login/')
def my_wishlist(request):
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
      
        rmname = rmid
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
    wh=Wishlist.objects.filter(clientid=str(user.id))
    t1=[]
    for i in wh:
        info=InfluencerProfile.objects.get(influencer_userid=str(i.influencerid))
        t=(info.profileimage,info.influencer_userid.username,info.fullname,Shortdescription.objects.get(
                        shortdescriptionid=info.short_description).shortdestext,info.currency,)
        pri=PricingPlans.objects.get(usersid=str(i.influencerid),plan_type='Basic',serviceid=1).increasedprice
        t=t+(str(pri),i.wishlistid)
        t1.append(t)
    return render(request, "wishlist.html",{'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'wh':t1,'userdet': client_details})

@login_required(login_url='/login/')
def agencymycart(request):
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
      
        rmname = rmid
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
    wh=Cart.objects.filter(clientid=str(user.id))
    t1=[]
    for i in wh:
        info=InfluencerProfile.objects.get(influencer_userid=str(i.influencerid))
        t=(info.profileimage,info.influencer_userid.username,info.fullname,Shortdescription.objects.get(
                        shortdescriptionid=info.short_description).shortdestext,info.currency,)
        pri=PricingPlans.objects.get(usersid=str(i.influencerid),plan_type='Basic',serviceid=1).increasedprice
        t=t+(str(pri),i.Cartid)
        t1.append(t)
    return render(request, "mycart.html",{'rmnmae':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'wh':t1,'userdet': client_details})



@login_required(login_url='/login/')
def blogs_home_user(request, cate=None):
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
      
        rmname = rmid
        image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
    blog = Blog.objects.all()
    act = request.session.get('acti', None)
    if cate is not None:
        blog = Blog.objects.filter(blog_categories__icontains=cate)

    return render(request, "bloghome.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'act': act, "allblog": blog, 'userdet': client_details})

@login_required(login_url='/login/')
def blogs_post_user(request, name):
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
      
        rmname = rmid
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
    client_details = AgencyProfile.objects.select_related(
        'agency_userid').filter(agency_userid=user)
    return render(request, "blogdetails.html", {'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'content':content,'det': bldet, "blogdeatils": blog, 'comm': bl, 'rc': blog1, 'num': num, 'cate': bcate, 'link': base_url, 'userdet': client_details, 'act': act})


logger = logging.getLogger()
fh = logging.FileHandler('Agency_view_log.txt')
logger.addHandler(fh)


def check_title(request):
    title = request.GET.get('title', None)
    response = {
        'is_taken': Casting_Call.objects.filter(posttitle__iexact=title).exists()
    }
    return JsonResponse(response)