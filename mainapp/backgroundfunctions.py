
from django.db.models import Max
from django.utils import timezone
from mainapp.models import *
from django.shortcuts import  HttpResponse,redirect
from pushnotificationapp.models import *
from inappnotifications.models import *
from Creator.models import *
import sys
from django.db.models import Count, F, Case, When, DateTimeField
from datetime import datetime, timedelta
from threading import Thread
from agora_chat.models import *
from Account.models import *
from emil_send.views import existing_user
from inappnotifications.views import send_customer_email,sendusernotification,sendInfluencernotification,sendagencynotification,sendRMnotification



def Sendperdaytransactions():
    
    ordrpur=Payments.objects.all().order_by('-paymentsid')
    
    
    
    pass
    



















def errortesting():
    print('errortesting here0')
    x=1/0
    print('errortesting here1',x)

def videoslotpushnotification():
    current_date = timezone.now().date()

    # Annotate the maximum 'endtime' for each 'influencerid'
    from django.db.models import Subquery, OuterRef

    latest_subslots = Subslots.objects.filter(
        influencerid=OuterRef('influencerid')
    ).order_by('-endtime').values('endtime')[:1]

    influencers_with_latest_endtime = Subslots.objects.annotate(
        latest_endtime=Subquery(latest_subslots)
    ).values('influencerid', 'latest_endtime').distinct()

    # Filter those having 'latest_endtime' equal to the current date
    filtered_influencers = influencers_with_latest_endtime.filter(
        latest_endtime__date=current_date
    )

    # Extract influencerids
    filtered_influencer_ids = [entry['influencerid'] for entry in filtered_influencers]
    
    # filtered_influencer_ids.append(103848)
    
    if len(filtered_influencer_ids)>0:
        for i in filtered_influencer_ids:
            user=Allusers.objects.get(id=str(i))
            icon="""
            <span class="symbol-label bg-light-warning">
                <!--begin::Svg Icon | path: icons/duotune/finance/fin006.svg-->
                    <span class="svg-icon svg-icon-2 svg-icon-warning">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path opacity="0.3" d="M20 15H4C2.9 15 2 14.1 2 13V7C2 6.4 2.4 6 3 6H21C21.6 6 22 6.4 22 7V13C22 14.1 21.1 15 20 15ZM13 12H11C10.5 12 10 12.4 10 13V16C10 16.5 10.4 17 11 17H13C13.6 17 14 16.6 14 16V13C14 12.4 13.6 12 13 12Z" fill="currentColor"></path>
                        <path d="M14 6V5H10V6H8V5C8 3.9 8.9 3 10 3H14C15.1 3 16 3.9 16 5V6H14ZM20 15H14V16C14 16.6 13.5 17 13 17H11C10.5 17 10 16.6 10 16V15H4C3.6 15 3.3 14.9 3 14.7V18C3 19.1 3.9 20 5 20H19C20.1 20 21 19.1 21 18V14.7C20.7 14.9 20.4 15 20 15Z" fill="currentColor"></path>
                        </svg>
                    </span>
                <!--end::Svg Icon-->
            </span>"""
            
            title="Please add slot for video chat service!"
            
            availnoti = notification.objects.filter(title=title, user=str(i))
            if availnoti.exists():
                last_noti = availnoti.latest('timestamp')  # Get the latest notification
                current_time = timezone.now()  # Use timezone-aware datetime
                time_difference = current_time - last_noti.timestamp
                if time_difference > timedelta(days=1):
                    infosend = notification(
                        title=title,
                        message="Slot of your video chat service is till date only so if you want to provide video chat service then please add video chat slot.",
                        user=user,
                        redirect_link='Service-Plan',
                        icon=icon
                    )
                    infosend.save()
            else:
                infosend=notification(title=title,message="Slot of your video chat service is till date only so if you want to provide video chat service then please add video chat slot.",user=user,redirect_link='Service-Plan',icon=icon)
                infosend.save()
    
    
    print('influecnerid',filtered_influencer_ids)
    # return None
    return HttpResponse(f'execute: {filtered_influencer_ids}')


