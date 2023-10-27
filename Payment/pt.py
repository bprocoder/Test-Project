import logging
import stripe
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.sessions.models import Session
import sys
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from mainapp.views import get_location
from mainapp.enanddc import encrypt, decrypt
import json
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
import os
import json
from django.db.models import Q, F
# from django.urls import reverse
# from django.core.signing import Signer
from mainapp.models import *
from Account.models import *
from mainapp.views import get_timezone



stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'https://www.influencerhiring.com'

# home view


def homepage(request):
    return render(request, 'checkout.html')

# success view


def success(request):
    return render(request, 'success.html')

# cancel view


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
    print("postdata",request.body)
    
    ordes=None
    exprice=None
    exdays=None
    ch=None
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

        if currcode is None:
            currcode = 'inr'
        session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
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

        if currcode is None:
            currcode = 'inr'
        session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
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

        if currcode is None:
            currcode = 'inr'
        session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
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
                exprice=order[0][11]
                if exprice is None:
                    exprice=0
                else:
                    exprice=exprice*100
                
                if exprice==0:
                    exdays=order[0][14].days
                    ch='Free Delivery'
                else:
                    exdays=order[0][12].days
                    ch='Taxes and Fast Response Charges'
                print(ordes,exprice,exdays)
            else:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, False, ccode,0])
                print("6",cursor.query)
                order = cursor.fetchall()
                amount = order[0][13]
                ordes=order[0][10]
                exprice=order[0][11]
                if exprice is None:
                    exprice=0+order[0][2]*100
                else:
                    exprice=exprice*100+order[0][2]*100
                
                if exprice==0+order[0][2]*100:
                    exdays=order[0][14].days
                    ch='Taxes'
                else:
                    exdays=order[0][12].days
                    ch='Taxes and Fast Response Charges'
                print(ordes,exprice,exdays)
                
                

            # print("no delivery chagres.")
        else:
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, True, ccode,0])
                request.session['coup'] = ''
                print("7",cursor.query)
                order = cursor.fetchall()
                amount = order[0][8]-order[0][11]
                ordes=order[0][10]
                exprice=order[0][11]
                if exprice is None:
                    exprice=0
                else:
                    exprice=exprice*100
                
                if exprice==0:
                    exdays=order[0][14].days
                    ch='Free Delivery'
                else:
                    exdays=order[0][12].days
                    ch='Taxes and Fast Response Charges'
                print(ordes,exprice,exdays)
                
            else:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, False, ccode,0])
                print("8",cursor.query)
                order = cursor.fetchall()
                amount = order[0][13]
                ordes=order[0][10]
                exprice=order[0][11]
                if exprice is None:
                    exprice=0+order[0][2]*100
                else:
                    exprice=exprice*100+order[0][2]*100
                
                if exprice==0+order[0][2]*100:
                    exdays=order[0][14].days
                    ch='Taxes'
                else:
                    exdays=order[0][12].days
                    ch='Taxes and Fast Response Charges'
                print(ordes,exprice,exdays)
            # print('delivery charges.')
            

    

        print("enter", infoid, bserviceid)
        print("client", currentuser, bplanid, othercharges)

        
        
        print("Order", order)

        nam = order[0][1]
        
        orderid = order[0][4]
        currcode = order[0][5]
        sername = order[0][6]
        # print("sdzxcv", type(nam), type(sername))
        # sername=sername + '('+nam+')'
        # print("ser", sername)
        amout = amount*100

        # print("details\n", amount, orderid, currcode, sername)
        print("execute")

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
                            "amount":exprice,"currency":currcode
                        },
                        "display_name":ch,
                        "delivery_estimate":{
                            # "minimum":{
                            #     "unit":"business_day","value":0
                            # },
                            "maximum":{
                                "unit":"business_day","value":exdays
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
        cls = ClientSettings.objects.filter(csettingsuserid=id)
        if cls.exists():
            cls = cls[0]
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

            wr = Webhook_Response(paymentstatus=paymentstatus, amount=payload['data']['object']['amount_total']/100, clientid=cls, payloadtype=payload['type'], currencycode=payload['data']['object']['currency'], countrycode=payload['data']['object']['customer_details']['address']['country'], email=payload['data']['object']
                                  ['customer_details']['email'], name=payload['data']['object']['customer_details']['name'], mode=payload['data']['object']['mode'], stripepaymentid=payload['data']['object']['payment_intent'], paymentmethodtype=payload['data']['object']['payment_method_types'][0], stripeapistatus=payload['livemode'], orderid=ordid)
            wr.save()
            paymentslip(request, payload['data']['object']['customer_details']['email'], payload['data']['object']
                        ['amount_total']/100, payload['data']['object']['currency'], payload['data']['object']['metadata']['order_id'])
            print("save response")
        

    walres = Webhookfullresponse()
    walres.json_response = payload
    walres.save()
    print("Save Webresponse")
    
    return HttpResponse(status=200)


logger = logging.getLogger()
fh = logging.FileHandler('paymentapp_view_log.txt')
logger.addHandler(fh)
