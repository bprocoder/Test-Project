from django.shortcuts import render, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib import messages
from django.conf import settings
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from mainapp.views import get_timezone
from mainapp.models import *
from mainapp.views import get_location
import math

import uuid,sys,json
# Create your views here.

@csrf_exempt
def paypalbutton(request):
    currentuser = request.user.id
    infoid = request.GET.get('infoid')
    bserviceid = request.GET.get('bserviceid')
    bplanid = request.GET.get('bplanid')
    othercharges = request.GET.get('othercharges')    
    ccode = request.session.get('coup')
    cursor = connection.cursor()
   
    # othercharges=othercharges[4:]

    
    print('infoid',infoid)
    print('bservice',bserviceid)
    

    
    order=None
    
    if bserviceid=='5' or bserviceid==5:
        eventname = request.GET.get('eventname')
        eventdate = request.GET.get('eventdate')
        eventtype = request.GET.get('eventtype')
        timefrom = request.GET.get('timefrom')
        timeto = request.GET.get('timeto')
        address = request.GET.get('address')
        description = request.GET.get('description')
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
                    
    if request.GET.get('tempid') is not None and  request.GET.get('temptext') is not None:
        
        if othercharges == '0' or othercharges == ' 0':
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, ccode,request.GET.get('tempid'),request.GET.get('temptext')])
                print("5",cursor.query)
                request.session['coup'] = ''
                order = cursor.fetchall()
                amount = order[0][8]

            else:
                cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, ccode,request.GET.get('tempid'),request.GET.get('temptext')])
                print("6",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
                # print("template chagres.")
        else:
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, ccode,request.GET.get('tempid'),request.GET.get('temptext')])
                print("7",cursor.query)
                request.session['coup'] = ''
                order = cursor.fetchall()
                amount = order[0][8]

            else:
                cursor.execute('select * from placegreetingsorders(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, ccode,request.GET.get('tempid'),request.GET.get('temptext')])
                print("8",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
                # print("template chagres.")
    
    if  request.GET.get('subslotid') is not None:

        if othercharges == '0' or othercharges == ' 0' or othercharges == '  0' :
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, True, ccode,request.GET.get('subslotid')])
                print("9",cursor.query)
                request.session['coup'] = ''
                order = cursor.fetchall()
                amount = order[0][8]
            else:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, False, ccode,request.GET.get('subslotid')])
                print("10",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
        
                           

            print("no delivery chagres.")
        else:
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, True, ccode,request.GET.get('subslotid')])
                request.session['coup'] = ''
                print("11",cursor.query)
                order = cursor.fetchall()
                amount = order[0][8]
                
            else:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, False, ccode,request.GET.get('subslotid')])
                print("12",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
            print('delivery',bserviceid )
    
    
    sys.stdout = open("basic.txt", "a")
    print('rahulother',request.GET.get('othercharges'))
    
                
    if bserviceid=='1' or bserviceid==1 or bserviceid=='3' or bserviceid==3 or bserviceid=='7' or bserviceid==7:

        if othercharges == '0' or othercharges == ' 0' or othercharges == 0:
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, True, ccode,0])
                request.session['coup'] = ''
                print("13",cursor.query)
                order = cursor.fetchall()
                amount = order[0][8]
                ordes=order[0][10]
                
            else:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, False, False, ccode,0])
                print("14",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
                ordes=order[0][10]

            # print("no delivery chagres.")
        else:
            if ccode is not None and len(ccode) > 2:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, True, ccode,0])
                request.session['coup'] = ''
                print("15",cursor.query)
                order = cursor.fetchall()
                amount = order[0][8]
                ordes=order[0][10]
                
            else:
                cursor.execute('select * from placeorderss(%s,%s,%s,%s,%s,%s,%s,%s)',
                            [currentuser, infoid, bplanid, bserviceid, True, False, ccode,0])
                print("16",cursor.query)
                order = cursor.fetchall()
                amount = order[0][3]
                ordes=order[0][10]
                print('all3:', order,amount)
    
    # infoid = ''
    # bserviceid = ''
    # bplanid = ''
    # othercharges = ''
        # print('delivery charges.')
    orderid = order[0][4]
    currcode = order[0][5]
    sername = order[0][6]
 
    amout = amount
    
    infocurr=request.session.get('selectinfocurr')
    
    
    print('orderid',orderid)
    print('service',sername)
    print('amount')
    print(amout)
    
    
    # infocurr='SLL'
    if infocurr == 'INR':
        rates = ExchangeRates.objects.filter(country='United States').values('rates')[:1]
        rate_value = rates[0]['rates'] if rates else 1
        amout=float(amout)*rate_value

    # elif infocurr =='USD':
    #     amout=amout
    else:
        
        rates = ExchangeRates.objects.filter(country='United States').values('rates')[:1]
        rate_value = rates[0]['rates'] if rates else 1
        amout=float(amout)*rate_value
    
        # rates = ExchangeRates.objects.filter(countery_abbrevation=str(infocurr)).values('rates')[:1]
        # rate_value = rates[0]['rates'] if rates else 1
        # norrup=1/rate_value
        # amout=amout*norrup
        # rates = ExchangeRates.objects.filter(country='United States').values('rates')[:1]
        # rate_value = rates[0]['rates'] if rates else 1
        # amout=amout*rate_value
        print('before change',amout)
        
    amout=math.ceil(amout)
    
    
    print('aftre change',amout)
    
    
    # country = get_location(request)
  
    # if country == 'India':
    #     country = 'India'
    # else:
    #     country='United States'
    # print("data", country)
    # curs = ExchangeRates.objects.get(country__icontains=country).rates
    # amout=amout*curs
  
    
    
    
    
    
    
    
    print('orderid',orderid)
    print('service',sername)
    print('amount')
    print(amout)
    
    
    
    
    
    
    host = request.get_host()
    
    paypal_dict = {
        # 'PAYPAL_TEST':settings.PAYPAL_TEST,
        'business': 'accounts@influencerhiring.com',#, #'ankit@bol7.com'
        'amount': amout,
        'currnecy_code': 'USD', 
        'item_name': 'sername',
        # 'invoice': str(uuid.uuid4()),
        'invoice': str(orderid),
        
        # 'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return': f'http://{host}{reverse("paypal_reverse")}',#request.build_absolute_uri(reverse('paypal_reverse')),
        'cancel_return': f'http://{host}{reverse("paypal_cancel")}',#request.build_absolute_uri(reverse('paypal_cancel')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form':form}
    print('execute')
    return render(request, 'paypalbutton.html', context)
    
    
    
def paypal_reverse(request):
    # messages.success('payment successful')
    return redirect('paypalbutton')

def paypal_cancel(request):
    # messages.error('payment cancelled')
    return redirect('paypalbutton')