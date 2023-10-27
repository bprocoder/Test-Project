from django.shortcuts import render,HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from mainapp.enanddc import encrypt, decrypt
from mainapp.models import *
from Creator.models import *
from Creator.views import get_monthly_orders
import logging
from django.db import connection
from django.db.models import F
from django.db.models import Subquery,OuterRef
import csv
import io
from .models import *
from django.db.models.functions import TruncMonth, Extract
from django.db.models import Q,Sum, Case, When, F, Value, IntegerField, Count,Func, DateTimeField
from django.db.models.functions import  Coalesce
import locale
from Client.models import *
from Creator.views import *
from agora_chat.models import *
import sys
# Create your views here.




@login_required(login_url='/login/')
def Invoice(request,orderid=None):
    cursor = connection.cursor()
    #sys.stdout = open("invoice.txt", "a")
    
    print("orid",orderid)
    orderid=decrypt(orderid)
    print("new oridered",orderid)
    
    cursor.execute('''
	        select mo.ordersid,mcp.fullname,mau.email,mip.fullname,ms.servicename,
            mi.Invoiceid,mi.invoicedate,mi."Taxamount",mi.taxpercentage,mo.finalamt,mo.orderamt,mip.currency
            from mainapp_orders as mo join 
            mainapp_clientprofile as mcp on mo.clientid=mcp.client_userid join
            mainapp_allusers as mau on mo.clientid=mau.id join
            mainapp_invoices as mi on mo.ordersid=mi.ordersid join
            mainapp_influencerprofile as mip on mo.influencerid=mip.influencer_userid join
            mainapp_services as ms on ms.serviceid=mo.serviceid
            where mo.ordersid=(%s);
    ''',[orderid])
    dat = cursor.fetchall()
    print("execute",dat)
    
    cursor.close()
    #sys.stdout.close()
    return render(request, "Account/invoice.html",{'detail':dat})


def monthlywisepayments():
   
    current_year = datetime.now().year

    # Create a list of all month names for the current year
    all_month_names = [str(month) for month in range(1, 13)]

    # Use annotate and TruncMonth to group by paymentdate on a monthly basis
    # Extract the month name and year
    monthly_payment_totals = Payments.objects.filter(
        ordersid__orderstatus=1,  # Add any additional filters as needed
        paymentdate__year=current_year  # Filter for the current year
    ).annotate(
      
        month_name=Extract('paymentdate', 'month'),
    ).values('month_name').annotate(total_amountpaid=Sum('amountpaid'))

    # Convert the monthly_payment_totals queryset to a dictionary for easy lookup
    monthly_totals_dict = {entry['month_name']: entry['total_amountpaid'] for entry in monthly_payment_totals}

    print('monadsf',monthly_totals_dict)
    # Create a list of results including default 0 values for non-existing months
    
    
    
    monthly_transaction_amount = ClientWithdrawalRequest.objects.filter(
    accountant_action=True, clientid__roles='influencer', creationdate__year=current_year
).annotate(
    
    month_name=Extract('creationdate', 'month'),
    
).values('month_name').annotate(total_amountpaid=Sum('transaction_amount'))

    monthly_transaction_dict = {entry['month_name']: entry['total_amountpaid'] for entry in monthly_transaction_amount}
    
    
    
    
    profit=[]
    revenue=[]
    expense=[]
    for month_name in all_month_names:
        month_name=int(month_name)
        if month_name in monthly_totals_dict:
            total_amountpaid =monthly_totals_dict[month_name]
        else:
            total_amountpaid=0
            
        if month_name in monthly_transaction_dict:
            total_transaction =monthly_transaction_dict[month_name]
        else:
            total_transaction=0
            
        totalsaving=total_amountpaid-total_transaction
            
        # result.append({'month_name': month_name, 'total_amountpaid': total_amountpaid,'total_transaction':total_transaction,'totalsaving':totalsaving})
        profit.append(totalsaving)
        revenue.append(total_amountpaid)
        expense.append(total_transaction)
        
        

    
    # result = [{'month_name': month_name, 'total_amountpaid': monthly_totals_dict.get(int(month_name), 0)}
    #       for month_name in all_month_names]

    
    return [profit,revenue,expense]
        