import re

email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

def is_valid_email(email):
    return re.match(email_pattern, email) is not None


def notifyforprofileupdation(request):
    current_date = timezone.now().date()
    sys.stdout = open("aaaaaaa.txt", "a")
    

 
    filled_fields_condition = (
    ~Q(country='')
    | ~Q(state='')
    | ~Q(city='')
    | ~Q(mobile=None)  # Check for 'mobile' being None
    | ~Q(address='')
    | ~Q(fullname='')
    | ~Q(desc_title='')
    | ~Q(language__len=0)
    | ~Q(categories__len=0)
    | ~Q(profileimage='')
    | ~Q(profileimage1='')
    | ~Q(platformdetails__len=0)
    | ~Q(currency='')
    | ~Q(services__len=0)
)

# Query the InfluencerProfile model with the combined conditions
    influencers_with_filled_fields = InfluencerProfile.objects.filter(
    filled_fields_condition,
    influencer_userid__isnull=False,
    influencer_userid__influencersettings__kyc=False
)
    
    print('date',influencers_with_filled_fields.count())

    # Extract influencerids
    # filtered_influencer_ids = [influencers_with_filled_fields]
    
    # filtered_influencer_ids.append(103848)
    execute=[]
    
    if len(influencers_with_filled_fields)>0:
        for i in influencers_with_filled_fields:
            id=i.influencer_userid.id
            print('email',i.influencer_userid.email)
            email=i.influencer_userid.email
            
            user=Allusers.objects.get(id=str(id))
            print('users',user)
            
            sendInfluencernotification(user=user.id,key='influencer-profileupdate',RM_Name=None,Influencer_Name=user.username,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None)
            print('first thread')
            if user.email:
                print('outer',is_valid_email(email))
                if is_valid_email(email):
                    print('innier',is_valid_email(email))
                    execute.append(email)

                    
                    send_customer_email(key='influencer-influencerprofileupdate',user_email=user.email,client=None,influencer=user.username,order_id=None,service_type=None,order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None,pward=None,otp=None)
                    
                    print('Second thread')
    
    return HttpResponse(f'execute: {execute}')


#This fucntion is also run at once time.
def topcreator(request):
        
    completed_orders = Orders.objects.filter(paymentstatus=True, orderstatus=1)
    order_counts = completed_orders.values('influencerid').annotate(order_count=Count('ordersid'))
    
    for i in order_counts:
        print(i['influencerid'])
        print(i['order_count'])
        if i['order_count'] > 15:
            top=Topinfluencer.objects.filter(influencerid=str(i['influencerid']))
            if top.exists():
                top=top[0]
                top.ordercompleteioncount=int(i['order_count'])
                top.save(update_fields=['ordercompleteioncount'])
                print('upadte det')
            else:
                top=Topinfluencer()
                top.influencerid=InfluencerSettings.objects.filter(influencer_userid=str(i['influencerid']))[0]
                top.ordercompleteioncount=int(i['order_count'])
                top.save()      
                print('save det')  
      
    # return HttpResponse(f'execute: {order_counts}')
    return redirect(request.META['HTTP_REFERER'])



def topcreator1():
        
    completed_orders = Orders.objects.filter(paymentstatus=True, orderstatus=1)
    order_counts = completed_orders.values('influencerid').annotate(order_count=Count('ordersid'))
    
    for i in order_counts:
        print(i['influencerid'])
        print(i['order_count'])
        if i['order_count'] > 15:
            top=Topinfluencer.objects.filter(influencerid=str(i['influencerid']))
            if top.exists():
                top=top[0]
                top.ordercompleteioncount=int(i['order_count'])
                top.save(update_fields=['ordercompleteioncount'])
                print('upadte det')
            else:
                top=Topinfluencer()
                top.influencerid=InfluencerSettings.objects.filter(influencer_userid=str(i['influencerid']))[0]
                top.ordercompleteioncount=int(i['order_count'])
                top.save()      
                print('save det')  
      
    # return HttpResponse(f'execute: {order_counts}')
    return None
    



