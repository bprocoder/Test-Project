import logging
import stripe
from threading import Thread
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.sessions.models import Session
import sys
from inappnotifications.views import *
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from mainapp.enanddc import encrypt, decrypt
import json
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from django.shortcuts import redirect
import os
import json
from django.db.models import Q, F
# from django.urls import reverse
# from django.core.signing import Signer
from mainapp.models import *
from Account.models import *
from mainapp.views import get_timezone
from emil_send.views import existing_user



stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'https://www.influencerhiring.com'

# home view


def homepage(request):
    return render(request, 'checkout.html')

# success view

import requests
def success(request):
    # utm_source="fff"
    sys.stdout = open("infocat.txt", "a")
    
    utm_source=request.session.get('utm_source')
    affiliate_id=request.session.get('affiliate_id')
    print('Trying to send webhook . . . ')
    print("utm_source : ",utm_source, "affiliate_id : ",affiliate_id)
    if utm_source == 'tradingbot':  
        # request.session['utm_source'] = utm_source
        # request.session['affiliate_id'] = affiliate_id 
        # utm_source=request.session.get('utm_source')
        # affiliate_id = request.session.get('affiliate_id')
        webhookdata = {
            'utm_source': utm_source,
            'affiliate_id': affiliate_id
        }
        print('sending webhookdata ...',webhookdata)
        requests.post(url='http://trading.24x7bot.com/webhook1/', data=json.dumps(webhookdata))
        del request.session['utm_source']
        del request.session['affiliate_id']
    else:
        print(" utm_source is not 'tradingbot'")
    return render(request, 'success.html')

# cancel view



def success1(request):
    # walletid = request.session.get('walletid')
    # if walletid is not None:
    #     payt=ClientPayout.objects.get(payoutid=walletid)
    #     amt=request.session.get('amt')
    #     if amt >= payt.remaining_balance_bank:
    #         payt.remaining_balance_bank=-amt
    #         payt.save()
    
    pur_ordid = request.session.get('pur_ordid', None)
    trans_id = request.session.get('trans_id', None)
    
    orde_amt = request.session.get('orde_amt', None)

    order_date = request.session.get('order_date', None)

    influencer_name = request.session.get('influencer_name', None)

   
   
    return render(request, 'success1.html',{'influencer_name':influencer_name,'order_date':order_date,'orde_amt':orde_amt,'pur_ordid':pur_ordid,'trans_id':trans_id})






def cancel(request):
    return render(request, 'cancel.html')


# value = 'my-sensitive-value'
# signer = Signer()
# signed_value = signer.sign(value)
# url = reverse('test') + f'?value={signed_value}'

# def test(request):
#     signed_value = request.GET.get('value', '')
#     signer = Signer()

#     try:
#         # Verify the signed value
#         value = signer.unsign(signed_value)
#     except (BadSignature, SignatureExpired):
#         # Handle the case where the value is invalid or has expired
#         value = None

#     data = {'value':value }
#     data = json.dumps(data, default=str)
#     return HttpResponse(data, content_type="application/json")