@login_required(login_url='/login/')
def Account_Dashboard(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    locale.setlocale(locale.LC_ALL, 'en_US')
    accpro=Accountprofile.objects.get(accountuserid=userid)
    if permissionname == 'account_permission':
        # sys.stdout = open("accountdeatils.txt", "a")
        orders_pay= Payments.objects.all()
        orders_ids_query=orders_pay.values_list('ordersid', flat=True)
        orders_id_list = list(orders_ids_query)
        ords=Orders.objects.filter(~Q(serviceid=None),paymentstatus=True,ordersid__in=orders_id_list).order_by('-ordersid')
        allserorders=ords.count()
        allserorders=locale.format('%d', allserorders, grouping=True)
        
        total_amount_paid =orders_pay.aggregate(Sum('amountpaid'))['amountpaid__sum']
        total_amount_paid1 =orders_pay.filter(ordersid__orderstatus=1).aggregate(Sum('amountpaid'))['amountpaid__sum']
        total_amount_paid2 =orders_pay.filter(ordersid__orderstatus=3).aggregate(Sum('amountpaid'))['amountpaid__sum']
        total_amount_paid3 =orders_pay.filter(ordersid__orderstatus=5).aggregate(Sum('amountpaid'))['amountpaid__sum']
        
        total_transaction_amount = ClientWithdrawalRequest.objects.filter(
    accountant_action=True, clientid__roles='influencer'
).aggregate(Sum('transaction_amount'))['transaction_amount__sum']
        
        totalsaving=total_amount_paid1-total_transaction_amount
        
        
        monthly__totals = monthlywisepayments()
        
        profit=monthly__totals[0]
        revenue=monthly__totals[1]
        expense=monthly__totals[2]

        max_revenue = max(revenue)


        
        print('monthlyadfs',monthly__totals)
        
        
        
        
        

        return render(request, "Account/index.html",{'max_revenue':max_revenue,'expense':expense,'revenue1':revenue,'profit':profit,'totalsaving':totalsaving,'acc':accpro,'ords':ords[:16],
                                                     'totord':total_amount_paid,'totord3':total_amount_paid1,'totord1':total_amount_paid2,'totord2':total_amount_paid3,
                                                     'allserorders':allserorders,'sum_finalamt2':total_amount_paid,'sum_finalamt5':total_amount_paid1,'sum_finalamt8':total_amount_paid2,'sum_finalamt11':total_transaction_amount,})  
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def user_bankdetails(request):  
    user = request.user    
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'kyc_manager_permission':
        
        selectuserid = request.session.get('bankselectid', None)
        accoun = Useraccounts.objects.filter(usersid=selectuserid)
        if accoun.exists():
            accoun = accoun[0]
            accno = decrypt(accoun.accountnumber)
            print("account", accno, accoun.accountnumber)
        else:
            accno = ''

        docs = UserDocuments.objects.filter(usersid=selectuserid)

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
        
        
        
        if  "verifieduserid" in request.POST:
            userids = request.POST.get('verifieduserid')
            
            print('sdfsafg',userids)
            
            UserDocuments.objects.filter(usersid=userids).update(dockyc=True)
            print('upadte cosmens satrta')
            return redirect(request.META['HTTP_REFERER'])

        
        return render(request, "KYC/bank-details.html",{'pass': depass, 'pan': depan, 'addhar': deaddhar, 'cancel': decan,'account': accoun, 'accnum': accno})
    return HttpResponseRedirect("/")
    



@login_required(login_url='/login/')
def kycbrandprofile(request):
    user = request.user    
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'kyc_manager_permission':
      
        agencyselectid=request.session.get('agencyselectid1')
        user=agencyselectid
        id = Allusers.objects.filter(id=str(agencyselectid))
        id = id[0]
    
        cltdet = AgencyProfile.objects.select_related('agency_userid').filter(
            agency_userid=int(user))
        orid = Orders.objects.filter(clientid=str(user)).last()
        logs = LoginIP.objects.filter(
            userid=user).order_by('-LoginIPid')[0:3]
        act = request.session.get('acti', None)
        
        exch=ExchangeRates.objects.all()
        
        docs=UnverifedAgencyDetails.objects.filter(clientid=str(user))
        if docs.exists():
            docs=docs[0]
        else:
            docs=''
            
        if request.method == 'POST':

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
                    id.save(update_fields=['password'])
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
                currnecy=request.POST.get('currnecy')

                pclnt = AgencyProfile.objects.get(agency_userid=str(user))
                
                if currnecy is not None and len(currnecy) > 1:
                    pclnt.currency = currnecy
                    print('up currnecy')
                
                
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
                    id.email = emailaddress
                    id.save(update_fields=['email'])
                    print("up email id")
                pclnt.save()

                print("api", image, name, emailaddress, phone,
                        country, language, timezone, pin, address)
                  
        return render(request, "KYC/brand-profile.html",{'docs':docs,'request_user':id,'exch':exch,'act': act, 'cltdet': cltdet, "orid": orid, 'log': logs, 'userdet': cltdet})
    


@login_required(login_url='/login/')
def Creators_over(request):
    user = request.user
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission' or permissionname == 'kyc_manager_permission':
    
        
        if permissionname=='kyc_manager_permission':
            userid=request.session['infoselectid2']
        else:
            userid=request.session['infoselectid1']
        
        ac = InfluencerProfile.objects.select_related(
            'influencer_userid').filter(influencer_userid=userid)
        ac = ac[0]
        kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc
        inforder = Orders.objects.select_related(
            'clientid', 'serviceid', 'influencerid', 'orderstatus').filter(influencerid=userid, paymentstatus=True).order_by('-ordersid')
        com = inforder.filter(orderstatus=1).count()    
        can = inforder.filter(orderstatus=3).count()
        pan = inforder.filter(orderstatus=5).count()
        act = inforder.filter(orderstatus=6).count()
        tot = inforder.count()
        brand1 = inforder.filter(serviceid=1)
        gm1 = inforder.filter(serviceid=4)
        vcs1 = inforder.filter(serviceid=2)
        ss1 = inforder.filter(serviceid=3)
        ss2 = inforder.filter(serviceid=7)
        ina1 = inforder.filter(serviceid=5)
        

        totbrand = 0
        for i in brand1:
            if i.iscouponapplied == True and i.finalamtafterdiscount > 0:
                totbrand = totbrand+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totbrand = totbrand+i.finalamt

        totgm = 0
        for i in gm1:
            if i.iscouponapplied == True and i.finalamtafterdiscount > 0:

                totgm = totgm+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totgm = totgm+i.finalamt

        totvcs = 0
        for i in vcs1:
            if i.iscouponapplied == True and i.finalamtafterdiscount > 0:
                totvcs = totvcs+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totvcs = totvcs+i.finalamt

        totina = 0
        for i in ina1:
            if i.iscouponapplied == True and i.finalamtafterdiscount > 0:
                totina = totina+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totina = totina+i.finalamt

        totss = 0
        for i in ss1:
            if i.iscouponapplied == True:
                totss = totss+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totss = totss+i.finalamt
        for i in ss2:
            if i.iscouponapplied == True:
                totss = totss+i.finalamtafterdiscount
            else:
                if i.finalamt is not None and (i.finalamt > 0):
                    totss = totss+i.finalamt

        totalearn = totbrand+totgm+totvcs+totina+totss

        
        
        request.session['totalearn1'] = totalearn
        request.session['tot1'] = tot
        request.session['com1'] = com

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


        threshold = timezone.now() - timedelta(minutes=5)
        active_user = Allusers.objects.filter(id=userid, last_activity__gte=threshold)
        if active_user.exists():
            active=True
        else:
            active=False
            
        request.session['active_info'] = active
        #sys.stdout = open("kycrequest.txt", "a")
        
        
        
        print('data',request.POST)
        
        
        
        return render(request, "KYC/influencer-overview.html",{'gis': gis, 'whychoose': whychoose, 'active': active, 'monthname': array2, 'revenue': array1, 'completed_tasks': array, 
                    'act': act, 'pan': pan, 'can': can, 'totalearn': totalearn, 'tot': tot, 'com': com,
                        'info': ac, 'kyc': kyc, 'order': inforder, 'plt': plt, 'lang': lang1, 'pro': pro, })
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Creators_setting(request):
    user = request.user
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission' or permissionname == 'kyc_manager_permission':
        ln = Languages.objects.all()
        cate = Categories.objects.all()
        
        if permissionname=='kyc_manager_permission':
            userid=request.session['infoselectid2']
        else:
            userid=request.session['infoselectid1']
        
        username = Allusers.objects.get(id=userid).email
        id = Allusers.objects.filter(id=userid)
        id = id[0]
   
        ac = InfluencerProfile.objects.select_related(
            'influencer_userid').filter(influencer_userid=userid)
        ac = ac[0]


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

        you = PlatformProfileLink.objects.filter(
            usersid=id, platformtype='Youtube')

        if you.exists():
            you = you[0].profilelink
        else:
            you = ''

        tik = PlatformProfileLink.objects.filter(
            usersid=id, platformtype='Tiktok')
        if tik.exists():
            tik = tik[0].profilelink
        else:
            tik = ''

        twi = PlatformProfileLink.objects.filter(
            usersid=id, platformtype='Twitter')
        if twi.exists():
            twi = twi[0].profilelink
        else:
            twi = ''

        fb = PlatformProfileLink.objects.filter(
            usersid=id, platformtype='Facebook')
        if fb.exists():
            fb = fb[0].profilelink

        ins = PlatformProfileLink.objects.filter(
            usersid=id, platformtype='Instagram')
        if ins.exists():
            ins = ins[0].profilelink
        else:
            ins = ''

        kyc = InfluencerSettings.objects.get(influencer_userid=id).kyc
        totalearn = request.session.get('totalearn1', None)
        tot = request.session.get('tot1', None)
        com = request.session.get('com1', None)

        noti = Notifications.objects.filter(
            touserid=userid).order_by('-notificationid')
        conoti = noti.filter(notificationstatus=False).count()

        exch = ExchangeRates.objects.all()


        why = Whychooseme.objects.filter(
            categoryid__in=ac.categories).order_by('whychoosemeid')
        abo = Aboutme.objects.filter(
            categoryid__in=ac.categories).order_by('aboutmeid')
        shortds = Shortdescription.objects.filter(
            categoryid__in=ac.categories).order_by('shortdescriptionid')

        gig = Rulesgig.objects.all().order_by('rulesid')

        qno = Influencerquestions.objects.filter(influencerid=userid)

        if request.method == 'POST':
            langlist = dict(request.POST)
            fe = request.POST.get("fname")
            image = request.FILES.get("avatar")
            image1 = request.FILES.get("avatar1")
            lan = request.POST.get("language")
            curr = request.POST.get("currency")
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
            if 'whyques' in request.POST:
                whyques = request.POST['whyques']
                whytext = request.POST['whytext']
                whytext1 = request.POST['whytext1']
                whytext2 = request.POST['whytext2']
                whytext3 = request.POST['whytext3']
                whytext4 = request.POST['whytext4']
                wh = []
                wh.extend([whyques, whytext, whytext1,
                        whytext2, whytext3, whytext4])
                cho = Whychooseselected(choosetext=wh)
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
                print("text", rulesforgig11)
                abou = Aboutselected(abouttext=rulesforgig11)
                abou.save()

                aboid = abou.aboutselectedid
                if aboid is not None and aboid > 0:
                    ac.aboutme = aboid
                    ac.save(update_fields=['aboutme'])
                    print('insert aboutme')

            if 'shortdes' in request.POST:
                shortdes = request.POST['shortdes']
                print("text", shortdes)
                abou = Shortdesselected(shortdestext=shortdes)
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

            # facebooklink = request.POST.get("facebooklink")
            # if facebooklink is not None:
            #     ppl = PlatformProfileLink.objects.filter(
            #         usersid=id, platformtype='Facebook')
            #     if ppl.exists():
            #         ppl = ppl[0]
            #         ppl.profilelink = facebooklink
            #         ppl.save(update_fields=['profilelink'])
            #         print("update facebook link")
            #     else:
            #         ppl = PlatformProfileLink(
            #             platformtype='Facebook', usersid=id, profilelink=facebooklink)
            #         ppl.save()
            #         print("Save facebook link")

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
                    # pd.subscribers_followers=instagramdata(instagram)
                    pd.save(update_fields=['subscribers_followers'])
                    # print("instgram followers update")
                else:
                    dp = PlatformDetails()
                    dp.usersid = id
                    dp.platformtype = pltformid
                    dp.platformcredential = instagram
                    # dp.subscribers_followers=instagramdata(instagram)
                    dp.additiontime = datetime.now()
                    dp.save()
                    # print("insert instagram")
            if youtube is not None and len(youtube) > 0:
                pltformid = Platforms.objects.get(
                    platform_name='Youtube').platformid
                pd = PlatformDetails.objects.filter(
                    usersid=id, platformtype=pltformid)
                if pd.exists():
                    # fetchytdetails(youtube, id, pltformid)
                    print("youtube followers update")
                else:
                    # fetchytdetails(youtube, id, pltformid)
                    print("youtube update")
            if tiktok is not None and len(tiktok) > 0:
                pltformid = Platforms.objects.get(
                    platform_name='Tiktok').platformid
                pd = PlatformDetails.objects.filter(
                    usersid=id, platformtype=pltformid)
                if pd.exists():
                    pd = pd[0]
                    pd.platformcredential = tiktok
                    # pd.subscribers_followers=titikusersdet(tiktok,id,pltformid)
                    pd.save(update_fields=[
                            'subscribers_followers', 'platformcredential'])
                    print("Tiktok followers update")
                else:
                    pd1 = PlatformDetails()
                    print('execute')

            if email is not None and len(email) > 0:
                au = Allusers.objects.filter(id=userid)
                if au.exists():
                    au = au[0]
                    au.email = email
                    au.save(update_fields=['email'])
                    # print("update email")

            if ac:
                ac.fullname = fe
                ac.desc_title = des_title
                ac.skills = Skills
                ac.profileimage = image
                ac.mobile = mob
                ac.currency = curr
                ac.country = country
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
                if curr is not None and len(curr) > 0:
                    ac.save(update_fields=['currency'])
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
            print("image", image, fe, lan, curr, mob,
                des_title, short_des, Skills, country, email)
            return redirect(request.META['HTTP_REFERER'])
        stds = Shortdesselected.objects.get(
            shortdesselectedid=ac.short_description).shortdestext
        ac.short_description = stds
        
        selectlangids=ac.language
        
        
        languages_dict = {lang.languageid: lang.languages for lang in Languages.objects.all()}
        ac.language = [languages_dict.get(i) for i in ac.language if languages_dict.get(i)]
        zipped_list = zip(selectlangids, ac.language)
    
        return render(request, "KYC/influencer-setting.html",{'zipped_list':zipped_list,'shortds': shortds, 'qno': qno, 'abo': abo, 'gig': gig, 'why': why, 'exch': exch, 'user': username, 'info': ac, 'insta': instauser, 'yt': ytuser, 'tk': tkuser, 'kyc': kyc, 'lan': ln, 'ytlink': you, 'tiklink': tik, 'twilink': twi, 'fblink': fb, 'inslink': ins, 'totalearn': totalearn, 'tot': tot, 'com': com, 'noti': noti, 'notcount': conoti, 'active': request.session['active_info'], 'cate': cate, })
    return HttpResponseRedirect("/")
    
@login_required(login_url='/login/')
def Creators_serviceplan(request):
    user = request.user
    
    
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission' or permissionname == 'kyc_manager_permission':
        if permissionname=='kyc_manager_permission':
            userid=request.session['infoselectid2']
        else:
            userid=request.session['infoselectid1']
    
        username = Allusers.objects.get(id=userid).email
        id = Allusers.objects.filter(id=userid)
        id = id[0]
        ac = InfluencerProfile.objects.filter(influencer_userid=userid)
        ac = ac[0]

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
            destd = plan.filter(plan_type='Standard')
            if destd.exists():
                destd = destd[0]
                print('destd', destd)

            depre = plan.filter(plan_type='Premium')
            if depre.exists():
                depre = depre[0]

        event_price = ''
        gm_price = ''
        vc_price = ''

        pry = PricingPlans.objects.filter(usersid=id)
        if pry.exists():
            event_price = pry.filter(serviceid=5)
            if event_price.exists():
                event_price = event_price[0]
            else:
                event_price = ''
            gm_price = pry.filter(serviceid=4)
            if gm_price.exists():
                gm_price = gm_price[0]
            else:
                gm_price = ''
            vc_price = pry.filter(serviceid=2)
            if vc_price.exists():
                vc_price = vc_price[0]
            else:
                vc_price = ''

        plan1 = PricingPlans.objects.filter(usersid=id, serviceid=7)
        if plan1.exists():
            debasic1 = plan1.filter(plan_type='Basic')
            if debasic1.exists():
                debasic1 = debasic1[0]
            else:
                debasic1 = ''
            destd1 = plan1.filter(plan_type='Standard')
            if destd1.exists():
                destd1 = destd1[0]
            else:
                destd1 = ''
            depre1 = plan1.filter(plan_type='Premium')
            if depre1.exists():
                depre1 = depre1[0]
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
            else:
                debasic2 = ''
            destd2 = plan2.filter(plan_type='Standard')
            if destd2.exists():
                destd2 = destd2[0]
            else:
                destd2 = ''
            depre2 = plan2.filter(plan_type='Premium')
            if depre2.exists():
                depre2 = depre2[0]
            else:
                depre2 = ''
        else:
            debasic2 = None
            destd2 = None
            depre2 = None

        totalearn = request.session.get('totalearn1', None)
        tot = request.session.get('tot1', None)
        com = request.session.get('com1', None)
        kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc
        noti = Notifications.objects.filter(
            touserid=userid).order_by('-notificationid')
        conoti = noti.filter(notificationstatus=False).count()

        subsslots = Subslots.objects.filter(
            influencerid=str(id)).order_by('-subslotid')



        if request.method == 'POST':
            
            print('date', request.POST)

            vc_start_date = request.POST.get('vc_start_date')
            vc_start_time = request.POST.get('vc_start_time')

            vc_end_date = request.POST.get('vc_end_date')
            vc_end_time = request.POST.get('vc_end_time')
            slot_duration = request.POST.get('slot_duration')

            if vc_end_date is not None and vc_start_time is not None and vc_start_date is not None and vc_end_time is not None and len(vc_end_date) > 1 and len(vc_start_time) > 1 and len(vc_end_time) > 1 and len(vc_start_date) > 1:
                vc_start_date = datetime.strptime(
                    vc_start_date, "%Y-%m-%d").date()
                vc_start_time = datetime.strptime(
                    vc_start_time, "%H:%M").time()

                # combine the date and time into a single datetime object
                vc_start_datetime = datetime.combine(
                    vc_start_date, vc_start_time)
                vc_end_date = datetime.strptime(vc_end_date, "%Y-%m-%d").date()
                vc_end_time = datetime.strptime(vc_end_time, "%H:%M").time()

                # combine the date and time into a single datetime object
                vc_end_datetime = datetime.combine(vc_end_date, vc_end_time)

                durationslot = vc_end_datetime-vc_start_datetime

                print('duration', durationslot)
                sslots = Slots(slottype='Video Chat', starttime=vc_start_datetime, influencerid=iset, slotduration=durationslot,
                               isactive=True, singleslotduration=slot_duration, slotperminprice=int(vc_price.increasedprice))
                sslots.save()
                print('inserte slosst')

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
        return render(request, "KYC/influencer-serviceplan.html",{ 'vc_slots': subsslots, 'vc_price': vc_price, 'gm_price': gm_price, 'event_price': event_price, 'ent': ent, 'active': request.session['active_info'], 'com': com, 'tot': tot, 'totalearn': totalearn, 'user': username, 'info': ac,  'ser': ser,'ser1':ser, 'basic': debasic, 'stand': destd, 'Prem': depre, 'sertag': stt123, 'kyc': kyc, 'noti': noti, 'notcount': conoti, 'basic1': debasic1, 'stand1': destd1, 'Prem1': depre1, 'basic2': debasic2, 'stand2': destd2, 'Prem2': depre2, })
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Creators_bank(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission' or permissionname == 'kyc_manager_permission':
        
        if permissionname=='kyc_manager_permission':
            userid=request.session['infoselectid2']
        else:
            userid=request.session['infoselectid1']
        id = Allusers.objects.filter(id=userid)

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

        totalearn = request.session.get('totalearn1', None)
        tot = request.session.get('tot1', None)
        com = request.session.get('com1', None)

        noti = Notifications.objects.filter(
            touserid=userid).order_by('-notificationid')
        conoti = noti.filter(notificationstatus=False).count()

    
        if request.method == 'POST':
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

            # print("baraeal")
            # print(bankname,currcode,accountname,accountnumber)
            # print(ifsccode,pan,aadhar,cancel)

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

            #sys.stdout = open("earningsdetails.txt", "a")
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

            return redirect(request.META['HTTP_REFERER'])
        
        
        return render(request, "KYC/influencer-bankdetails.html",{'active': request.session['active_info'], 'com': com, 'noti': noti, 'notcount': conoti, 'tot': tot, 'totalearn': totalearn, 'info': ac, 'pass': depass, 'pan': depan, 'addhar': deaddhar, 'cancel': decan, 'kyc': cyc, 'account': accoun, 'accnum': accno})
    return HttpResponseRedirect("/")
   
@login_required(login_url='/login/')
def Creators_seo(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission' or permissionname == 'kyc_manager_permission':
        
        if permissionname=='kyc_manager_permission':
            userid=request.session['infoselectid2']
        else:
            userid=request.session['infoselectid1']
        id = Allusers.objects.filter(id=userid)
        id = id[0]
        permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
            userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
        ac = InfluencerProfile.objects.select_related(
            'influencer_userid').filter(influencer_userid=userid)
        ac = ac[0]
        totalearn = request.session.get('totalearn1', None)
        tot = request.session.get('tot1', None)
        com = request.session.get('com1', None)

        paid = Pages.objects.get(pagename='Service').pageid
        pseo = Seo_Settings.objects.filter(
            page=str(paid), influencerid=str(userid))
        kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc

        noti = Notifications.objects.filter(
            touserid=userid).order_by('-notificationid')
        conoti = noti.filter(notificationstatus=False).count()

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

        return render(request, "KYC/influencer-seo.html",{'active': request.session['active_info'], 'totalearn': totalearn, 'tot': tot, 'com': com, 'info': ac, 'infoseo': pseo, 'kyc': kyc, 'noti': noti, 'notcount': conoti,})
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Total_Earnings(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'account_permission':
        ords=Orders.objects.filter(~Q(serviceid=None),paymentstatus=True).order_by('-ordersid')
        
        return render(request, "Account/total-earnings.html",{'ords':ords})
    return HttpResponseRedirect("/")



@login_required(login_url='/login/')
def Payment(request):
    return render(request, "Account/payment.html")  


@login_required(login_url='/login/')
def Influencers_Payments(request):
    return render(request, "Account/influencer-payment.html") 

@login_required(login_url='/login/')
def Marginset(request):
    user = request.user
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission' :
        influencer=InfluencerSettings.objects.filter(kyc=True).order_by('-influencer_settingsid')
        #sys.stdout = open("ptdt.txt", "a")
        
        if "infomargin" in request.POST:
            infomargin = request.POST.get('infomargin')
            influencerid = request.POST.get('ainfoid')
            
            print('margin',infomargin,influencerid)
            
            new_values = {
    'marginpercentage': infomargin,
    }

            PricingPlans.objects.filter(usersid=str(influencerid)).update(**new_values)
            print('update values')
        
      
        return render(request, "Account/setmargin.html",{'creators':influencer}) 
    return HttpResponseRedirect("/") 


@login_required(login_url='/login/')
def Creators_List(request):
    user = request.user
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission' :
        influencer=InfluencerSettings.objects.filter(kyc=True)
        all=Allusers.objects
        totalcreator=all.filter(roles='influencer').count()
        totalclient=all.filter(roles='client').count()
        totalagency=all.filter(roles='agency').count()
        totalrm=all.filter(roles='RM').count()
        
      
        return render(request, "Account/creators.html",{'totalrm':totalrm,'totalagency':totalagency,'totalclient':totalclient,'totalcreator':totalcreator,'creators':influencer}) 
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def Agency_List(request):
    user = request.user

    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission' :
        agency=AgencySettings.objects.filter(kyc=True)
        all=Allusers.objects
        totalcreator=all.filter(roles='influencer').count()
        totalclient=all.filter(roles='client').count()
        totalagency=all.filter(roles='agency').count()
        totalrm=all.filter(roles='RM').count()
        
      
        return render(request, "Account/agency.html",{'totalrm':totalrm,'totalagency':totalagency,'totalclient':totalclient,'totalcreator':totalcreator,'agency':agency}) 
    return HttpResponseRedirect("/")
     
    
    
@login_required(login_url='/login/')
def Client_List(request):
    user = request.user
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission' :
        client=ClientSettings.objects.all()
        all=Allusers.objects
        totalcreator=all.filter(roles='influencer').count()
        totalclient=all.filter(roles='client').count()
        totalagency=all.filter(roles='agency').count()
        totalrm=all.filter(roles='RM').count()
        
      
        return render(request, "Account/clients.html",{'totalrm':totalrm,'totalagency':totalagency,'totalclient':totalclient,'totalcreator':totalcreator,'clients':client[:100]}) 
    return HttpResponseRedirect("/")




@login_required(login_url='/login/')
def ClientsProfile(request):
     
    user = request.user

    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission' or permissionname == 'kyc_manager_permission':
        
        
        if permissionname=='kyc_manager_permission':
            clientselectid1=request.session.get('clientselectid2')
        else:
            clientselectid1=request.session.get('clientselectid1')
        
        
        user=clientselectid1
        id = Allusers.objects.filter(id=user)
        id = id[0]
    
        cltdet = ClientProfile.objects.select_related('client_userid').filter(
            client_userid=int(user))
        orid = Orders.objects.filter(clientid=str(user)).last()
        logs = LoginIP.objects.filter(
            userid=user).order_by('-LoginIPid')[0:3]
        act = request.session.get('acti', None)
        
        exch=ExchangeRates.objects.all()
        
        docs=UnverifedAgencyDetails.objects.filter(clientid=str(user))
        if docs.exists():
            docs=docs[0]
        else:
            docs=''
    
        
        
        #sys.stdout = open("ptdt.txt", "a")
        if request.method == 'POST':

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
                    id.save(update_fields=['password'])
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
                currnecy=request.POST.get('currnecy')

                pclnt = ClientProfile.objects.get(client_userid=str(user))
                
                if currnecy is not None and len(currnecy) > 1:
                    pclnt.currency = currnecy
                    print('up currnecy')
                
                
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
                    id.email = emailaddress
                    id.save(update_fields=['email'])
                    print("up email id")
                pclnt.save()

                print("api", image, name, emailaddress, phone,
                        country, language, timezone, pin, address)
                  
        return render(request, "KYC/client-profile.html",{'docs':docs,'request_user':id,'exch':exch,'act': act, 'cltdet': cltdet, "orid": orid, 'log': logs, 'userdet': cltdet})
    


@login_required(login_url='/login/')
def Mailviewinvoice(request):
    return render(request, "Account/mailinvoice.html")

@login_required(login_url='/login/')
def Cancelorders(request):

    user = request.user

    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission':
        order_details = Orders.objects.filter(orderstatus=3,paymentstatus=True).order_by('-ordersid')
        
        canorderno=order_details.count()
        penorderno=Orders.objects.filter(orderstatus=5,paymentstatus=True).count()
        
        comorderno=Orders.objects.filter(orderstatus=1,paymentstatus=True).count()
        actorderno=Orders.objects.filter(orderstatus=6,paymentstatus=True).count()
        totorder=Orders.objects.filter(paymentstatus=True).count()
        
        
        

        return render(request, "Account/cancel-order.html",{'totorder':totorder,'actorderno':actorderno,'canorderno':canorderno,'penorderno':penorderno,'comorderno':comorderno,'order': order_details})
    return HttpResponseRedirect("/")
    
@login_required(login_url='/login/')
def Completeorders(request):
    user = request.user

    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission':
        order_details = Orders.objects.filter(orderstatus=1,paymentstatus=True).order_by('-ordersid')
        
        comorderno=order_details.count()
        penorderno=Orders.objects.filter(orderstatus=5,paymentstatus=True).count()
        canorderno=Orders.objects.filter(orderstatus=3,paymentstatus=True).count()
        actorderno=Orders.objects.filter(orderstatus=6,paymentstatus=True).count()
        totorder=Orders.objects.filter(paymentstatus=True).count()
        
        
        
    
    
        return render(request, "Account/complete-order.html",{'totorder':totorder,'actorderno':actorderno,'canorderno':canorderno,'penorderno':penorderno,'comorderno':comorderno,'order': order_details})
    return HttpResponseRedirect("/")
    

@login_required(login_url='/login/')
def Orders_Ac(request):
     
    user = request.user

    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission':
        order_details = Orders.objects.filter(orderstatus=5,paymentstatus=True).order_by('-ordersid')
        
        penorderno=order_details.count()
        canorderno=Orders.objects.filter(orderstatus=3,paymentstatus=True).count()
        comorderno=Orders.objects.filter(orderstatus=1,paymentstatus=True).count()
        actorderno=Orders.objects.filter(orderstatus=6,paymentstatus=True).count()
        totorder=Orders.objects.filter(paymentstatus=True).count()
        
        
        return render(request, "Account/orders.html",{'totorder':totorder,'actorderno':actorderno,'canorderno':canorderno,'penorderno':penorderno,'comorderno':comorderno,'order': order_details})
    return HttpResponseRedirect("/")
    
@login_required(login_url='/login/')
def Activeorders(request):
    
    
    user = request.user

    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission':
        order_details = Orders.objects.filter(orderstatus__in=[6,7],paymentstatus=True).order_by('-ordersid')
        
        actorderno=order_details.count()
        penorderno=Orders.objects.filter(orderstatus=5,paymentstatus=True).count()
        comorderno=Orders.objects.filter(orderstatus=1,paymentstatus=True).count()
        canorderno=Orders.objects.filter(orderstatus=3,paymentstatus=True).count()
        
        totorder=Orders.objects.filter(paymentstatus=True).count()
        
        
        return render(request, "Account/active-orders.html",{'totorder':totorder,'actorderno':actorderno,'canorderno':canorderno,'penorderno':penorderno,'comorderno':comorderno,'order': order_details})
    return HttpResponseRedirect("/")
    



@login_required(login_url='/login/')
def Profile_Settings(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'account_permission':
        #sys.stdout = open("accountdeatils.txt", "a")
        accpro=Accountprofile.objects.get(accountuserid=userid)
        aclogs=Alluserlogs.objects.filter(userid=userid).order_by('-alluserlogsid')[:15]
        if request.method == 'POST':
            testid=request.FILES.get("avatar")
            name=request.POST.get('name')
            email=request.POST.get('email')
            number=request.POST.get('number')
            address1=request.POST.get('address1')

            if name is not None and len(name) >1:
                accpro.name = name
                accpro.save()
            if number is not None and len(number) >1:
                accpro.number = number
                accpro.save()
            if address1 is not None and len(address1) >1:
                accpro.address = address1
                accpro.save()
            if testid is not None and len(testid) >1:
                accpro.image = testid
                accpro.save()
            
            if email is not None and len(email) > 1:
                id.email=email
                id.save(update_fields=['email'])
                
        return render(request, "Account/profile-settings.html",{'aclogs':aclogs,'acc':accpro})
    return HttpResponseRedirect("/")
    

#####################################SEO SETTING#############################################
#####################################SEO SETTING#############################################
#####################################SEO SETTING#############################################


@login_required(login_url='/login/')
def Blogs_Home_Ac(request, cate=None):
    blog = Blog.objects.all()
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'seo_permission':
        if cate is not None: 
            blog = Blog.objects.filter(blog_categories__icontains=cate)
        return render(request, "SEO/blog-home.html", {"allblog": blog})
    return HttpResponseRedirect("/")
    
@login_required(login_url='/login/')
def Blogs_Edit(request,):
    blog = Blog.objects.all()
    bcate = BlogsCate.objects.all()
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'seo_permission':
        if request.method == 'POST':
            name=request.POST.get("name")
            blogcategory=request.POST.get("blogcategory")
            metatitle=request.POST.get("metatitle")
            metadescription=request.POST.get("metadescription")
            keyword=request.POST.get("keyword")
            url=request.POST.get("url")
            blogtitle=request.POST.get("blogtitle")
            shortdiscription=request.POST.get("shortdiscription")
            blogdescription=request.POST.get("blogdescription")
            alttext=request.POST.get("alttext")
            image=request.FILES.get('avatar')
            blogid=request.POST.get("approved")
            
            
            con=Blog.objects.filter(blogid=blogid)
            if con.exists():
                con=con[0]
                if name is not None and len(name) > 0:
                    con.name=name
                    con.save(update_fields=['name'])
                if blogcategory is not None and len(blogcategory) > 0:
                    con.blog_categories=blogcategory
                    con.save(update_fields=['blog_categories'])
                if metatitle is not None and len(metatitle) > 0:
                    con.title_tegs=metatitle
                    con.save(update_fields=['title_tegs'])
                
                if metadescription is not None and len(metadescription) > 0:
                    con.meta_description=metadescription
                    con.save(update_fields=['meta_description'])
                
                if keyword is not None and len(keyword) > 0:
                    con.keyword=keyword
                    con.save(update_fields=['keyword'])
        
                if url is not None and len(url) > 0:
                    con.url_structure=url
                    con.save(update_fields=['url_structure'])
        
                if blogtitle is not None and len(blogtitle) > 0:
                    con.title=blogtitle
                    con.save(update_fields=['title'])
                    
                if shortdiscription is not None and len(shortdiscription) > 0:
                    con.short_discription=shortdiscription
                    con.save(update_fields=['short_discription'])
        
                if blogdescription is not None and len(blogdescription) > 0:
                    con.discription=blogdescription
                    con.save(update_fields=['discription'])
        
                if alttext is not None and len(alttext) > 0:
                    con.alttext=alttext
                    con.save(update_fields=['alttext'])

                if image is not None and len(image) > 0:
                    con.image=image
                    con.save(update_fields=['image'])
        
        
        return render(request, "SEO/blogedit.html",{"blog": blog, "cate": bcate,'data':list(blog.values())})
    return HttpResponseRedirect("/")
    
    
@login_required(login_url='/login/')
def deleteblog(request, blogid):
    Blogcontent.objects.filter(blog=blogid).delete()
    BlogComments.objects.filter(blog=blogid).delete()
    Blog.objects.filter(blogid=blogid).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login/')
def Blogs_Content_Edit(request,):
    blog = Blogcontent.objects.all()
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'seo_permission':
        if request.method == 'POST':
            blogsubtitle=request.POST.get("blogsubtitle")
            description=request.POST.get("description")
            alttext=request.POST.get("target_title")
            image=request.FILES.get("avatar")
            blogcon=request.POST.get("approved")
            
            con=Blogcontent.objects.filter(blogcontentid=blogcon)
            if con.exists():
                con=con[0]
                if blogsubtitle is not None and len(blogsubtitle) > 0:
                    con.title=blogsubtitle
                    con.save(update_fields=['title'])
                if description is not None and len(description) > 0:
                    con.discription=description
                    con.save(update_fields=['discription'])
                if alttext is not None and len(alttext) > 0:
                    con.alttext=alttext
                    con.save(update_fields=['alttext'])
                if image is not None and len(image) > 0:
                    con.image=image
                    con.save(update_fields=['image'])               
                    
                
        
        return render(request, "SEO/editblogcontent.html",{"blog": blog,})
    return HttpResponseRedirect("/")
    

@login_required(login_url='/login/')
def Blogs_Post_Ac(request, name):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'seo_permission':
        # name = name.replace('-', ' ')
        print(name)
        base_url = "{0}://{1}{2}".format(request.scheme,
                                        request.get_host(), request.path)
        print("Url", base_url)

        blog = Blog.objects.all()
        bcate = BlogCategory.objects.all()
        blog1 = blog.order_by('-date').values()[0:5]
        bldet = Blog.objects.filter(url_structure__icontains=name)[0]
        
        content=Blogcontent.objects.filter(blog=str(bldet.blogid)).order_by('blogcontentid')
        if content.exists():
            content=content
        else:
            content=''
        bl = BlogComments.objects.filter(blog=bldet, isapproved=True)
        num = len(bl)
        return render(request, "SEO/blogdetails.html", {'content':content,'det': bldet, "blogdeatils": blog, 'comm': bl, 'rc': blog1, 'num': num, 'cate': bcate, 'link': base_url})
    return HttpResponseRedirect("/")
    

def Createinvoice(request):
    return render(request, "Account/create-invoice.html")



@login_required(login_url='/login/')
def Blog_Comments(request):
    # blgcom=Blog_Comments
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'seo_permission':
        #sys.stdout = open("approvedblogcomment.txt", "a")
        # result = BlogComments.objects.select_related('blog').all()
        # print("Data",result)
        result1 = BlogComments.objects.all().order_by('-commentid')
        print("new data",result1)
        if request.method == 'POST':
            if "deletebutton" in request.POST:
                    commentid=request.POST.get("deletebutton")
                    print("deleteid:",commentid)
                    ostid=BlogComments.objects.get(commentid=commentid)
                    ostid.delete()
                    print("delete commentid")
            if "approved" in request.POST:
                    commentid1=request.POST.get("approved")
                    print("approved:",commentid1)
                    ostid=BlogComments.objects.filter(commentid=commentid1)
                    if ostid.exists():
                        ostid=ostid[0]
                        ostid.isapproved=True
                        ostid.rm_userid=userid
                        ostid.save(update_fields=['isapproved','rm_userid'])
                        print("update isapproved",commentid1)
        
        #sys.stdout.close()
        
        return render(request, "SEO/blog-comments.html",{'comment':result1})
    return HttpResponseRedirect("/")
    


@login_required(login_url='/login/')
def Bloginsert(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'seo_permission':
        #sys.stdout = open("bloginsert.txt", "a")
        bcate=BlogsCate.objects.all()
        if request.method == 'POST':
            name = request.POST.get("name")
            title = request.POST.get("title")
            blog_categories = request.POST.get('blogcate')
            short_discription = request.POST.get("Shortdesc")
            discription = request.POST.get('Longdesc')
            keyword=request.POST.get('keyword')
            alttext=request.POST.get('alttext')
            image=request.FILES.get('blogimage')
            titleteg=request.POST.get('titleteg')
            metadescrip=request.POST.get('metadescrip')
            urlstruct=request.POST.get('urlstruct')
            
            
            # transferfile=request.FILES.get('transferfile')
            # if transferfile is not None and len(transferfile) > 0:
            #     reader = csv.DictReader(io.TextIOWrapper(transferfile))
            #     for row in reader:
            #         rprow=Banktransfersfrompaymentgateway(paymentgatewaytype='Stripe',type=row['Type'],id=row['ID'],created=row['Created'],description=row['Description'],amount=row['Amount'],currency=row['Currency'],convertedamt=row['Converted Amount'],fees=row['Fees'],netamount=row['Net'],convertedcurrency=row['Converted Currency'],details=row['Details'])
            #         rprow.save()
            
            # csvfile=request.FILES.get('excelfile')
            # if csvfile is not None and len(csvfile) > 0:
            #     reader = csv.DictReader(io.TextIOWrapper(csvfile))
            #     for row in reader:
            #         print("innerdate",row)
            #         print("Data",row['id'])
                    
            #         rprow=Stripepayments(id=row['id'],Description=row['Description'],Seller_Message=row['Seller Message'],Created=row['Created (UTC)'],Amount=row['Amount'],Amount_Refunded=row['Amount Refunded'],Currency=row['Currency'],Converted_Amount=row['Converted Amount'],Converted_Amount_Refunded=row['Converted Amount Refunded'],Fee=row['Fee'],
            #         Tax=row['Tax'],Converted_Currency=row['Converted Currency'],Mode=row['Mode'],
            #         Status=row['Status'],Statement_Descriptor=row['Statement Descriptor'],
            #         Captured=row['Captured'],Card_ID=row['Card ID'],Card_Last4=row['Card Last4'],
            #         Card_Brand=row['Card Brand'],Card_Funding=row['Card Funding'],Card_Exp_Month=row['Card Exp Month'],
            #         Card_Exp_Year=row['Card Exp Year'],Card_Name=row['Card Name'],Card_Address_Country=row['Card Address Country'],
            #         Card_Issue_Country=['Card Issue Country'],Card_Fingerprint=row['Card Fingerprint'],
            #         Card_CVC_Status=row['Card CVC Status'],Disputed_Amount=row['Disputed Amount'],
            #         Dispute_Status=row['Dispute Status'],Dispute_Reason=row['Dispute Reason'],
            #         Dispute_Date=row['Dispute Date (UTC)'],Dispute_Evidence_Due=row['Dispute Evidence Due (UTC)'],
            #     Payment_Source_Type=row['Payment Source Type'],Is_Link=row['Is Link'],
            #     Destination=row['Destination'], Transfer=row['Transfer'],Transfer_Group=row['Transfer Group'],PaymentIntent_ID=row['PaymentIntent ID'])
            #         rprow.save()
            # print("Execute saves csv files.")
            # print("Rahul",csvfile)
            
            
            
            
            # Bl=Blog.objects.filter(title=title)
            # if Bl.exists():
            #     Bl=Bl[0]
            #     if name is not None:
            #         Bl.name=name
            #         Bl.save(update_fields=['name'])
            #     if blog_categories is not None:
            #         Bl.blog_categories=blog_categories
            #         Bl.save(update_fields=['blog_categories'])
            #     if short_discription is not None:
            #         # short_discription=markdown.markdown(short_discription)
            #         Bl.short_discription=short_discription
            #         Bl.save(update_fields=['short_discription'])
            #     if discription is not None:
            #         discription=markdown.markdown(discription)
            #         print("des",discription)
            #         Bl.discription=discription
            #         Bl.save(update_fields=['discription'])
            #     if image is not None:
            #         Bl.image=image
            #         Bl.save(update_fields=['image'])
            #     if keyword is not None:
            #         Bl.keyword=keyword
            #         Bl.save(update_fields=['keyword'])
            # else:
            # discription=markdown.markdown(discription)
            # print("dfg",discription)
            ul=Blog(name=name,title=title,alttext=alttext,blog_categories=blog_categories,short_discription=short_discription,discription=discription,image=image,keyword=keyword,title_tegs=titleteg,meta_description=metadescrip,url_structure=urlstruct)
            ul.save()
            print("insert blog")
        #sys.stdout.close()
        return render(request, "SEO/blog-insert.html",{'bcate':bcate})
    return HttpResponseRedirect("/")
    


@login_required(login_url='/login/')
def Blog_Content(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'seo_permission':
        #sys.stdout = open("bloginsert.txt", "a")
        bcate=Blog.objects.all()
        if request.method == 'POST':
            blogid = request.POST.get("blogid")
            title = request.POST.get("title")
            discription = request.POST.get('Longdesc')
            alttext=request.POST.get('alttext')       
            image=request.FILES.get('blogimage')
            blid=Blog.objects.get(blogid=blogid)
            blt=Blogcontent(blog=blid,title=title,discription=discription,image=image,alttext=alttext)
            blt.save()
            print('ibnsert blog content')
        
        
        return render(request, "SEO/blogcontent.html",{'bcate':bcate})  
    return HttpResponseRedirect("/")
    


logger = logging.getLogger()
fh = logging.FileHandler('account_view_log.txt')
logger.addHandler(fh)



#################################kyc manager function##############################
#################################kyc manager function##############################
#################################kyc manager function##############################

@login_required(login_url='/login/')
def kycdashboard(request):
    
    permissionname = request.user.userpermissions.permissionid.permission_name
    if permissionname == 'kyc_manager_permission':
        activeusers=Allusers.objects.filter(is_active=True)
        activeclients=activeusers.filter(roles='client').distinct().count()
        activeinfos=activeusers.filter(roles='influencer',influencersettings__kyc=True
).distinct().count()
        activeagency=activeusers.filter(roles='agency',agencysettings__kyc=True
).distinct().count()
        
        pendingkyc =  activeusers.filter(
    roles='influencer',influencersettings__kyc=False
).distinct().count() + activeusers.filter(
    roles='agency',agencysettings__kyc=False
).distinct().count()

        totalactiveusers=activeclients+activeinfos+activeagency+pendingkyc
        
        inforew=InfluencersReview.objects.filter(isapproved=True).count()
        peninforew=InfluencersReview.objects.filter(Q(isapproved=False) | Q(isapproved__isnull=True)).count()
        
        blogrew=BlogComments.objects.filter(isapproved=True).count()
        penblogrew=BlogComments.objects.filter(Q(isapproved=False) | Q(isapproved__isnull=True)).count()
        
        testrew=Testimonails.objects.filter(testimonails_approved=True).count()
        pentestrew=Testimonails.objects.filter(Q(testimonails_approved=False) | Q(testimonails_approved=True)).count()
        
        totalpen=peninforew+penblogrew+pentestrew
        
        totalrew=totalpen+inforew+blogrew+testrew
        
        
        return render(request, "KYC/index.html",{'totalrew':totalrew,'totalpen':totalpen,'testrew':testrew,'blogrew':blogrew,'inforew':inforew,'totalactiveusers':totalactiveusers,'pendingkyc':pendingkyc,'activeclients':activeclients,'activeinfos':activeinfos,'activeagency':activeagency})
    return HttpResponseRedirect("/")
    

###################################################################################

@login_required(login_url='/login/')
def Total_KYC_Request(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'kyc_manager_permission':
        accpro=Kycprofile.objects.get(kycid=userid)
        
        infodet=InfluencerSettings.objects.filter(Q(kyc=False) | Q(kyc=None)).order_by('-influencer_settingsid')
        #sys.stdout = open("kycrequest.txt", "a")
    
        return render(request, "KYC/total-kyc-request.html" , {'acc':accpro,'infodet':infodet})
    return HttpResponseRedirect("/")




@login_required(login_url='/login/')
def Total_KYC_Request1(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'kyc_manager_permission':
        accpro=Kycprofile.objects.get(kycid=userid)
        agencydet = UnverifedAgencyDetails.objects.filter(Q(verified=False) | Q(verified=None)).order_by('-unverifedagencydetailsid')
    
        #sys.stdout = open("kycrequest.txt", "a")
    
        return render(request, "KYC/brand-kyc-request.html" , {'acc':accpro,'agencydet':agencydet})
    return HttpResponseRedirect("/")

    
########################################################################################
@login_required(login_url='/login/')
def Brands_Lists(request):
    user = request.user
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'kyc_manager_permission':
        brandinfo=Allusers.objects.filter(is_active=True,roles='agency',agencysettings__kyc=True).order_by('-id')

        return render(request, "KYC/brands.html",{'brandinfo':brandinfo,})  

########################################################################################
@login_required(login_url='/login/')
def Creators_Lists(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'kyc_manager_permission':
        rmmapinfo=Allusers.objects.filter(is_active=True,roles='influencer',influencersettings__kyc=True).order_by('-id')

              
        return render(request, "KYC/creators.html",{'rmmapinfo':rmmapinfo,})
    

########################################################################################
@login_required(login_url='/login/')
def Clients_Lists(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'kyc_manager_permission':
        clientinfo=Allusers.objects.filter(is_active=True,roles='client',clientsettings__kyc=True).order_by('-id')

        return render(request, "KYC/client.html",{'clientinfo':clientinfo,})  

########################################################################################
@login_required(login_url='/login/')
def KYC_Profilesetting(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'kyc_manager_permission':
        lnhis=LoginIP.objects.filter(userid=userid).order_by('-LoginIPid')[:4]
        ln=Languages.objects.all()
        #sys.stdout = open("ptdt.txt", "a")
        if request.method == 'POST':
                 
            if 'profile_phone' in request.POST:
                profile_phone = request.POST.get('profile_phone')
                print("profile", profile_phone)
                pclnt = Kycprofile.objects.get(rmid=str(userid))
                if profile_phone is not None and len(profile_phone) > 1:
                    pclnt.number = profile_phone
                    print('up phone')
                pclnt.save()
                    
            elif 'new_password' in request.POST and 'confirm_password' in request.POST:

                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')

                print("new pass", new_password)
                print("sdfds", confirm_password)
                if new_password is not None and len(new_password) > 0 and new_password == confirm_password:
                    id.password = make_password(new_password)
                    id.save(update_fields=['password'])
                    print("up password")
            else:
                name = request.POST.get('name')
                image = request.FILES.get("avatar")
                emailaddress = request.POST.get('emailaddress')
                phone = request.POST.get('phone')
                pin = request.POST.get('pin')
                country = request.POST.get('country')
                address = request.POST.get('address')
                state = request.POST.get('state')
                city = request.POST.get('city')
                langlist = dict(request.POST)
                

                rmpro=Kycprofile.objects.filter(kycid=str(userid))
                if rmpro.exists():
                    rmpro=rmpro[0]
                    if name is not None and len(name) > 0:
                        rmpro.name=name
                        rmpro.save(update_fields=['name'])
                    if image is not None and len(image) > 0:
                        rmpro.profilepic=image
                        rmpro.save(update_fields=['profilepic'])
                    if address is not None and len(address) > 0:
                        rmpro.address=address
                        rmpro.save(update_fields=['address'])
                    if phone is not None and len(phone) > 0:
                        rmpro.number=phone
                        rmpro.save(update_fields=['number'])
                    if pin is not None and len(pin) > 0:
                        rmpro.pincode=pin
                        rmpro.save(update_fields=['pincode'])
                    if country is not None and len(country) > 0:
                        rmpro.country=country
                        rmpro.save(update_fields=['country'])
                    if state is not None and len(state) > 0:
                        rmpro.state=state
                        rmpro.save(update_fields=['state'])
                    if city is not None and len(city) > 0:
                        rmpro.city=city
                        rmpro.save(update_fields=['city'])
                    if emailaddress is not None and len(emailaddress) > 0:
                        id.email=emailaddress
                        id.save()
                    if "language" in langlist:
                        Language = langlist["language"]
                        print('Languga',Language)
                        if '' not in Language:
                            rmpro.languagesknown = list(Language)
                            rmpro.save(update_fields=['languagesknown'])
        
        return render(request, "KYC/profile-settings.html",{'ln':ln,'log':lnhis})
    return HttpResponseRedirect("/")
 

########################################################################################
@login_required(login_url='/login/')
def Blogshome(request, cate=None):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'kyc_manager_permission':
        blog = Blog.objects.all()
        act = request.session.get('acti', None)
        if cate is not None:
            blog = Blog.objects.filter(blog_categories__icontains=cate)

        return render(request, "KYC/bloghome.html", { "allblog": blog, })

##########################################################################################

@login_required(login_url='/login/')
def Blogsdetails(request, name):
    
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'kyc_manager_permission':
        base_url = "{0}://{1}{2}".format(request.scheme,
                                        request.get_host(), request.path)
        print("Url", base_url)

        act = request.session.get('acti', None)
        blog = Blog.objects.all()
        bcate = BlogCategory.objects.all()
        blog1 = blog.order_by('-date').values()[0:5]
        bldet = Blog.objects.filter(url_structure__icontains=name)[0]
        content=Blogcontent.objects.filter(blog=str(bldet.blogid)).order_by('blogcontentid')
        if content.exists():
            content=content
        else:
            content=''
        bl = BlogComments.objects.filter(blog=bldet, isapproved=True)
        num = len(bl)
        print("number", num)
    
        return render(request, "KYC/blogdetails.html", {'content':content,'det': bldet, "blogdeatils": blog, 'comm': bl, 'rc': blog1, 'num': num, 'cate': bcate, 'link': base_url, 'act': act})

##################################################################################################
@login_required(login_url='/login/')
def Platform_Review(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'kyc_manager_permission':
        tes = Testimonails.objects.all().order_by('id')
        if request.method == 'POST':
            if "deletebutton" in request.POST:
                    testid=request.POST.get("deletebutton")
                    print("deleteid:",testid)
                    ostid=Testimonails.objects.get(id=testid)
                    ostid.delete()
                    print("delete testimonials")
            if "approved" in request.POST:
                    test1id=request.POST.get("approved")
                    print("approved:",test1id)
                    ostid=Testimonails.objects.filter(id=test1id)
                    if ostid.exists():
                        ostid=ostid[0]
                        ostid.testimonails_approved=True
                        ostid.approveuserid=Allusers.objects.get(id=userid)
                        ostid.save(update_fields=['testimonails_approved','approveuserid'])
                        print("update testimonails_approved",test1id)
        return render(request, "KYC/platform-review.html",{'test':tes})

####################################################################################################
@login_required(login_url='/login/')
def Influencer_Review(request):
    
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'kyc_manager_permission':
        #sys.stdout = open("influencerreview.txt", "a")
        influencer_reviews = InfluencersReview.objects.values(
            "influencersreviewid",
            "review_message",
            "rating",
            "date",
            "isapproved"
        ).annotate(
            Clientname=Subquery(Allusers.objects.filter(id=OuterRef("clientid")).values("username")),
            influencername=Subquery(InfluencerProfile.objects.filter(influencer_userid=OuterRef("influencerid")).values("fullname"))
        ).order_by('-influencersreviewid')
        print("Output",influencer_reviews)
        if request.method == 'POST':
            if "deletebutton" in request.POST:
                    reviewid=request.POST.get("deletebutton")
                    print("deleteid:",reviewid)
                    ostid=InfluencersReview.objects.get(influencersreviewid=reviewid)
                    ostid.delete()
                    print("delete reviewid")
            if "approved" in request.POST:
                    reviewid1=request.POST.get("approved")
                    print("approved:",reviewid1)
                    ostid=InfluencersReview.objects.filter(influencersreviewid=reviewid1)
                    if ostid.exists():
                        ostid=ostid[0]
                        ostid.isapproved=True
                        ostid.approveuserid=Allusers.objects.get(id=userid)
                        ostid.save(update_fields=['isapproved','approveuserid'])
                        print("update isapproved",reviewid1)
        #sys.stdout.close()
        return render(request, "KYC/influencers-reviews.html",{'test':influencer_reviews})

########################################################################################################
@login_required(login_url='/login/')
def Allcastings(request):
    #sys.stdout = open("RMtotalcalling.txt", "a")
    
    # id = Allusers.objects.filter(id=rmuser)
    # id = id[0]
    # cls = Rmsettings.objects.filter(rmid=id)
    # if cls.exists():
    #     cls = cls[0]
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'kyc_manager_permission':
        result1 = Casting_Call.objects.filter(Q(approved=False) | Q(approved__isnull=True)).select_related('categoryid').annotate(
        categoryname=F('categoryid__categoryname')
        ).order_by('-castingcallid').values('categoryname','castingcallid', 'brandlogo', 'brandbanner','productimage','posttitle','approvedby','creationdate','cardcolor','approved','expirydate','brandname','postdescription','requiredplatform','compensation')
        if request.method == "POST":
            print("fgasdjf",request.POST)
            if request.POST.get("ccid1") is not None:
                postid = request.POST.get("ccid1")
                cancelreason = request.POST.get("target_details")
                print("cancel post",postid,cancelreason)
                
                pos=Casting_Call.objects.filter(castingcallid=postid)
                pos=pos[0]
                rcal=Callcastingreasons.objects.filter(callcastid=postid)
                if rcal.exists():
                    rcal=rcal[0]
                    rcal.reason=cancelreason
                    # rcal.cancelledby=cls
                    rcal.save(update_fields=['reason','cancelledby'])
                    print("Updates reason" )
                else:
                    cdf=Callcastingreasons(callcastid=pos,reason=cancelreason)
                    # ,cancelledby=cls
                    cdf.save()
                    print("Save reason")
                caldel=Casting_Call.objects.filter(castingcallid=postid)
                if caldel.exists():
                    caldel=caldel[0]
                    caldel.approved=False
                    # caldel.approvedby=cls
                    caldel.save(update_fields=['approved'])
                    Thread(target=lambda:sendagencynotification(user=caldel.clientid.id,key='agency-castingcalldecline',castingcallid=None,RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=None)).start()        
                    
                    send_customer_email(key='agency-castingcalldeclined',user_email=caldel.clientid.email,
                   client=caldel.clientid.username,influencer=None,order_id=None,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=caldel.castingcallid,brief_pitch=None,decline_reson=None) 
                        
                
    
                
            if request.POST.get("approved") is not None:
                approved = request.POST.get("approved")
                print("appovedid",approved)
                caldel=Casting_Call.objects.filter(castingcallid=approved)
                if caldel.exists():
                    caldel=caldel[0]
                    caldel.approved=True
                    # caldel.approvedby=cls
                    caldel.save(update_fields=['approved','approvedby'])
                    Thread(target=lambda:sendagencynotification(user=caldel.clientid.id,key='agency-castingcallapproved',castingcallid=None,RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=None)).start()        
                    print("approved satsu")
                    
                    
                    send_customer_email(key='agency-castingcallapproved',user_email=caldel.clientid.email,
                   client=caldel.clientid.username,influencer=None,order_id=None,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=caldel.castingcallid,brief_pitch=None,decline_reson=None) 
                        
                
    
                
        
        #sys.stdout.close()
        return render(request, "KYC/allcastingcalls.html",{'det':result1})

#############################################################################################################
@login_required(login_url='/login/')
def Activecastings(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'kyc_manager_permission':
        result1 = Casting_Call.objects.filter(approved=True).select_related('categoryid').annotate(
        categoryname=F('categoryid__categoryname')
        ).order_by('-castingcallid').values('categoryname','castingcallid', 'brandlogo', 'brandbanner','productimage','posttitle','approvedby','creationdate','cardcolor','approved','expirydate','brandname','postdescription','requiredplatform','compensation')
        return render(request, "KYC/active-call.html",{'det':result1})

#############################################################################################################
@login_required(login_url='/login/')
def BlogCommments_Status(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'kyc_manager_permission':
        result1 = BlogComments.objects.all().order_by('-commentid')
        print("new data",result1)
        if request.method == 'POST':
            if "deletebutton" in request.POST:
                    commentid=request.POST.get("deletebutton")
                    print("deleteid:",commentid)
                    ostid=BlogComments.objects.get(commentid=commentid)
                    ostid.delete()
                    print("delete commentid")
            if "approved" in request.POST:
                    commentid1=request.POST.get("approved")
                    print("approved:",commentid1)
                    ostid=BlogComments.objects.filter(commentid=commentid1)
                    if ostid.exists():
                        ostid=ostid[0]
                        ostid.isapproved=True
                        ostid.approveuserid=id
                        ostid.save(update_fields=['isapproved','approveuserid'])
                        print("update isapproved",commentid1)
        
        #sys.stdout.close()
        
        return render(request, "KYC/blog-comments.html",{'comment':result1})
    return HttpResponseRedirect("/")

#################################################################################################################
@login_required(login_url='/login/')
def Completed_KYC(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'kyc_manager_permission':
        accpro=Kycprofile.objects.get(kycid=userid)

        infodet=InfluencerSettings.objects.filter(kyc=True).order_by('-influencer_settingsid')
    
        
        return render(request, "KYC/completed-kyc.html" , {'acc':accpro,'infodet':infodet})
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def Completed_KYC1(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'kyc_manager_permission':
        accpro=Kycprofile.objects.get(kycid=userid)
        agencydet = AgencySettings.objects.filter(kyc=True).order_by('-agencysettingsid')

    
        
        return render(request, "KYC/complete-brandkyc.html" , {'acc':accpro,'agencydet':agencydet})
    return HttpResponseRedirect("/")




@login_required(login_url='/login/')
def webstoriesapproval(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    if permissionname == 'kyc_manager_permission':
        stories=Webstory.objects.all().order_by('-webstoryid')
        file_ids = set()
        for story in stories:
            file_ids.update(story.filesid)

        # Fetch all required Webstoryfiles records in a single query
        files = Webstoryfiles.objects.in_bulk(file_ids)

        # Replace the file IDs with the actual Webstoryfiles objects
        for story in stories:
            story.filesid = [files[file_id].webstoryfiles for file_id in story.filesid if file_id in files]
            
            
            
        if request.method == 'POST':
            #sys.stdout = open("approved.txt", "a")
         
            if "changeapproved" in request.POST:
                webstoryid=request.POST.get("changeapproved")
                web=Webstory.objects.get(webstoryid=webstoryid)
                web.isapproved=True
                web.aprovedby=id
                web.save()
                print('save apporved')
                Thread(target=lambda:sendInfluencernotification(user=web.userid.id,key='influencer-webstorydecline',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None)).start()
                
            if "cancelapproved" in request.POST:
                webstoryid=request.POST.get("cancelapproved")
                web=Webstory.objects.get(webstoryid=webstoryid)
                web.isapproved=False
                web.aprovedby=id
                web.save()
                print('not approved')
                Thread(target=lambda:sendInfluencernotification(user=web.userid.id,key='influencer-webstoryadded',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None)).start()
                
                    
            return redirect(request.META['HTTP_REFERER'])
        return render(request, "KYC/webstory-kyc.html",{'stories':stories})
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def get_story_by_id(request):
    webstory_id = request.GET.get('webstoryid')
    if webstory_id:
        try:
            webstory_id = int(webstory_id)
            story = Webstory.objects.filter(webstoryid=webstory_id).first()
            
            if not story:
                return JsonResponse({'error': 'No matching story found'}, status=404)
            
            # Replace the file IDs with actual file paths.
            file_urls = Webstoryfiles.objects.filter(webstoryfilesid__in=story.filesid).values_list('webstoryfiles', flat=True)
            story.filesid = list(file_urls)
            
            # Convert the story to dictionary format.
            story_data = {
                'webstoryid': story.webstoryid,
                'title': story.title,
                'filesid': story.filesid,
                'caption': story.caption,
                # ... Add other fields as needed
                'thumbnail': story.thumbnail.url if story.thumbnail else None,
                'thumnailtitle': story.thumnailtitle,
                'date':story.date,
            }
            
            return JsonResponse(story_data, safe=False)
        except ValueError:
            return JsonResponse({'error': 'Invalid webstoryid format'}, status=400)
    return JsonResponse({'error': 'webstoryid not provided'}, status=400)



############################wallet ###############################
@login_required(login_url='/login/')
def client_payout(request):
    user = request.user.id
    # print('this is the uyser',user)
    rmid=None
    try:
        channel_name = single_chat.objects.filter(user=user, channel_status=True, channel_for_RM_chat=True).values().first()['channel']
        print('this is the channel',channel_name)
        unread_messages = len(list(message.objects.filter(channel=channel_name,status=False).exclude(sender=request.user.username)))
        if unread_messages > 0:
            unread_status = True
        else:
            unread_status = False
        role = request.user.roles
        print(role)
        if role == 'client':
            rmid = ClientProfile.objects.get(client_userid=request.user.id).rmid.rmid
            rmobj = Rmprofile.objects.get(rmid=rmid)
            rmname = rmobj.name
            image = rmobj.profilepic
        elif role == 'agency':
            rmid = AgencyProfile.objects.get(agency_userid=request.user.id).rmid.rmid
            rmobj = Rmprofile.objects.get(rmid=rmid)
            rmname = rmobj.name
            image = rmobj.profilepic
        elif role == 'influencer':
            rmid = Rmtoinfluencermappings.objects.get(mappedid=request.user.id).mappedtoid
            rmname = rmid.rmid.rmprofile.name
            image = rmid.rmid.rmprofile.profilepic
    except:
        channel_name = 'None'
        unread_status = False
        image='none'
        rmname='None'
    user = request.user
    clientid=Allusers.objects.get(id=user.id)
    sys.stdout = open("offerpost.txt", "a")
    
    permissionname = user.userpermissions.permissionid.permission_name
    try:
        clientpayout=ClientPayout.objects.get(clientid=user.id)
        currency=clientpayout.currency
        if currency is None or currency =='':
            permissionname=None
                   
    except:
        permissionname=permissionname
        
    print('permi',permissionname)
        
    if permissionname == 'influencer_permission' or permissionname == 'agency_permission' or permissionname == 'client_permission' :
        clientpayout, created = ClientPayout.objects.get_or_create(clientid=clientid, defaults={
                        'remaining_balance_bank':0, 'successful_withdrawal_bank':0, 'hold_bank':0,
                       
                        })
        
        if clientpayout.currency is None or clientpayout.currency =='':
            if permissionname == 'influencer_permission':
                clientpayout.currency=request.user.influencerprofile.currency
            if permissionname == 'agency_permission':
                clientpayout.currency=request.user.agencyprofile.currency
            if permissionname == 'client_permission':
                clientpayout.currency=request.user.clientprofile.currency
            clientpayout.save()
        
        
        history=ClientPayoutHistory.objects.filter(clientid=str(user.id)).order_by('-payouthistoryid')
        requt=ClientWithdrawalRequest.objects.filter(clientid=str(user.id)).order_by('-withdrawalrequestid')
        
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
            
        try:
            if 'payout_request' in request.POST:
                print('payout_request request.POST', request.POST)
                print('curr',request.POST.get('method'),requested_currency)
                if request.POST.get('method') == 'Bank Withdrawal' and requested_currency=='INR' :
                    print('ifif')
                    requested_amount= request.POST.get('requested_amount')
                    if requested_amount is not None:
                        
                        requested_amount= float(requested_amount)
                    
                        remaining_balance_bank= clientpayout.remaining_balance_bank
                        print('requested_amount',requested_amount)
                        if requested_amount <= remaining_balance_bank or requested_amount>0:
                            print('amountBank:',request.POST.get('requested_amount'))
                            
                            addnew_clientpayoutrequest=ClientWithdrawalRequest(clientid=Allusers.objects.get(id=str(request.user.id)),
                                                                            requested_method='Bank Withdrawal',
                                                                            assigned_rm=Allusers.objects.get(id=rmid.id),
                                                                                requested_currency=requested_currency,
                                                                                requested_amount=requested_amount,
                                                                                isrefund_balance=False, isrefund_hold=True) #status=False means hold
                            addnew_clientpayoutrequest.save()
                            #     print('hold_bank:',clientpayout.hold_bank)
                            clientpayout.remaining_balance_bank-= requested_amount
                            clientpayout.hold_bank+= requested_amount
                            clientpayout.save()
                        else:
                            #show this msg on front end 
                            print('max amount that you can request is your remaining balance')
        except:
            pass        

        return render(request, "Account/wallet.html",{'requested_currency':requested_currency,'rmname':rmname,'image':image,'unread_status':unread_status,'channel_name':channel_name,'requt':requt,'history':history,'min_rerquest_limit':min_rerquest_limit})
    
    
    
    elif permissionname == None and request.user.roles=='agency':
        messages.warning(
                        request, "Please enter your country to access this page")
        return HttpResponseRedirect("/profile_setting/")
    
    elif permissionname == None and request.user.roles=='influencer':
        messages.warning(
                        request, "Please enter your country to access this page")
        return HttpResponseRedirect("/Settings/")
    elif permissionname == None and request.user.roles=='client' :
        messages.warning(
                        request, "Please enter your country to access this page")
        return HttpResponseRedirect("/Profile-Setting/")
    else:
        return HttpResponseRedirect("/")
    
    
    


def accountordersdet(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'account_permission':
        

        orderid = request.session.get('ODRID')
        paymentdet = Payments.objects.filter(ordersid=orderid)
        order_det = Orders.objects.filter(ordersid=orderid, paymentstatus=True)

        userid=str(order_det[0].influencerid)
     
        id = Allusers.objects.filter(id=userid)
        id = id[0]
      
        ac = InfluencerProfile.objects.select_related(
            'influencer_userid').filter(influencer_userid=userid)
        ac = ac[0]
        
        re = Ordercancelreasons.objects.filter(
            orderid=orderid, usersid=userid)
        ras = re
        chtme = OrderChat.objects.filter(orderid=orderid).order_by('date')
            
        print('Rahul-barawal',order_det[0].subslotid,type(order_det[0].subslotid))
        
        if order_det[0].subslotid is not None:

            sabslot = Subslots.objects.get(subslotid=str(order_det[0].subslotid.subslotid))
            zoome=zoomeet.objects.get(orderid=orderid)
        else:
            sabslot = ''
            zoome= ''
            
            
        ordreq=Ordersrequirements.objects.filter(ordersid=orderid)

        qno = Orderrequirementquestions.objects.filter(orderid=orderid)

        

        if request.method == 'POST':
            if "acceptorder" in request.POST:
                orid = request.POST.get("acceptorder")
                print("orderidaccept:", orid)
                acc = Orders.objects.filter(ordersid=orid, influencerid=userid)
                if acc.exists():
                    acc = acc[0]
                    ostid = Orderstatus.objects.filter(status='Processing')
                    if ostid.exists():
                        ostid = ostid[0]
                        acc.orderstatus = ostid
                        acc.acceptancedate = timezone.now()
                        acc.save(update_fields=[
                            'orderstatus', 'acceptancedate'])
                        # existing_user(request,name=acc.clientid.client_userid.username,user_type='existing_user',email_add=acc.clientid.client_userid.email,template_name='order-acceptance-by-influencer.html',subject='Exciting News! Your Order Has Been Accepted by '+acc.influencerid.fullname,order_no=acc.ordersid,influencer_name=acc.influencerid.fullname,completion_date=get_date_from_days(acc.planid.deliverytime))
                        Thread(target=lambda: existing_user(request, name=acc.clientid.client_userid.username, user_type='existing_user', email_add=acc.clientid.client_userid.email, template_name='order-acceptance-by-influencer.html',
                               subject='Exciting News! Your Order Has Been Accepted by '+acc.influencerid.fullname, order_no=acc.ordersid, influencer_name=acc.influencerid.fullname, completion_date=get_date_from_days(acc.planid.deliverytime))).start()
                        print("update order status", ostid)

            if "reason" in request.POST:
                reason = request.POST.get("reason")
                ostid = Orderstatus.objects.filter(status='Cancelled')
                if ostid.exists():
                    ostid = ostid[0]
                ordid = Orders.objects.filter(ordersid=orderid)
                if ordid.exists():
                    ordid = ordid[0]
                    if re.exists():
                        re = re[0]
                        re.reason = reason
                        re.save(update_fields=['reason'])
                        print("update reason")
                        ordid.orderstatus = ostid
                        ordid.cancelleddate = timezone.now()
                        ordid.save(update_fields=[
                                   'orderstatus', 'cancelleddate'])
                        print("update orderstatus with reasion update")
                    else:
                        re = Ordercancelreasons(
                            orderid=ordid, reason=reason, usersid=ac)
                        re.save()
                        print("Save reaon")
                        ordid.orderstatus = ostid
                        ordid.cancelleddate = timezone.now()
                        ordid.save(update_fields=[
                                   'orderstatus', 'cancelleddate'])
                        print("update orderstatus with reasion save")
                    # existing_user(request,name=ordid.clientid.client_userid.username,user_type='existing_user',email_add=ordid.clientid.client_userid.email,template_name='order-not-accepted.html',subject='Your Order Not Accepted by '+ordid.influencerid.fullname,order_no=ordid.ordersid,brief_explanation=reason,instruction='Contact with Customer Support')
                    Thread(target=lambda: existing_user(request, name=ordid.clientid.client_userid.username, user_type='existing_user', email_add=ordid.clientid.client_userid.email, template_name='order-not-accepted.html',
                           subject='Your Order Not Accepted by '+ordid.influencerid.fullname, order_no=ordid.ordersid, brief_explanation=reason, instruction='Contact with Customer Support')).start()

            # if "content" in request.POST:
            #     mess = request.POST.get('content')
            #     if mess is not None and len(mess) > 0:
            #         ch = OrderChat(userid=id, text=mess, orderid=order_det[0])
            #         ch.save()
            #         print("Save chat")
        return render(request, "Account/order-details.html",{'zoome':zoome, 'sabslot': sabslot, 'qno': qno, 'pymethod': paymentdet, 're': ras, 'chtme': chtme, 'order': order_det, 'info': ac, 'ordreq':ordreq })
    return HttpResponseRedirect("/")




def payout_request(request):
    sys.stdout = open("offerpost.txt", "a")
    print(1111)
    user = request.user.id
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'account_permission':
        print(2222)
        payhis=ClientWithdrawalRequest.objects.filter(rm_action=True).order_by('-withdrawalrequestid')
        
        if 'acceptorder' in request.POST:
            print(3333)
            requestid=request.POST.get('acceptorder')
            
            transactionphtoo=request.FILES.get('avatar')
            amount=float(request.POST.get('amount'))
            
            req=ClientWithdrawalRequest.objects.get(withdrawalrequestid=requestid)
            
            if transactionphtoo and amount:
                clientpayout=ClientPayout.objects.get(clientid=str(req.clientid))
                clientpayout.hold_bank-=amount
                clientpayout.successful_withdrawal_bank+=amount
                clientpayout.save()
                
                req.assigned_accountant=Allusers.objects.get(id=request.user.id)
                req.accountant_action=True
                req.transaction_screenshot=transactionphtoo
                req.transaction_amount=amount
                req.save()
        return render(request, "Account/payout-request.html",{'payhis':payhis})
    return HttpResponseRedirect("/")
    
@login_required(login_url='/login/')
def user_wallet(request):
    user = request.user.id
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'account_permission':
        userwall=ClientPayout.objects.all().order_by('-clientid__username')
        return render(request, "Account/user-wallet.html",{'userwall':userwall})
    return HttpResponseRedirect("/")



from affiliates.models import AffiliatePayoutRequest, PlatformPayoutRequest
@login_required(login_url='/login/')
def orders_purchase_log(request):
    user = request.user.id
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'account_permission':
        ordrpur=Payments.objects.all().order_by('-paymentsid')
        return render(request, "Account/order-purchase-logs.html",{'ordrpur':ordrpur})
    return HttpResponseRedirect("/")
    
@login_required(login_url='/login/')
def advertiser_txn(request):
    user = request.user.id
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'account_permission':
        
        platformpayoutrequest = PlatformPayoutRequest.objects.filter(isremoved=False).order_by('-id')
        context = {'platformpayoutrequest':platformpayoutrequest}
        return render(request, "Account/advertiser-txn.html", context)
    return HttpResponseRedirect("/")
    

@login_required(login_url='/login/')
def affiliate_txn(request):
    user = request.user.id
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'account_permission':
        affiliatepayoutrequest = AffiliatePayoutRequest.objects.all().order_by('-id')
        context={'affiliatepayoutrequest':affiliatepayoutrequest}
        return render(request, "Account/affiliate-txn.html", context)
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def wallet_txn(request):
    user = request.user.id
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'account_permission':
    
        clientpayouthistory=ClientPayoutHistory.objects.all().order_by('-payouthistoryid')
        context  = {'clientpayouthistory':clientpayouthistory}
        return render(request, "Account/wallet-txn.html", context)
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def wallet_withdrawal_req(request):
    user = request.user.id
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'account_permission':
    
        clientwithdrawalrequest=ClientWithdrawalRequest.objects.all().order_by('-withdrawalrequestid')
        context = {'clientwithdrawalrequest':clientwithdrawalrequest}
        return render(request, "Account/wallet-withdrawal-req.html", context)
    return HttpResponseRedirect("/")
    