#This fucntion will be run at one time
def monitoranupdateorderstatus():
    
    
    three_days_ago = timezone.now() - timedelta(days=4)

    # Query to retrieve the desired orders
    orders = Orders.objects.filter(
    paymentstatus=True,
    orderstatus=5,
    orderdate__lte=three_days_ago,
)
    print('query',orders.query)
    print('data',orders)

    # You can iterate through the 'orders' queryset to access the results
    for i in orders:

        orderid=str(i.ordersid)
        userid=i.influencerid
        ac = InfluencerProfile.objects.get(influencer_userid=str(userid))
        reason = 'Concerned Influencer was taking too much time to accept this order. So, this order has been cancelled.'
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
            
            # print('cancel reason', i.ordersid)
            
            ctus=chat_user.objects.filter(orderid=orderid).exclude(RM=True)
            if ctus.exists:
                for i in ctus:
                    i.channel_status=False
                    i.save(update_fields=['channel_status'])
                    print('cancel chat', i.orderid)
            
            clientid=ordid.clientid
            clientpayout, created = ClientPayout.objects.get_or_create(clientid=clientid, defaults={
                'remaining_balance_bank':0, 'successful_withdrawal_bank':0, 'hold_bank':0,
              
                })
            
            try:
            
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
                    
                    clientpayouthistory = ClientPayoutHistory(clientid=clientid, 
paymentid=payments,requested_currency=requested_currency,wallet_transaction_amount=int(newprice),isrefund_balance=True,isrefund_hold=False,remark='Cancel Order Refund')
                    clientpayouthistory.save()
                    payments.is_refunded=True
                    payments.save()
                    # print('refud', i.ordersid)
                    
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
                # print('mail send', i.ordersid)
            except:
                pass    
                
        # print('execute', i.ordersid)
        # break
    
    # order_counts='Rahul'
    return None
    
    # return HttpResponse(f'execute: {order_counts}')



def monitoranusenddelaywarning():
    # sys.stdout = open("aaaaaaa.txt", "a")
        # Calculate the sum of orderdate and deliverytime for each order with orderdescription 'Exclusive service not acquired'
    
    delivery_time_expr = Case(
    When(orderdescription='Exclusive service not acquired', then=F('planid__deliverytime')),
    When(orderdescription='Exclusive service acquired', then=F('planid__exclusivedeliverytime')),
    output_field=DateTimeField()
)

    # Calculate the delivery time for each order
    delivery_time = F('orderdate') + delivery_time_expr 

    # Query to retrieve the desired orders
    orders = Orders.objects.filter(
        paymentstatus=True,
        orderstatus=6,
        orderdate__lte=delivery_time
    )
    print('query',orders.query)
    print('data',orders)
    
    
    # You can iterate through the 'orders' queryset to access the results
    for i in orders:
        # print('execute', i.ordersid)
        

        orderid=str(i.ordersid)
        ordid = Orders.objects.filter(ordersid=orderid)[0]
 
          
        send_customer_email(key='influencer-influencerdelayingorder',user_email=ordid.influencerid.influencer_userid.email,
        client=ordid.clientid.username,influencer=ordid.influencerid.influencer_userid.username,order_id=ordid.ordersid,service_type=None,
        order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None)   
        
        sendInfluencernotification(user=ordid.influencerid.influencer_userid.id,key='influencer-influencerdelayingorder',RM_Name=None,Influencer_Name=ordid.influencerid.influencer_userid.username,Product_Name=None,Decline_Reason=None,Order_Id=ordid.ordersid,reason=None)
        
            
        Thread(target=lambda:sendRMnotification(key='rm-influencerdelayingorder',RM_Name=None,client_type=None,client_Name=ordid.clientid.username,rmid=ordid.rmid,Influencer_Name=ordid.influencerid.influencer_userid.username,Order_ID=ordid.ordersid,reason=None,Order_Stage=None)).start()
        # print('sendmai', i.ordersid)
        
        # break
    
    # order_counts='Rahul'
    return None
        
    
    # return HttpResponse(f'execute: {order_counts}')