@csrf_exempt
def paymentslip(request, email2, amount, curr, orid):
    # def paymentslip(request):
    cursor = connection.cursor()
    sys.stdout = open("payslip.txt", "a")
    clientid = request.user.id
    print("Clientid", clientid)
    # email1=Allusers.objects.get(id=clientid).email
    email1 = Allusers.objects.filter(id=clientid)
    if email1.exists():
        email1 = email1[0]
    print("Rahul")
    email = ['Rahul.Barawal@bol7.com', 'Naveen.Singh@bol7.com', email1, email2]
    # curr='inr'
    # orid=645
    # amount=1000
    cursor.execute('''
        SELECT s.servicename, i.fullname, mo.taxamt, mo.taxpercentage
        FROM mainapp_orders AS mo
        JOIN mainapp_services AS s ON s.serviceid = mo.serviceid
        JOIN mainapp_payments AS mp ON mp.ordersid = mo.ordersid
        JOIN mainapp_influencerprofile AS i ON i.influencer_userid = mo.influencerid
        WHERE mo.ordersid =(%s);
    ''', [orid])
    dat = cursor.fetchall()
    print("execute", dat)
    servicename = dat[0][0]
    influname = dat[0][1]
    taxamt = dat[0][2]
    taxper = dat[0][3]

    # Yeh Hatana Hai
    if taxper is None:
        taxper = 18
    if taxamt is None:
        taxamt = amount*.18
    # Yha tak hatana hai
    cursor.close()
    print("Data", servicename, influname, taxamt, taxper)
    orid = encrypt(orid)
    html_con = render_to_string("Influencer-Admin/order-mail.html", {'servicename': servicename, 'name': influname,
                                'taxamt': taxamt, 'taxper': taxper, 'curr': curr, 'amount': amount, 'orid': orid}, request=request)
    text = strip_tags(html_con)

    data = {
        'subject': 'Confirming Mail For Your Placed Order:',
        'body': text,
        'to_email': email[2],
        'to_email1': email[3],
    }
    mwg = EmailMultiAlternatives(
        subject=data['subject'],
        body=data['body'],
        from_email='admin@influencerhiring.com',
        to=[data['to_email'], data['to_email1']]
    )
    mwg.attach_alternative(html_con, "text/html")
    # img_dir=r'C:\Users\BOL7\Desktop\Influencer\mainapp\static'
    img_dir = str(settings.BASE_DIR)+'\mainapp\static'
    img_dir = r'{}'.format(img_dir)
    image = "influencerhiring.png"
    file_path = os.path.join(img_dir, image)
    with open(file_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header(
            'Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition',
                       'inline', filename=image)
    mwg.attach(img)
    image1 = "pay.png"
    file_path = os.path.join(img_dir, image1)
    with open(file_path, 'rb') as f:
        imag1 = MIMEImage(f.read())
        imag1.add_header('Content-ID', '<{name}>'.format(name=image1))
        imag1.add_header('Content-Disposition', 'inline', filename=image1)
    mwg.attach(imag1)
    mwg.send()
    print("execute all function")
    return HttpResponse('You have successfully placed order.', status=200)


@csrf_exempt
def create_checkout_session(request):
    sys.stdout = open("basicpayment.txt", "a")
    currentuser = request.user.id
    data = request.body
    ccode = request.session.get('coup')
    # print("Couponcode", ccode)
    cursor = connection.cursor()
    data = json.loads(data.decode())
    infoid = data['infoid']
    bserviceid = data['bserviceid']
    bplanid = data['bplanid']
    othercharges = data['othercharges'][4:]
    
    
    
    walletid=data['walletid']
    
    
    if walletid !=0:
        print("postdata1",request.body,walletid,type(walletid))

        request.session['walletid'] = data['walletid']
        payt=ClientPayout.objects.get(payoutid=walletid)
    
    
    
    
    print("postdata",request.body)
    
    ordes=None

    if bserviceid=='5' or bserviceid==5:
        serimg="https://www.influencerhiring.com/media/influacq.jpg"
        eventname = data['eventname']
        eventdate = data['eventdate']
        eventtype = data['eventtype']
        timefrom = data['timefrom']
        timeto = data['timeto']
        address = data['address']
        description = data['description']
        clienttimezone=get_timezone(request)

        print(eventname,eventdate,eventtype,timefrom,timeto,address,description,clienttimezone)

        if othercharges == '0' or othercharges == ' 0':
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placeinfluenceracquisitionorders(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, ccode,eventname,eventdate,eventtype,timefrom,timeto,address,description,clienttimezone])
                print("1",cursor.query)
                request.session['coup'] = ''
                order = cursor.fetchall()
                amount = order[0][8]

            else:
                cursor.execute('select * from placeinfluenceracquisitionorders(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, ccode,eventname,eventdate,eventtype,timefrom,timeto,address,description,clienttimezone])
                print("2",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
                # print("template chagres.")
        else:
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placeinfluenceracquisitionorders(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, ccode,eventname,eventdate,eventtype,timefrom,timeto,address,description,clienttimezone])
                print("3",cursor.query)
                request.session['coup'] = ''
                order = cursor.fetchall()
                amount = order[0][8]

            else:
                cursor.execute('select * from placeinfluenceracquisitionorders(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, ccode,eventname,eventdate,eventtype,timefrom,timeto,address,description,clienttimezone])
                print("4",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
                # print("template chagres.")
        ordes=order[0][10]
        orderid = order[0][4]
        currcode = order[0][5]
        sername = order[0][6]
        amout = amount*100
        # print("execute")
        
        
        if walletid != 0:
            if amout >= payt.remaining_balance_bank:
                amout=amout-(payt.remaining_balance_bank*100)
                payt.is_wallet_used_with_payment_gateway=True
                payt.save()
            amout=int(amout)
            print('waalet id execute',walletid)
        

        if currcode is None:
            currcode = 'inr'
        session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
              shipping_options=[
                {
                    "shipping_rate_data":{
                        "type":"fixed_amount",
                        "fixed_amount":{
                            "amount":0,"currency":currcode
                        },
                        "display_name":"`",
                        "delivery_estimate":{
                            # "minimum":{
                            #     "unit":"business_day","value":1
                            # },
                            "maximum":{
                                "unit":"business_day","value":1
                            },
                        },
                    },
                },
            ],
            line_items=[{
                'price_data': {
                    'currency': currcode,
                    'product_data': {
                        'name': sername,
                        'description':ordes,
                        "images":[serimg],
                    },
                    'unit_amount': amout,
                },
                'quantity': 1,
            }],
            metadata={
                "order_id": orderid
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            consent_collection={
                'terms_of_service':'required',
                },
        )
        
        # print(session)
        return JsonResponse({'id': session.id})
    
    
    
    
    
    
    if 'tempid' in data and 'temptext' in data:
        # print("tempid",data['tempid'])
        serimg="https://www.influencerhiring.com/media/Videogreetings.jpg"
        if othercharges == '0' or othercharges == ' 0':
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, ccode,data['tempid'],data['temptext']])
                print("1",cursor.query)
                request.session['coup'] = ''
                order = cursor.fetchall()
                amount = order[0][8]

            else:
                cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, ccode,data['tempid'],data['temptext']])
                print("2",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
                # print("template chagres.")
        else:
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, ccode,data['tempid'],data['temptext']])
                print("1",cursor.query)
                request.session['coup'] = ''
                order = cursor.fetchall()
                amount = order[0][8]

            else:
                cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, ccode,data['tempid'],data['temptext']])
                print("2",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
                # print("template chagres.")
        ordes=order[0][10]
        orderid = order[0][4]
        currcode = order[0][5]
        sername = order[0][6]
        amout = amount*100
        # print("execute")
        if walletid != 0:
            if amout >= payt.remaining_balance_bank:
                amout=amout-(payt.remaining_balance_bank*100)
                payt.is_wallet_used_with_payment_gateway=True
                payt.save()
            amout=int(amout)
            print('waalet id execute',walletid)

        if currcode is None:
            currcode = 'inr'
        session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
              shipping_options=[
                {
                    "shipping_rate_data":{
                        "type":"fixed_amount",
                        "fixed_amount":{
                            "amount":0,"currency":currcode
                        },
                        "display_name":"`",
                        "delivery_estimate":{
                            # "minimum":{
                            #     "unit":"business_day","value":1
                            # },
                            "maximum":{
                                "unit":"business_day","value":1
                            },
                        },
                    },
                },
            ],
            line_items=[{
                'price_data': {
                    'currency': currcode,
                    'product_data': {
                        'name': sername,
                        'description':ordes,
                        "images":[serimg],
                    },
                    'unit_amount': amout,
                },
                'quantity': 1,
            }],
            metadata={
                "order_id": orderid
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            consent_collection={
                'terms_of_service':'required',
                },
        )
        
        # print(session)
        return JsonResponse({'id': session.id})
    

    if 'subslotid' in data:
        # print("myvar",data['subslotid'])
        serimg="https://www.influencerhiring.com/media/videochat.jpg"
        if othercharges == '0' or othercharges == ' 0':
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, True, ccode,data['subslotid']])
                print("1",cursor.query)
                request.session['coup'] = ''
                order = cursor.fetchall()
                amount = order[0][8]
            else:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, False, ccode,data['subslotid']])
                print("2",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
        
                           

            # print("no delivery chagres.")
        else:
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, True, ccode,data['subslotid']])
                request.session['coup'] = ''
                print("3",cursor.query)
                order = cursor.fetchall()
                amount = order[0][8]
                
            else:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, False, ccode,data['subslotid']])
                print("4",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
                
            # print('delivery charges.')
    
        ordes=order[0][10]
        orderid = order[0][4]
        currcode = order[0][5]
        sername = order[0][6]
        amout = amount*100
        print("execute")
        if walletid != 0:
            if amout >= payt.remaining_balance_bank:
                amout=amout-(payt.remaining_balance_bank*100)
                payt.is_wallet_used_with_payment_gateway=True
                payt.save()
            amout=int(amout)
            print('waalet id execute',walletid)

        if currcode is None:
            currcode = 'inr'
        session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
            
              shipping_options=[
                {
                    "shipping_rate_data":{
                        "type":"fixed_amount",
                        "fixed_amount":{
                            "amount":0,"currency":currcode
                        },
                        "display_name":"`",
                        "delivery_estimate":{
                            # "minimum":{
                            #     "unit":"business_day","value":1
                            # },
                            "maximum":{
                                "unit":"business_day","value":1
                            },
                        },
                    },
                },
            ],
            line_items=[{
                'price_data': {
                    'currency': currcode,
                    'product_data': {
                        'name': sername,
                        'description':ordes,
                        "images":[serimg],
                    },
                    'unit_amount': amout,
                },
                'quantity': 1,
            }],
            metadata={
                "order_id": orderid
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            consent_collection={
                'terms_of_service':'required',
                },
        )
        
        # print(session)
        return JsonResponse({'id': session.id})


    
    
    if 'subslotid' not in data and 'tempid' not in data:
        sys.stdout = open("basic.txt", "a")
        print("details\n", currentuser, infoid, bserviceid, ccode)
        
        serimg="https://www.influencerhiring.com/media/BrandPromotion.jpg"
        if othercharges == '0' or othercharges == ' 0':
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, True, ccode,0])
                request.session['coup'] = ''
                print("5",cursor.query)
                order = cursor.fetchall()
                amount = order[0][8]
                ordes=order[0][10]
               
            else:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, False, ccode,0])
                print("6",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
                ordes=order[0][10]

            print("no delivery chagres.")
        else:
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, True, ccode,0])
                request.session['coup'] = ''
                print("7",cursor.query)
                order = cursor.fetchall()
                amount = order[0][8]
                ordes=order[0][10]
                
            else:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, False, ccode,0])
                print("8",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
                ordes=order[0][10]
                
            print('delivery charges.')
        orderid = order[0][4]
        currcode = order[0][5]
        sername = order[0][6]
        # print("sdzxcv", type(nam), type(sername))
        # sername=sername + '('+nam+')'
        # print("ser", sername)
        amout = amount*100
        if walletid != 0:
            if amout >= payt.remaining_balance_bank:
                amout=amout-(payt.remaining_balance_bank*100)
                payt.is_wallet_used_with_payment_gateway=True
                payt.save()
            amout=int(amout)
            print('waalet id execute',walletid)
        

        
        

        if currcode is None:
            currcode = 'inr'
        session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
            shipping_options=[
                {
                    "shipping_rate_data":{
                        "type":"fixed_amount",
                        "fixed_amount":{
                            "amount":0,"currency":currcode
                        },
                        "display_name":"`",
                        "delivery_estimate":{
                            # "minimum":{
                            #     "unit":"business_day","value":1
                            # },
                            "maximum":{
                                "unit":"business_day","value":1
                            },
                        },
                    },
                },
            ],
            
            
            line_items=[{
                'price_data': {
                    'currency': currcode,
                    'product_data': {
                        'name': sername,
                        'description':ordes,
                        "images":[serimg],
                    },
                    'unit_amount': amout,
                   
                },
                'quantity': 1,
                 
            }],
            metadata={
                "order_id": orderid
            },
            
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            
            consent_collection={
                'terms_of_service':'required',
                },
        )
        
        # print(session)
        return JsonResponse({'id': session.id})



