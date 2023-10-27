from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from mainapp.models import *
from .models import *
from threading import Thread
from Creator.models import *
from mainapp.enanddc import encrypt, decrypt
from zoomeet.models import *
from emil_send.views import existing_user
from Creator.views import get_monthly_orders
import sys
from django.contrib.auth.hashers import make_password
from Client.models import *
from Creator.views import *
from django.template.loader import render_to_string



def RM_Dashboard(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        rmmapinfo=Rmtoinfluencermappings.objects.filter(mappedtoid=str(userid))
        creatorcount=rmmapinfo.count()
        mapped_ids = rmmapinfo.values_list('mappedid', flat=True)
        totalords = Orders.objects.filter(paymentstatus=True,influencerid__influencer_userid__in=mapped_ids)
        total=totalords.count()
        pending=totalords.filter(orderstatus=5).count()
        complete=totalords.filter(orderstatus=1).count()
        active=totalords.filter(orderstatus__in=[6,7]).count()
        cancel=totalords.filter(orderstatus=3).count()
        
        
        brand1 = totalords.filter(serviceid=1)
        brand = brand1.count()
        gm1 = totalords.filter(serviceid=4)
        gm = gm1.count()
        vcs1 = totalords.filter(serviceid=2)
        vcs = vcs1.count()
        ss1 = totalords.filter(serviceid=3)
        ss2 = totalords.filter(serviceid=7)
        ss = ss1.count()+ss2.count()
        ina1 = totalords.filter(serviceid=5)
        ina = ina1.count()
            
        
        return render(request, "Relationship-Manager/index.html",
        {'ina':ina,'ss':ss,'vcs':vcs,'gm':gm,'brand':brand,'cancel':cancel,'tot':total,'active':active,'complete':complete,'pending':pending,'totalords':totalords,'creatorcount':creatorcount})
    return HttpResponseRedirect("/")
    


def RM_Completed_orders(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        rmmapinfo=Rmtoinfluencermappings.objects.filter(mappedtoid=str(userid))
        mapped_ids = rmmapinfo.values_list('mappedid', flat=True)
        totalords = Orders.objects.filter(paymentstatus=True,influencerid__influencer_userid__in=mapped_ids).order_by('-ordersid')
        total=totalords.count()
        pending=totalords.filter(orderstatus=5).count()
        active=totalords.filter(orderstatus__in=[6,7]).count()
        cancel=totalords.filter(orderstatus=3).count()
        totalords =totalords.filter(orderstatus=1) 
        complete=totalords.count()
        
        return render(request, "Relationship-Manager/completed-orders.html",{'cancel':cancel,'total':total,'rmmapinfo':rmmapinfo,'active':active,'complete':complete,'pending':pending,'totalords':totalords})
    return HttpResponseRedirect("/")
    


    
def RM_Influencer_Payment(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        rmmapinfo=Rmtoinfluencermappings.objects.filter(mappedtoid=str(userid))
        mapped_ids = rmmapinfo.values_list('mappedid', flat=True)
        totalords = Orders.objects.filter(paymentstatus=True,influencerid__influencer_userid__in=mapped_ids,orderstatus=1,isrmapproved=True).order_by('-ordersid')
        if request.method=='POST':
            if 'acceptorder' in request.POST:
                acceptorder=request.POST.get('acceptorder')
                ords=Orders.objects.get(ordersid=acceptorder)
                ords.isrmapproved=False
                ords.save()
        
        
        return render(request, "Relationship-Manager/influencer-payment.html",{'totalords':totalords})
    return HttpResponseRedirect("/")
    

def RM_Approval(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        rmmapinfo=Rmtoinfluencermappings.objects.filter(mappedtoid=str(userid))
        mapped_ids = rmmapinfo.values_list('mappedid', flat=True)
        totalords = Orders.objects.filter(paymentstatus=True,influencerid__influencer_userid__in=mapped_ids,orderstatus=1,isrmapproved=False).order_by('-ordersid')
        if request.method=='POST':
            if 'acceptorder' in request.POST:
                acceptorder=request.POST.get('acceptorder')
                ords=Orders.objects.get(ordersid=acceptorder)
                ords.isrmapproved=True
                ords.save()
        
        return render(request, "Relationship-Manager/rm-approval.html",{'totalords':totalords})
    return HttpResponseRedirect("/")
    




def RM_Pending_orders(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        rmmapinfo=Rmtoinfluencermappings.objects.filter(mappedtoid=str(userid))
        mapped_ids = rmmapinfo.values_list('mappedid', flat=True)
        totalords = Orders.objects.filter(paymentstatus=True,influencerid__influencer_userid__in=mapped_ids).order_by('-ordersid')
        total=totalords.count()
        active=totalords.filter(orderstatus__in=[6,7]).count()
        cancel=totalords.filter(orderstatus=3).count()
        complete=totalords.filter(orderstatus=1).count()
        totalords =totalords.filter(orderstatus=5) 
        pending=totalords.count()
        
        
        
        return render(request, "Relationship-Manager/pending-orders.html",{'cancel':cancel,'total':total,'rmmapinfo':rmmapinfo,'active':active,'complete':complete,'pending':pending,'totalords':totalords})
    return HttpResponseRedirect("/")
    


def RM_Active_orders(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        rmmapinfo=Rmtoinfluencermappings.objects.filter(mappedtoid=str(userid))
        mapped_ids = rmmapinfo.values_list('mappedid', flat=True)
        totalords = Orders.objects.filter(paymentstatus=True,influencerid__influencer_userid__in=mapped_ids).order_by('-ordersid')
        total=totalords.count()
        pending=totalords.filter(orderstatus=5).count()
        
        cancel=totalords.filter(orderstatus=3).count()
        complete=totalords.filter(orderstatus=1).count()       
        totalords =totalords.filter(orderstatus__in=[6, 7])  
        active=totalords.count()
        return render(request, "Relationship-Manager/active-orders.html",{'cancel':cancel,'total':total,'rmmapinfo':rmmapinfo,'active':active,'complete':complete,'pending':pending,'totalords':totalords})
    return HttpResponseRedirect("/")
    


def RM_Cancelled_orders(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        rmmapinfo=Rmtoinfluencermappings.objects.filter(mappedtoid=str(userid))
        mapped_ids = rmmapinfo.values_list('mappedid', flat=True)
        totalords = Orders.objects.filter(paymentstatus=True,influencerid__influencer_userid__in=mapped_ids).order_by('-ordersid')
        total=totalords.count()
        pending=totalords.filter(orderstatus=5).count()
        active=totalords.filter(orderstatus__in=[6,7]).count()
        complete=totalords.filter(orderstatus=1).count()
        totalords =totalords.filter(orderstatus=3) 
        cancel=totalords.count()
        return render(request, "Relationship-Manager/cancelled-orders.html",{'cancel':cancel,'total':total,'rmmapinfo':rmmapinfo,'active':active,'complete':complete,'pending':pending,'totalords':totalords})
    return HttpResponseRedirect("/")
    


def RM_Profile_Setting(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        lnhis=LoginIP.objects.filter(userid=userid).order_by('-LoginIPid')[:4]
        ln=Languages.objects.all()
        #sys.stdout = open("ptdt.txt", "a")
        if request.method == 'POST': 
            if 'profile_phone' in request.POST:
                profile_phone = request.POST.get('profile_phone')
                print("profile", profile_phone)
                pclnt = Rmprofile.objects.get(rmid=str(userid))
                if profile_phone is not None and len(profile_phone) > 1:
                    pclnt.number = profile_phone
                pclnt.save()
            elif 'new_password' in request.POST and 'confirm_password' in request.POST:
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
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
                rmpro=Rmprofile.objects.filter(rmid=str(userid))
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
        return render(request, "Relationship-Manager/profile-setting.html",{'ln':ln,'log':lnhis})
    return HttpResponseRedirect("/")
    


def RM_Influencer_Overview(request):
    #sys.stdout = open("totalorderdetails.txt", "a")
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        print('daya',request.session['infoselectid'])
        userid=request.session['infoselectid']
        ac = InfluencerProfile.objects.select_related(
            'influencer_userid').filter(influencer_userid=userid)
        ac = ac[0]
        kyc = InfluencerSettings.objects.get(influencer_userid=userid).kyc
        inforder = Orders.objects.select_related(
            'clientid', 'serviceid', 'influencerid', 'orderstatus').filter(influencerid=userid, paymentstatus=True).order_by('-ordersid')
        com = inforder.filter(orderstatus=1).count()    
        can = inforder.filter(orderstatus=3).count()
        pan = inforder.filter(orderstatus=5).count()
        act = inforder.filter(orderstatus__in=[6,7]).count()
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
        noti = Notifications.objects.filter(
            touserid=userid).order_by('-notificationid')
        conoti = noti.filter(notificationstatus=False).count()

        # #sys.stdout = open("pitch.txt", "a")
        array = []
        array1 = []
        array2 = []
        mon = get_monthly_orders(inforder)

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
        return render(request, "Relationship-Manager/influencer-overview.html",{'gis': gis, 'whychoose': whychoose, 'active': active, 'monthname': array2, 'revenue': array1, 'completed_tasks': array, 
                    'act': act, 'pan': pan, 'can': can, 'totalearn': totalearn, 'tot': tot, 'com': com,
                        'info': ac, 'kyc': kyc, 'order': inforder, 'plt': plt, 'lang': lang1, 'pro': pro, 'noti': noti, 'notcount': conoti, })
    return HttpResponseRedirect("/")
    
##################################################################################

def RM_Influencer_Setting(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        ln = Languages.objects.all()
        cate = Categories.objects.all()
        userid = request.session['infoselectid']
        username = Allusers.objects.get(id=userid).email
        id = Allusers.objects.filter(id=userid)
        id = id[0]
        permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
            userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
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
        print("categoriesid", ac.categories)
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
                if mob is not None and len(mob) > 0:
                    ac.save(update_fields=['mobile'])
                if city is not None and len(city) > 0:
                    ac.save(update_fields=['city'])
                if address is not None and len(address) > 0:
                    ac.save(update_fields=['address'])
                if aboutme is not None and len(aboutme) > 0:
                    ac.save(update_fields=['aboutme'])
                if image is not None and len(image) > 0:
                    ac.save(update_fields=['profileimage'])
                if image1 is not None and len(image1) > 0:
                    ac.save(update_fields=['profileimage1'])
                if Skills is not None and len(Skills) > 0:
                    ac.save(update_fields=['skills'])
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
                if des_title is not None and len(des_title) > 0:
                    ac.save(update_fields=['desc_title'])
                if country is not None and len(country) > 0:
                    ac.save(update_fields=['country'])
                if fe is not None and len(fe) > 0:
                    ac.save(update_fields=['fullname'])
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
        return render(request, "Relationship-Manager/influencer-setting.html",{'zipped_list':zipped_list,'shortds': shortds, 'qno': qno, 'abo': abo, 'gig': gig, 'why': why, 'exch': exch, 'user': username, 'info': ac, 'insta': instauser, 'yt': ytuser, 'tk': tkuser, 'kyc': kyc, 'lan': ln, 'ytlink': you, 'tiklink': tik, 'twilink': twi, 'fblink': fb, 'inslink': ins, 'totalearn': totalearn, 'tot': tot, 'com': com, 'noti': noti, 'notcount': conoti, 'active': request.session['active_info'], 'cate': cate, })
    return HttpResponseRedirect("/")

######################################################################################################################

def RM_Influencer_Serviceplan(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        userid = request.session['infoselectid']
        username = Allusers.objects.get(id=userid).email
        id = Allusers.objects.filter(id=userid)
        id = id[0]
        permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
            userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
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
            #sys.stdout = open("serviceplan.txt", "a")
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
            imshoutoutprice = request.POST.get('imshoutoutprice')
            greetingprice = request.POST.get('greetingprice')
            videochat = request.POST.get('videochat')
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
        return render(request, "Relationship-Manager/influencer-serviceplan.html",{ 'vc_slots': subsslots, 'vc_price': vc_price, 'gm_price': gm_price, 'event_price': event_price, 'ent': ent, 'active': request.session['active_info'], 'com': com, 'tot': tot, 'totalearn': totalearn, 'user': username, 'info': ac,  'ser': ser,'ser1':ser, 'basic': debasic, 'stand': destd, 'Prem': depre, 'sertag': stt123, 'kyc': kyc, 'noti': noti, 'notcount': conoti, 'basic1': debasic1, 'stand1': destd1, 'Prem1': depre1, 'basic2': debasic2, 'stand2': destd2, 'Prem2': depre2, })
    return HttpResponseRedirect("/")

    
def RM_Influencer_Bank(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        userid = request.session['infoselectid']
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

            return redirect(request.META['HTTP_REFERER'])
        return render(request, "Relationship-Manager/influencer-bank.html",{'active': request.session['active_info'], 'com': com, 'noti': noti, 'notcount': conoti, 'tot': tot, 'totalearn': totalearn, 'info': ac, 'pass': depass, 'pan': depan, 'addhar': deaddhar, 'cancel': decan, 'kyc': cyc, 'account': accoun, 'accnum': accno})
    return HttpResponseRedirect("/")
    
 
 
def RM_Influencer_SEO(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        userid = request.session['infoselectid']
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
        return render(request, "Relationship-Manager/influencer-seo.html",{'active': request.session['active_info'], 'totalearn': totalearn, 'tot': tot, 'com': com, 'info': ac, 'infoseo': pseo, 'kyc': kyc, 'noti': noti, 'notcount': conoti,})
    return HttpResponseRedirect("/")
    
##################################################################################################

def RM_Orders_Details(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
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
        return render(request, "Relationship-Manager/orders-details.html",{'zoome':zoome, 'sabslot': sabslot, 'qno': qno, 'pymethod': paymentdet, 're': ras, 'chtme': chtme, 'order': order_det, 'info': ac,  'ordreq':ordreq })
    return HttpResponseRedirect("/")
    
##########################################################################################

def RM_Influencers(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        rmmapinfo=Rmtoinfluencermappings.objects.filter(mappedtoid=str(userid))      
        return render(request, "Relationship-Manager/influencers.html",{'rmmapinfo':rmmapinfo,})
    return HttpResponseRedirect("/")

############################################################################################

def RMClients(request):   
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        clientinfo=ClientProfile.objects.filter(rmid=userid).order_by('-client_profile_id')[:20]
        if 'ainfoid' in request.POST:
            infoid=request.POST.get('ainfoid')
            rmselect=request.POST.get('rmselect')
            rmselect=Rmsettings.objects.get(rmid=rmselect)
            rms=ClientProfile.objects.filter(client_userid=infoid)
            if rms.exists():
                rms=rms[0]
                rms.rmid=rmselect
                rms.save(update_fields=['rmid'])
            print('update details')
        return render(request, "Relationship-Manager/clients.html",{'clientinfo':clientinfo,})
    return HttpResponseRedirect("/")

###################################################################################################
    

def rmclient_profile(request): 
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        clientselectid=request.session.get('clientselectid')
        user=clientselectid
        id = Allusers.objects.filter(id=user)
        id = id[0]
        cltdet = ClientProfile.objects.select_related('client_userid').filter(
            client_userid=int(user))
        orid = Orders.objects.filter(clientid=str(user)).last()
        logs = LoginIP.objects.filter(
            userid=user).order_by('-LoginIPid')[0:3]
        act = request.session.get('acti', None)
        exch=ExchangeRates.objects.all()
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
        return render(request, "Relationship-Manager/client-profile.html",{'exch':exch,'act': act, 'cltdet': cltdet, "orid": orid, 'log': logs, 'userdet': cltdet})
    
##################################################################################################################

def rmbrandlist(request): 
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        agencyinfo=AgencyProfile.objects.filter(rmid=userid,agency_userid__agencysettings__kyc=True).order_by('-agency_profile_id')[:20]
        if 'ainfoid' in request.POST:
            infoid=request.POST.get('ainfoid')
            rmselect=request.POST.get('rmselect')
            rmselect=Rmsettings.objects.get(rmid=rmselect)
            rms=AgencyProfile.objects.filter(agency_userid=infoid)
            if rms.exists():
                rms=rms[0]
                rms.rmid=rmselect
                rms.save(update_fields=['rmid'])
            print('update details')
    return render(request, "Relationship-Manager/brands.html",{'agencyinfo':agencyinfo,})

###################################################################################################################

def rmbrandprofile(request):
    user = request.user
    id = Allusers.objects.get(id=str(user.id))
    userid=user.id
    permissionname = user.userpermissions.permissionid.permission_name
    if permissionname == 'relationship_manager_permission':
        agencyselectid=request.session.get('agencyselectid')
        user=agencyselectid
        id = Allusers.objects.filter(id=user)
        id = id[0]
        cltdet = AgencyProfile.objects.select_related('agency_userid').filter(
            agency_userid=int(user))
        orid = Orders.objects.filter(clientid=str(user)).last()
        logs = LoginIP.objects.filter(
            userid=user).order_by('-LoginIPid')[0:3]
        act = request.session.get('acti', None)
        exch=ExchangeRates.objects.all()
        
        
        #sys.stdout = open("ptdt.txt", "a")
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
                  
        return render(request, "Relationship-Manager/brand-profile.html",{'exch':exch,'act': act, 'cltdet': cltdet, "orid": orid, 'log': logs, 'userdet': cltdet})
    


def rmordersinvoice(request,orderid=None):
    user = request.user.id
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
    
        
    if permissionname == 'relationship_manager_permission':
        
    
        return render(request, "Relationship-Manager/invoice.html",{'pay':pay,'act': act,'userdet':client_details,})
    return HttpResponseRedirect("/")
    

#############################################################################################################
def withdrawalrequest(request):
    user = request.user.id
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'relationship_manager_permission':
        
        payhis=ClientWithdrawalRequest.objects.filter(assigned_rm=request.user.id).order_by('-withdrawalrequestid')
        
        if 'acceptorder' in request.POST:
            requestid=request.POST.get('acceptorder')
            req=ClientWithdrawalRequest.objects.get(withdrawalrequestid=requestid)
            req.rm_action=True
            req.save()
        return render(request, "Relationship-Manager/withdrawal-request.html",{'payhis':payhis})
    return HttpResponseRedirect("/")
    
############################################################################################################

@login_required(login_url='/login/')
def users_wallet_info(request):
    user = request.user.id
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=user).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    if permissionname == 'relationship_manager_permission':
        
        agency_user_ids = AgencyProfile.objects.filter(rmid=user).values_list('agency_userid', flat=True)

    # Get client_userid based on rmid from ClientProfile
        client_user_ids = ClientProfile.objects.filter(rmid=user).values_list('client_userid', flat=True)

        # Get mappedid based on mappedtoid from Rmtoinfluencermappings
        mapped_ids = Rmtoinfluencermappings.objects.filter(mappedtoid=user).values_list('mappedid', flat=True)

        # Combine all results into a single list
        all_user_ids = list(agency_user_ids) + list(client_user_ids) + list(mapped_ids)
        
        
        userwall=ClientPayout.objects.filter(clientid__in=all_user_ids).order_by('-clientid__username')
        
        return render(request, "Relationship-Manager/user-wallet.html",{'userwall':userwall})
    return HttpResponseRedirect("/")