def some_view(order):
    response = requests.get(url=f"https://www.influencerhiring.com/schedule-meet/{order}/")
    print('fdvfv')
    # return HttpResponse(status=200)
    return 0




@csrf_exempt
def webhookpaypal(request):
    sys.stdout = open("webhookpaypal.txt", "a")
    print("webhookpaypal")
    payload = request.body
    payload = json.loads(payload)
    print("payload", payload)
    return HttpResponse(status=200)

@csrf_exempt
def webhook(request):
    sys.stdout = open("webbiookpayment.txt", "a")
    print("Webhook")
    payload = request.body
    payload = json.loads(payload)
    print("try", payload)


    if payload['type'] == 'checkout.session.completed':
        print(payload['type'])
        print(payload['data']['object']['amount_total']/100)
        print(payload['data']['object']['client_reference_id'])
        print(payload['data']['object']['currency'])
        print(payload['data']['object']
              ['customer_details']['address']['country'])
        print(payload['data']['object']['customer_details']['email'])
        print(payload['data']['object']['customer_details']['name'])
        print(payload['data']['object']['metadata']['order_id'])
        print(payload['data']['object']['mode'])
        print(payload['data']['object']['payment_intent'])
        print(payload['data']['object']['payment_method_types'][0])
        print(payload['data']['object']['payment_status'])
        print(payload['livemode'])

        id = Allusers.objects.filter(
            id=payload['data']['object']['client_reference_id'])
        id = id[0]
        cls=id
        ordid = Orders.objects.filter(
            ordersid=payload['data']['object']['metadata']['order_id'])
        if ordid.exists():
            ordid = ordid[0]

        print("1st execute", id, cls, ordid)
        wr = Webhook_Response.objects.filter(
            orderid=payload['data']['object']['metadata']['order_id'])
        print("erer", wr)
        if wr.exists():
            wr = wr[0]
            if payload['data']['object']['payment_status'] == 'paid':
                wr.paymentstatus = True
                wr.save(update_fields=['paymentstatus'])

            wr.amount = payload['data']['object']['amount_total']/100
            wr.clientid = cls
            wr.payloadtype = payload['type']
            wr.currencycode = payload['data']['object']['currency']
            wr.countrycode = payload['data']['object']['customer_details']['address']['country']
            wr.email = payload['data']['object']['customer_details']['email']
            wr.name = payload['data']['object']['customer_details']['name']
            wr.mode = payload['data']['object']['mode']
            wr.stripepaymentid = payload['data']['object']['payment_intent']
            wr.paymentmethodtype = payload['data']['object']['payment_method_types'][0]
            wr.stripeapistatus = payload['livemode']
            wr.save(update_fields=['amount', 'clientid', 'payloadtype', 'currencycode', 'countrycode',
                    'email', 'name', 'mode', 'stripepaymentid', 'paymentmethodtype', 'stripeapistatus'])
            paymentslip(request, payload['data']['object']['customer_details']['email'], payload['data']['object']
                        ['amount_total']/100, payload['data']['object']['currency'], payload['data']['object']['metadata']['order_id'])
            print("update response")
            
        else:
            if payload['data']['object']['payment_status'] == 'paid':
                paymentstatus = True
                
            print('1 st execute')
            
            
           
            try:
                payt=ClientPayout.objects.get(clientid=str(cls),is_wallet_used_with_payment_gateway=True)
                amt=payload['data']['object']['amount_total']/100
                totamot=amt+int(payt.remaining_balance_bank)
                wr = Webhook_Response(paymentstatus=paymentstatus, amount=totamot, clientid=cls, payloadtype=payload['type'], currencycode=payload['data']['object']['currency'], countrycode=payload['data']['object']['customer_details']['address']['country'], email=payload['data']['object']
                                    ['customer_details']['email'], name=payload['data']['object']['customer_details']['name'], mode=payload['data']['object']['mode'], stripepaymentid=payload['data']['object']['payment_intent'], paymentmethodtype='Card and Wallet', stripeapistatus=payload['livemode'], orderid=ordid)
                wr.save()
                hispay=ClientPayoutHistory()
                hispay.clientid=cls
                hispay.paymentid=Payments.objects.get(ordersid=str(ordid.ordersid))
                hispay.wallet_transaction_amount=payt.remaining_balance_bank
                hispay.requested_currency=payt.currency
                hispay.remark='Order Purchased Using Wallet Balance And Stripe Gateway'
                hispay.save()
                if totamot >= payt.remaining_balance_bank:
                    payt.remaining_balance_bank=0
                    payt.is_wallet_used_with_payment_gateway=False
                    payt.save()
                print('waalet with strip execute')
            except ClientPayout.DoesNotExist:
                wr = Webhook_Response(paymentstatus=paymentstatus, amount=payload['data']['object']['amount_total']/100, clientid=cls, payloadtype=payload['type'], currencycode=payload['data']['object']['currency'], countrycode=payload['data']['object']['customer_details']['address']['country'], email=payload['data']['object']
                                    ['customer_details']['email'], name=payload['data']['object']['customer_details']['name'], mode=payload['data']['object']['mode'], stripepaymentid=payload['data']['object']['payment_intent'], paymentmethodtype=payload['data']['object']['payment_method_types'][0], stripeapistatus=payload['livemode'], orderid=ordid)
                wr.save()
                print('stripe onley')
            print('save respose')
            Thread(target=lambda:existing_user(request,name=id.username,user_type='existing_user',email_add=payload['data']['object']['customer_details']['email'],template_name='payment-received.html',subject='Payment Confirmation For Your Order #'+str(payload['data']['object']['metadata']['order_id']),order_date=ordid.orderdate,order_no=ordid.ordersid,payment_amount=str(payload['data']['object']['currency'])+' '+str(payload['data']['object']['amount_total']/100),payment_method=payload['data']['object']['payment_method_types'][0])).start()
            
            Thread(target=lambda:existing_user(request,name=ordid.influencerid.influencer_userid.username,user_type='existing_user',email_add=ordid.influencerid.influencer_userid.email,template_name='order-recieved-influencer.html',subject='New Order #'+str(payload['data']['object']['metadata']['order_id']+'Recievd'),order_date=ordid.orderdate,order_no=ordid.ordersid,payment_amount=str(payload['data']['object']['currency'])+' '+str(payload['data']['object']['amount_total']/100),payment_method=payload['data']['object']['payment_method_types'][0])).start()
            
            send_customer_email(key='client-neworderplaced',user_email=id.email,
                   client=id.username,influencer=ordid.influencerid.influencer_userid.username,order_id=ordid.ordersid,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None) 
            
            send_customer_email(key='influencer-neworderplaced',user_email=ordid.influencerid.influencer_userid.email,
                   client=id.username,influencer=ordid.influencerid.influencer_userid.username,order_id=ordid.ordersid,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None) 
            
            if cls.roles=='client':
                Thread(target=lambda:sendusernotification(user=cls.id,key='user-orderplaced',RM_Name=None,Influencer_Name=ordid.influencerid.influencer_userid.username,Product_Name=ordid.serviceid.servicename,Decline_Reason=None,Order_Id=ordid.ordersid)).start()
                Thread(target=lambda:sendusernotification(user=cls.id,key='user-chatinvitation',RM_Name=None,Influencer_Name=ordid.influencerid.influencer_userid.username,Product_Name=ordid.serviceid.servicename,Decline_Reason=None,Order_Id=ordid.ordersid)).start()
                
            
            if cls.roles=='agency':
                Thread(target=lambda:sendagencynotification(user=cls.id,key='agency-orderplaced',castingcallid=None,RM_Name=None,Influencer_Name=ordid.influencerid.influencer_userid.username,Product_Name=ordid.serviceid.servicename,Decline_Reason=None,Order_Id=ordid.ordersid)).start()            
                Thread(target=lambda:sendagencynotification(user=cls.id,key='agency-chatinvitation',castingcallid=None,RM_Name=None,Influencer_Name=ordid.influencerid.influencer_userid.username,Product_Name=ordid.serviceid.servicename,Decline_Reason=None,Order_Id=ordid.ordersid)).start()            
                
                
            
            
            Thread(target=lambda:sendInfluencernotification(user=ordid.influencerid.influencer_userid.id,key='influencer-orderrecived',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=ordid.ordersid,reason=None)).start()
            Thread(target=lambda:sendInfluencernotification(user=ordid.influencerid.influencer_userid.id,key='influencer-orderchat',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=ordid.ordersid,reason=None)).start()
            
            Thread(target=lambda:sendRMnotification(key='rm-influencerreciveorder',RM_Name=None,client_type=None,client_Name=ordid.clientid.username,rmid=ordid.rmid,Influencer_Name=ordid.influencerid.influencer_userid.username,Order_ID=ordid.ordersid,reason=None,Order_Stage=None)).start()
            
            cartin=Cart.objects.filter(clientid=str(cls.id),influencerid=str(ordid.influencerid.influencer_userid.id))
            cartin.delete()
            
            
            
            print('sendmain;')
            # paymentslip(request, payload['data']['object']['customer_details']['email'], payload['data']['object']
            #             ['amount_total']/100, payload['data']['object']['currency'], payload['data']['object']['metadata']['order_id'])
            
            

                    
                
                

        
        if ordid.serviceid.serviceid==2:
            some_view(int(ordid.ordersid))
            print("save zoommeet")
        
        
        
        

    walres = Webhookfullresponse()
    walres.json_response = payload
    walres.save()
    print("Save Webresponse")
    
    return HttpResponse(status=200)







def generatewallettransaction_id(id):
    # Generate a UUID4, which is a randomly generated UUID
    transaction_id = id
    
    # Convert the UUID to a string
    transaction_id_str = str(transaction_id)

    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time as a string
    datetime_str = current_datetime.strftime("%Y%m%d%H%M%S")

    # Combine the "wallet" string, date, time, and UUID to create the unique ID
    unique_id = f"wallet_{datetime_str}_{transaction_id_str}"
    
    return unique_id




def Walletpurchase(request):
    
    
    
    if request.method == 'POST':
        sys.stdout = open("walletpur.txt", "a",encoding='UTF-8')
        walletid = request.POST.get('walletid')
        ccode = request.session.get('coup')
        currentuser = request.user.id
        cursor = connection.cursor()
        infoid = str(request.POST.get('infoid'))
        bserviceid = request.POST.get('bserviceid')
        bplanid = request.POST.get('bplanid')
        othercharges = request.POST.get('othercharges')

        payt=ClientPayout.objects.get(payoutid=walletid)
        
        data=dict(request.POST)
        
        print('sdvzc',data,type(data),'couponcide',ccode)
        
        # print('gm',data['temptext'][0])
        
        
        
        if bserviceid=='5' or bserviceid==5:
            
            eventname = data['eventname'][0]
            eventdate = data['eventdate'][0]
            eventtype = data['eventtype'][0]
            timefrom = data['timefrom'][0]
            timeto = data['timeto'][0]
            address = data['address'][0]
            description = data['description'][0]
            clienttimezone=get_timezone(request)

            print(eventname,eventdate,eventtype,timefrom,timeto,address,description,clienttimezone)

            if othercharges == '0' or othercharges == ' 0':
                if ccode is not None and len(ccode) > 2:
                    cursor.execute('select * from placeinfluenceracquisitionorders(%s,%s,%s,%s,%s,%s,%s,%s,%s::integer,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, True, ccode,eventname,eventdate,eventtype,timefrom,timeto,address,description,clienttimezone])
                    print("1",cursor.query)
                    request.session['coup'] = ''
                    order = cursor.fetchall()
                    amount = order[0][8]

                else:
                    cursor.execute('select * from placeinfluenceracquisitionorders(%s,%s,%s,%s,%s,%s,%s,%s,%s::integer,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, False, ccode,eventname,eventdate,eventtype,timefrom,timeto,address,description,clienttimezone])
                    print("2",cursor.query)
                    order = cursor.fetchall()
                    amount = order[0][3]
                    # print("template chagres.")
            else:
                if ccode is not None and len(ccode) > 2:
                    cursor.execute('select * from placeinfluenceracquisitionorders(%s,%s,%s,%s,%s,%s,%s,%s,%s::integer,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, True, ccode,eventname,eventdate,eventtype,timefrom,timeto,address,description,clienttimezone])
                    print("3",cursor.query)
                    request.session['coup'] = ''
                    order = cursor.fetchall()
                    amount = order[0][8]

                else:
                    cursor.execute('select * from placeinfluenceracquisitionorders(%s,%s,%s,%s,%s,%s,%s,%s,%s::integer,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, False, ccode,eventname,eventdate,eventtype,timefrom,timeto,address,description,clienttimezone])
                    print("4",cursor.query)
                    order = cursor.fetchall()
                    amount = order[0][3]
            
        
        
        if bserviceid==4 or bserviceid=='4':
            if othercharges == '0' or othercharges == ' 0':
                if ccode is not None and len(ccode) > 2:
                    cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, True, ccode,data['tempid'][0],data['temptext'][0]])
                    print("1",cursor.query)
                    request.session['coup'] = ''
                    order = cursor.fetchall()
                    amount = order[0][8]

                else:
                    cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, False, ccode,data['tempid'][0],data['temptext'][0]])
                    print("2",cursor.query)
                    order = cursor.fetchall()
                    amount = order[0][3]
                    # print("template chagres.")
            else:
                if ccode is not None and len(ccode) > 2:
                    cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, True, ccode,data['tempid'][0],data['temptext'][0]])
                    print("1",cursor.query)
                    request.session['coup'] = ''
                    order = cursor.fetchall()
                    amount = order[0][8]

                else:
                    cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, False, ccode,data['tempid'][0],data['temptext'][0]])
                    print("2",cursor.query)
                    order = cursor.fetchall()
                    amount = order[0][3]
        
        
        if bserviceid==2 or bserviceid=='2':
            
            if othercharges == '0' or othercharges == ' 0':
                if ccode is not None and len(ccode) > 2:
                    cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, False, True, ccode,data['subslotid'][0]])
                    print("1",cursor.query)
                    request.session['coup'] = ''
                    order = cursor.fetchall()
                    amount = order[0][8]
                else:
                    cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, False, False, ccode,data['subslotid'][0]])
                    print("2",cursor.query)
                    order = cursor.fetchall()
                    amount = order[0][3]
            
                            
            else:
                if ccode is not None and len(ccode) > 2:
                    cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, True, True, ccode,data['subslotid'][0]])
                    request.session['coup'] = ''
                    print("3",cursor.query)
                    order = cursor.fetchall()
                    amount = order[0][8]
                    
                else:
                    cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, True, False, ccode,data['subslotid'][0]])
                    print("4",cursor.query)
                    order = cursor.fetchall()
                    amount = order[0][3]
        
        
        
        
        if bserviceid==1 or bserviceid=='1' or bserviceid==7 or bserviceid=='7' or bserviceid==3 or bserviceid=='3':
        
            print("details\n", currentuser, infoid, bserviceid, ccode)
            
            
            if othercharges == '0' or othercharges == ' 0':
                if ccode is not None and len(ccode) > 2:
                    cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, False, True, ccode,0])
                    request.session['coup'] = ''
                    print("5",cursor.query)
                    order = cursor.fetchall()
                    amount = order[0][8]
                    ordes=order[0][10]
                
                else:
                    cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, False, False, ccode,0])
                    print("6",cursor.query)
                    order = cursor.fetchall()
                    amount = order[0][3]
                    ordes=order[0][10]

                print("no delivery chagres.")
            else:
                if ccode is not None and len(ccode) > 2:
                    cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, True, True, ccode,0])
                    request.session['coup'] = ''
                    print("7",cursor.query)
                    order = cursor.fetchall()
                    amount = order[0][8]
                    ordes=order[0][10]
                    
                else:
                    cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                                [currentuser, infoid, bplanid, bserviceid, True, False, ccode,0])
                    print("8",cursor.query)
                    order = cursor.fetchall()
                    amount = order[0][3]
                    ordes=order[0][10]
                    
                print('delivery charges.')
        orderid = order[0][4]
     
     
       
        amout = amount
        if amout <= payt.remaining_balance_bank :#and currenttime > previoususer_datetime+1min:
            payt.remaining_balance_bank-=amout
            payt.save()
            
            
            
        
    
            print('request.POST',request.POST,walletid,othercharges)
            id = Allusers.objects.filter(id=request.user.id)
            id = id[0]
            cls=id
            ordid = Orders.objects.filter(ordersid=orderid)
        
            if ordid.exists():
                ordid = ordid[0]
                print('fsdfasdf',ordid.serviceid,type(ordid.serviceid))
                if int(ordid.serviceid.serviceid)==2:
                    some_view(int(ordid.ordersid))
                    print("save zoommeet")
            paymentstatus = True
                
            print('1 st execute')
            
            pyid=generatewallettransaction_id(orderid)
            
            wr = Webhook_Response(paymentstatus=paymentstatus, amount=amout, clientid=cls, currencycode=payt.currency, email=request.user.email
                                    , name=request.user.username,   paymentmethodtype='Wallet Only', orderid=ordid,stripepaymentid=pyid)
            wr.save()
        
            request.session['pur_ordid'] = orderid

            request.session['trans_id'] = pyid
            request.session['orde_amt'] = amout
            request.session['order_date'] = str(ordid.orderdate)
            request.session['influencer_name'] = ordid.influencerid.influencer_userid.username

            
            
            
            hispay=ClientPayoutHistory()
            hispay.clientid=cls
            hispay.paymentid=Payments.objects.get(ordersid=orderid)
            hispay.wallet_transaction_amount=amout
            hispay.requested_currency=payt.currency
            hispay.remark='Order Purchased Using Wallet Balance Only'
            hispay.save()
            
            
            cartin=Cart.objects.filter(clientid=str(id.id),influencerid=str(ordid.influencerid.influencer_userid.id))
            cartin.delete()
                
            
            
            print('save respose')
            
            Thread(target=lambda:existing_user(request,name=id.username,user_type='existing_user',
            email_add=request.user.email,template_name='payment-received.html',
            subject='Payment Confirmation For Your Order #'+str(ordid.ordersid),
            order_date=ordid.orderdate,order_no=ordid.ordersid,
            payment_amount=str(payt.currency)+' '+str(amout),payment_method='Wallet Only')).start()
            # 
            Thread(target=lambda:existing_user(request,name=ordid.influencerid.influencer_userid.username,user_type='existing_user',
                                                email_add=ordid.influencerid.influencer_userid.email,
                template_name='order-recieved-influencer.html',subject='New Order #'+str(str(ordid.ordersid)+'Recievd'),order_date=ordid.orderdate,
                order_no=ordid.ordersid,payment_amount=str(payt.currency)+' '+str(amout),payment_method='Wallet Only')).start()
            
            send_customer_email(key='client-neworderplaced',user_email=id.email,
                    client=id.username,influencer=ordid.influencerid.influencer_userid.username,order_id=ordid.ordersid,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None) 
            
            send_customer_email(key='influencer-neworderplaced',user_email=ordid.influencerid.influencer_userid.email,
                    client=id.username,influencer=ordid.influencerid.influencer_userid.username,order_id=ordid.ordersid,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None) 
            
            if cls.roles=='client':
                Thread(target=lambda:sendusernotification(user=cls.id,key='user-orderplaced',RM_Name=None,Influencer_Name=ordid.influencerid.influencer_userid.username,Product_Name=ordid.serviceid.servicename,Decline_Reason=None,Order_Id=ordid.ordersid)).start()
                Thread(target=lambda:sendusernotification(user=cls.id,key='user-chatinvitation',RM_Name=None,Influencer_Name=ordid.influencerid.influencer_userid.username,Product_Name=ordid.serviceid.servicename,Decline_Reason=None,Order_Id=ordid.ordersid)).start()
                
            
            if cls.roles=='agency':
                Thread(target=lambda:sendagencynotification(user=cls.id,key='agency-orderplaced',castingcallid=None,RM_Name=None,Influencer_Name=ordid.influencerid.influencer_userid.username,Product_Name=ordid.serviceid.servicename,Decline_Reason=None,Order_Id=ordid.ordersid)).start()            
                Thread(target=lambda:sendagencynotification(user=cls.id,key='agency-chatinvitation',castingcallid=None,RM_Name=None,Influencer_Name=ordid.influencerid.influencer_userid.username,Product_Name=ordid.serviceid.servicename,Decline_Reason=None,Order_Id=ordid.ordersid)).start()            
                
                
                        
            
            Thread(target=lambda:sendInfluencernotification(user=ordid.influencerid.influencer_userid.id,key='influencer-orderrecived',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=ordid.ordersid,reason=None)).start()
            Thread(target=lambda:sendInfluencernotification(user=ordid.influencerid.influencer_userid.id,key='influencer-orderchat',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=ordid.ordersid,reason=None)).start()
            
            Thread(target=lambda:sendRMnotification(key='rm-influencerreciveorder',RM_Name=None,client_type=None,client_Name=ordid.clientid.username,rmid=ordid.rmid,Influencer_Name=ordid.influencerid.influencer_userid.username,Order_ID=ordid.ordersid,reason=None,Order_Stage=None)).start()
            
            
        return JsonResponse({'results': 'ok'})
    
    



logger = logging.getLogger()
fh = logging.FileHandler('paymentapp_view_log.txt')
logger.addHandler(fh)
