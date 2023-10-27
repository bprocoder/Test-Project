from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from mainapp.models import *
from .models import *
from Creator.models import *
from inappnotifications.views import *
from threading import Thread
import sys
import markdown
from django.http import JsonResponse
from django.db import connection
from django.contrib.sessions.models import Session
from django.views.decorators.cache import cache_page
from django.contrib.auth.hashers import make_password
import datetime
import calendar
from Creator.views import get_monthly_orders
from django.db.models import Sum, Case, When, F, Value, IntegerField, Count,Func, DateTimeField
from django.db.models.functions import  Coalesce, ExtractMonth, ExtractDay, Concat
from django.db.models.fields import CharField


# Create your views here.

def get_orders_current_day():
    date = datetime.date.today()
    
    
    date = datetime.date(2023, 5, 4)
    
    

    # Get orders for the current date
    orders_per_day_totals = (
    Orders.objects.filter(orderdate__date=date, paymentstatus=True)
    .values('orderdate')
        .annotate(
                
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
        )
        .order_by('orderdate') 
    )
    

    # sys.stdout = open("accountdeatils.txt", "a")
    
    cdtime=[]
    cdsales=[]
    
    for ords in orders_per_day_totals:
        order_date = ords['orderdate']
        total_orders = ords['total_orders']
        total_finalamt = ords['total_finalamt']
        total_finalamtafterdiscount = ords['total_finalamtafterdiscount']
        
        print("Order Date:", order_date)
        print("Order Time:", order_date.strftime('%I:%M:%S %p')  )
        cdtime.append(order_date.strftime('%I:%M:%S %p'))
        print("Total Orders:", total_orders)
        print("Total Final Amount:", total_finalamt)
        print("Total Final Amount After Discount:", total_finalamtafterdiscount)
        cdsales.append(total_finalamt+total_finalamtafterdiscount)
        print("-----------------------------")
    
    
    return cdtime,cdsales



def get_orders_per_day_totals():
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    
    # Get the first and last day of the current month
    first_day = datetime.date(current_year, current_month, 1)
    last_day = datetime.date(current_year, current_month, 1) + datetime.timedelta(days=32)
    last_day = last_day.replace(day=1) - datetime.timedelta(days=1)
    
    # Filter orders within the date range of the current month
    orders_per_day_totals = (
        Orders.objects
        .filter(orderdate__range=[first_day, last_day],paymentstatus=True)
        .values('orderdate')
        .annotate(
              date_number_month = Concat(
                ExtractDay('orderdate'),
                Value(' '),
                           Value(calendar.month_name[current_month]),
                   output_field=CharField()
            ),
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
        )
        .order_by('orderdate')
    )
    
    # sys.stdout = open("accountdeatils.txt", "a")
    
 
    
    sum_total_orders = {}
    sum_total_finalamt = {}
    sum_total_finalamtafterdiscount = {}

    for item in orders_per_day_totals:
        date_number_month = item['date_number_month']
        total_orders = item['total_orders']
        total_finalamt = item['total_finalamt']
        total_finalamtafterdiscount = item['total_finalamtafterdiscount']
        
        sum_total_orders[date_number_month] = sum_total_orders.get(date_number_month, 0) + total_orders
        sum_total_finalamt[date_number_month] = sum_total_finalamt.get(date_number_month, 0) + total_finalamt
        sum_total_finalamtafterdiscount[date_number_month] = sum_total_finalamtafterdiscount.get(date_number_month, 0) + total_finalamtafterdiscount

    # Print the sums for each date_number_month
    
    cmdate=[""]
    cmords=[]
    cmsales=[]
    for date_number_month in sum_total_orders:
        total_orders_sum = sum_total_orders[date_number_month]
        total_finalamt_sum = sum_total_finalamt[date_number_month]
        total_finalamtafterdiscount_sum = sum_total_finalamtafterdiscount[date_number_month]
        
        print(f"Date: {date_number_month}")
        
        cmdate.append(date_number_month)
        print(f"Total Orders: {total_orders_sum}")
        cmords.append(total_orders_sum)
        print(f"Total Final Amount: {total_finalamt_sum}")
        print(f"Total Final Amount After Discount: {total_finalamtafterdiscount_sum}")
        cmsales.append(total_finalamt_sum+total_finalamtafterdiscount_sum)
        print()
    cmdate.append("")
    
    
        
    # sys.stdout.close()
    return cmdate,cmsales


def current_month_data():
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    array4 = []
    array5 = []
    order = Orders.objects.filter(orderdate__month=current_month, orderdate__year=current_year,paymentstatus=True)

    brand_cm_orders=order.filter(serviceid=1)
    brand_data = get_monthly_orders(brand_cm_orders)
    for i in brand_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt']+i['total_finalamtafterdiscount'])
    
    gm_cm_orders=order.filter(serviceid=4)
    gm_data = get_monthly_orders(gm_cm_orders)
    for i in gm_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt']+i['total_finalamtafterdiscount'])
    
    
    videochat_cm_orders=order.filter(serviceid=2)
    video_data = get_monthly_orders(videochat_cm_orders)
    for i in video_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt']+i['total_finalamtafterdiscount'])
    
    infoacq_cm_orders=order.filter(serviceid=5)
    infoqcq_data = get_monthly_orders(infoacq_cm_orders)
    for i in infoqcq_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt']+i['total_finalamtafterdiscount'])
    
    insta_cm_orders=order.filter(serviceid=7)
    insta_data = get_monthly_orders(insta_cm_orders)
    for i in insta_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt']+i['total_finalamtafterdiscount'])
    
    youtube_cm_orders=order.filter(serviceid=3)
    ytube_data = get_monthly_orders(youtube_cm_orders)
    for i in ytube_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt']+i['total_finalamtafterdiscount'])
    
    
    
    return array4, array5


def get_last_7_days_data():
    end_date = datetime.datetime.now().date()
    start_date = end_date - timedelta(days=6)
    
    array4 = []
    array5 = []
    
    order = Orders.objects.filter(orderdate__range=[start_date, end_date], paymentstatus=True)

    brand_cm_orders = order.filter(serviceid=1)
    brand_data = get_monthly_orders(brand_cm_orders)
    for i in brand_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt'] + i['total_finalamtafterdiscount'])
    
    gm_cm_orders = order.filter(serviceid=4)
    gm_data = get_monthly_orders(gm_cm_orders)
    for i in gm_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt'] + i['total_finalamtafterdiscount'])
    
    videochat_cm_orders = order.filter(serviceid=2)
    video_data = get_monthly_orders(videochat_cm_orders)
    for i in video_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt'] + i['total_finalamtafterdiscount'])
    
    infoacq_cm_orders = order.filter(serviceid=5)
    infoqcq_data = get_monthly_orders(infoacq_cm_orders)
    for i in infoqcq_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt'] + i['total_finalamtafterdiscount'])
    
    insta_cm_orders = order.filter(serviceid=7)
    insta_data = get_monthly_orders(insta_cm_orders)
    for i in insta_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt'] + i['total_finalamtafterdiscount'])
    
    youtube_cm_orders = order.filter(serviceid=3)
    ytube_data = get_monthly_orders(youtube_cm_orders)
    for i in ytube_data:
        array4.append(i['total_orders'])
        array5.append(i['total_finalamt'] + i['total_finalamtafterdiscount'])
    
    return array4, array5












# @login_required(login_url='/login/')
def Admin_Dashboard(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    array4,array5=current_month_data()
    totalorder = sum(array4)
    totalrevenue=sum(array5)
    if totalrevenue==0 :
        totalavg=0
    else:
        totalavg=totalrevenue/totalorder
    array6,array7=get_last_7_days_data()
    totalweekorder = sum(array6)
    totalweekrevenue=sum(array7)
    if totalweekrevenue==0 :
        totalavg1=0
    else:
        totalavg1=totalweekrevenue/totalweekorder
    maxdaysnum = max(totalweekorder,totalorder)
    maxmonnum = max(totalrevenue,totalweekrevenue)
    cmdate,cmsales=get_orders_per_day_totals()
    cumsales = sum(cmsales)
    ord1=Orders.objects.select_related('serviceid','influencerid','orderstatus').filter(paymentstatus=True).order_by('-ordersid')
    ord=ord1.filter(serviceid=1)[:5]
    gm=ord1.filter(serviceid=4)[:5]
    vc=ord1.filter(serviceid=2)[:5]
    ss=ord1.filter(serviceid=7)[:3].union(ord1.filter(serviceid=3)[:3])
    ias=ord1.filter(serviceid=5)[:5]
    cmdate1=cmdate
    del cmdate1[0]
    cmdtsales=zip(cmdate1, cmsales)
    cdtime,cdsales=get_orders_current_day()
    
    cdtsal=zip(cdtime[-5:][::-1], cdsales[-5:][::-1])
    
     
    array11 = []
    array12 = []
    mon = get_monthly_orders(ord1)
    for i in mon:    
        array11.append(i['total_finalamt']+i['total_finalamtafterdiscount'])
        array12.append(i['month'])
        
        
    cydtsales=zip(array11, array12)
    
    if permissionname == 'admin_permission':

        return render(request, "Super-Admin/index.html",{'cdtsal':cdtsal,
'cdsales':cdsales,'cdtime':cdtime,'cydtsales':cydtsales,'cymon':array12,'cysales':array11,'cmdtsales':cmdtsales,'ias':ias,'ss':ss,'vc':vc,'gm':gm,'ords':ord,'cumsales':cumsales,'cmdate':cmdate,'cmsales':cmsales,'maxdaysnum':maxdaysnum,'maxmonnum':maxmonnum,'totalavg1':totalavg1,'totalavg':totalavg,'totalrevenue':totalrevenue,'totalorder':totalorder,'orders':array4,'revenue':array5,'weekorders':array6,'weekrevenue':array7,'totalweekorder':totalweekorder,'totalweekrevenue':totalweekrevenue})
    return HttpResponseRedirect("/")




def my_data(request):
    data = Orders.objects.select_related(
        'clientid', 'serviceid', 'orderstatus').all().order_by('-ordersid')

    data = [{'ordersid': obj.ordersid, 'orderdate': obj.orderdate, 'serviceid_id': obj.serviceid_id, 'ordersid1': obj.ordersid,
             'orderdate1': obj.orderdate, 'serviceid_id1': obj.serviceid_id, 'serviceid_id2': obj.serviceid_id} for obj in data]
    return JsonResponse(list(data), safe=False)





def Agencies(request):
    return render(request, "Super-Admin/agencies.html")



def User_Referral(request):
    return render(request, "Super-Admin/user-referral.html")

def User_Referral_Count(request):
    return render(request, "Super-Admin/referralcount.html")


def AccountUser(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    ac_details = Accountprofile.objects.select_related(
        'accountuserid').all().order_by('-acoountprofileid')
    if permissionname == 'admin_permission':

        return render(request, "Super-Admin/account-user.html",{'acdet':ac_details})
    return HttpResponseRedirect("/")


def Account_User_Profile(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    accountid = request.session.get('ACCID')
    
    accpro=Accountprofile.objects.select_related(
        'accountuserid').filter(accountuserid=accountid)
    sys.stdout = open("accountdeatils.txt", "a")
    
    print("accoountid",accountid)
    
    if permissionname == 'admin_permission':
        if request.method == 'POST':
            image=request.FILES.get('avatar')
            name=request.POST.get('name')
            email=request.POST.get('email')
            number=request.POST.get('number')
            address1=request.POST.get('address1')
            profileid=request.POST.get('profileid')
            
            pro=Accountprofile.objects.filter(acoountprofileid=profileid)
            if pro.exists():
                pro=pro[0]
                if name is not None and len(name)>1:
                    pro.name=name
                    pro.save(update_fields=['name'])
                    print("update name")
                if image is not None and len(image)>1:
                    pro.image=image
                    pro.save(update_fields=['image'])
                    print("update image")
                if number is not None and len(number)>1:
                    pro.number=number
                    pro.save(update_fields=['number'])
                    print("update number")
                
                if address1 is not None and len(address1)>1:
                    pro.address=address1
                    pro.save(update_fields=['address'])
                    print("update address")
                    
                if email is not None and len(email)>1:
                    em=Allusers.objects.get(id=str(pro.accountuserid))
                    em.email=email
                    em.save(update_fields=['email'])
                    print("update email")
                
                    
                
            
            
            
            
            print("Rahul adate",request.POST,image)
            # return JsonResponse({'results': 'ok'})
        return render(request, "super-Admin/accountuser-profile.html",{'acc':accpro})
    sys.stdout.close()
    return HttpResponseRedirect("/")
    



def Brands(request):
    return render(request, "Super-Admin/brands.html")


def RM_List(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    rm_details = Rmprofile.objects.select_related(
        'rmid').all().order_by('-profileid')[0:11]
    if permissionname == 'admin_permission':
        return render(request, "Super-Admin/rm.html", {"rm_details": rm_details})
    return HttpResponseRedirect("/")


def Managers(request):
    return render(request, "Super-Admin/managers.html")


def Account_Info(request):
    return render(request, "Super-Admin/accounts-info.html")


def Welcome_Message(request):
    return render(request, "Super-Admin/welcome-message.html")


def Reset_Password_Message(request):
    return render(request, "Super-Admin/reset-password.html")


def Orders_Confirmed_Message(request):
    return render(request, "Super-Admin/orders-confirmed.html")


def Card_Declined_Message(request):
    return render(request, "Super-Admin/card-declined.html")


def Promotions_Email1(request):
    return render(request, "Super-Admin/promotions-email1.html")


def Promotions_Email2(request):
    return render(request, "Super-Admin/promotions-email2.html")


def Promotions_Email3(request):
    return render(request, "Super-Admin/promotions-email3.html")


def Blogs_Home_Admin(request, cate=None):
    blog = Blog.objects.all()
    if cate is not None:
        blog = Blog.objects.filter(blog_categories__icontains=cate)

    return render(request, "super-Admin/blog-home.html", {"allblog": blog})


def Blogs_Post_Admin(request, name):
    name = name.replace('-', ' ')
    print(name)
    base_url = "{0}://{1}{2}".format(request.scheme,
                                     request.get_host(), request.path)
    print("Url", base_url)

    blog = Blog.objects.all()
    bcate = BlogCategory.objects.all()
    blog1 = blog.order_by('-date').values()[0:5]
    bldet = Blog.objects.filter(title__icontains=name)[0]
    print("sdagf", bldet)
    bl = BlogComments.objects.filter(blog=bldet, isapproved=True)
    num = len(bl)
    print("number", num)

    return render(request, "super-Admin/blog-post.html", {'det': bldet, "blogdeatils": blog, 'comm': bl, 'rc': blog1, 'num': num, 'cate': bcate, 'link': base_url, })


def Data_Charts(request):
    return render(request, "super-Admin/charts.html")


def PageWise_SEOContent(request):
    pagewise=Seo_Settings.objects.all()
    return render(request, "super-Admin/page-wiseseo.html",{'pageseo':pagewise})


def Change_SEOSetting (request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    seoid=request.session.get('SEOID')
    seoset=Seo_Settings.objects.filter(seoid=seoid)
    if permissionname == 'admin_permission':
        if request.method == 'POST':
            sys.stdout = open("totalorderdetails.txt", "a")
            title=request.POST.get('title')
            description=request.POST.get('description')
            keyword=request.POST.get('keyword')
            print("data",title,description,keyword)
            if seoset.exists():
                seoset1=seoset[0]
                if title is not None and len(title) > 0:
                    seoset1.title=title
                    seoset1.save(update_fields=['title'])
                if description is not None and len(description) > 0:
                    seoset1.description=description
                    seoset1.save(update_fields=['description'])
                if keyword is not None and len(keyword) > 0:
                    seoset1.keyword=keyword 
                    seoset1.save(update_fields=['keyword'])
            return JsonResponse({'result': 'ok'})
        return render(request, "super-Admin/change-seosetting.html",{'seo':seoset})
    return HttpResponseRedirect("/")
    




def All_Page_SEOContent(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    
    seo=Seo_Content.objects.all()
    
    
    if permissionname == 'admin_permission':
        if request.method == 'POST':
            sys.stdout = open("totalorderdetails.txt", "a")
            robots=request.POST.get('robots')
            Googlesiteverification=request.POST.get('Googlesiteverification')
            twittercard=request.POST.get('twittercard')
            twittersite=request.POST.get('twittersite')
            twittercreator=request.POST.get('twittercreator')
            twittertitle=request.POST.get('twittertitle')
            twitterimg=request.POST.get('twitterimg')
            twitterimgalt=request.POST.get('twitterimgalt')
            twitterplayer=request.POST.get('twitterplayer')
            twitterplayerwidth=request.POST.get('twitterplayerwidth')
            twitterplayerheight=request.POST.get('twitterplayerheight')
            fbappid=request.POST.get('fbappid')
            ogtitle=request.POST.get('ogtitle')
            ogurl=request.POST.get('ogurl')
            ogimgurl=request.POST.get('ogimgurl')
            ogimgtype=request.POST.get('ogimgtype')
            ogimgwidth=request.POST.get('ogimgwidth')
            ogimgheight=request.POST.get('ogimgheight')
            ogtype=request.POST.get('ogtype')
            oglocale=request.POST.get('oglocale')
            ogimageurl=request.POST.get('ogimageurl')
            ogimagesecureurl=request.POST.get('ogimagesecureurl')
            ogsitename=request.POST.get('ogsitename')
            ogseealso=request.POST.get('ogseealso')
            
            articleauthor=request.POST.get('articleauthor')
            formatdetection=request.POST.get('formatdetection')
            
           
            if seo.exists():
                seo1=seo[0]
                if robots is not None and len(robots) > 0:
                    seo1.robot=robots
                    seo1.save(update_fields=['robot'])
                if Googlesiteverification is not None and len(Googlesiteverification) > 0:
                    seo1.google_site_verification=Googlesiteverification
                    seo1.save(update_fields=['google_site_verification'])
                if twittercard is not None and len(twittercard) > 0:
                    seo1.twitter_card=twittercard
                    seo1.save(update_fields=['twitter_card'])
                if twittersite is not None and len(twittersite) > 0:
                    seo1.twitter_site=twittersite
                    seo1.save(update_fields=['twitter_site'])
                if twittercreator is not None and len(twittercreator) > 0:
                    seo1.twitter_creator=twittercreator
                    seo1.save(update_fields=['twitter_creator'])
                if twittertitle is not None and len(twittertitle) > 0:
                    seo1.twitter_title=twittertitle
                    seo1.save(update_fields=['twitter_title'])
                if twitterimg is not None and len(twitterimg) > 0:
                    seo1.twitter_image_url=twitterimg
                    seo1.save(update_fields=['twitter_image_url'])
                if twitterimgalt is not None and len(twitterimgalt) > 0:
                    seo1.twitter_image_alt=twitterimgalt
                    seo1.save(update_fields=['twitter_image_alt'])
                if twitterplayer is not None and len(twitterplayer) > 0:
                    seo1.twitter_player=twitterplayer
                    seo1.save(update_fields=['twitter_player'])
                if twitterplayerwidth is not None and len(twitterplayerwidth) > 0:
                    seo1.twitter_player_width=twitterplayerwidth
                    seo1.save(update_fields=['twitter_player_width'])
                if twitterplayerheight is not None and len(twitterplayerheight) > 0:
                    seo1.twitter_player_height=twitterplayerheight
                    seo1.save(update_fields=['twitter_player_height'])
                if fbappid is not None and len(fbappid) > 0:
                    seo1.fb_app_id=fbappid
                    seo1.save(update_fields=['fb_app_id'])
                if ogtitle is not None and len(ogtitle) > 0:
                    seo1.og_title=ogtitle
                    seo1.save(update_fields=['og_title'])
                if ogurl is not None and len(ogurl) > 0:
                    seo1.og_url=ogurl
                    seo1.save(update_fields=['og_url'])
                if ogimgurl is not None and len(ogimgurl) > 0:
                    seo1.og_img_url=ogimgurl
                    seo1.save(update_fields=['og_img_url'])
                if ogimgtype is not None and len(ogimgtype) > 0:
                    seo1.og_img_type=ogimgtype
                    seo1.save(update_fields=['og_img_type'])
                if ogimgwidth is not None and len(ogimgwidth) > 0:
                    seo1.og_img_width=ogimgwidth
                    seo1.save(update_fields=['og_img_width'])
                if ogimgheight is not None and len(ogimgheight) > 0:
                    seo1.og_img_height=ogimgheight
                    seo1.save(update_fields=['og_img_height'])
                if ogtype is not None and len(ogtype) > 0:
                    seo1.og_type=ogtype
                    seo1.save(update_fields=['og_type'])
                if oglocale is not None and len(oglocale) > 0:
                    seo1.og_locale=oglocale
                    seo1.save(update_fields=['og_locale'])
                if ogimageurl is not None and len(ogimageurl) > 0:
                    seo1.og_image_url=ogimageurl
                    seo1.save(update_fields=['og_image_url'])
                if ogimagesecureurl is not None and len(ogimagesecureurl) > 0:
                    seo1.og_img_secure_url=ogimagesecureurl
                    seo1.save(update_fields=['og_img_secure_url'])
                if ogsitename is not None and len(ogsitename) > 0:
                    seo1.og_site_name=ogsitename
                    seo1.save(update_fields=['og_site_name'])
                if ogseealso is not None and len(ogseealso) > 0:
                    seo1.og_see_also=ogseealso
                    seo1.save(update_fields=['og_see_also'])
                if articleauthor is not None and len(articleauthor) > 0:
                    seo1.aticle_author=articleauthor
                    seo1.save(update_fields=['aticle_author'])
                if formatdetection is not None and len(formatdetection) > 0:
                    seo1.format_detecation=formatdetection
                    seo1.save(update_fields=['format_detecation'])
        return render(request, "super-Admin/allpageseo.html",{'seo':seo})
    return HttpResponseRedirect("/")


def Data_Tables(request):
    return render(request, "super-Admin/tables.html")


def Data_Mixed(request):
    return render(request, "super-Admin/mixed.html")


def Account_Setting(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    infoid = request.session.get('INFOID')
    infoid = 57
    
    info = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=infoid)
    
    langu=Languages.objects.all()
    
    
    
    oderct=Orders.objects.filter(influencerid=infoid)
    otl=oderct.count()
    comp=oderct.filter(orderstatus=1).count()
    succ=(comp/otl)*100
    earn=request.session.get('EARN')
    platids = PlatformDetails.objects.filter(
        usersid=id).values_list('platformdetailid', flat=True)
    if permissionname == 'admin_permission':
        if request.method == 'POST':
            sys.stdout = open("influencerinfo.txt", "a")
            if 'emailaddress' in request.POST and 'emailaddress1' in request.POST:
                email=request.POST.get('emailaddress')
                email1=request.POST.get('emailaddress1')
                print("Email",email)
                print("Email 1",email1)
                if email == email1:
                    print("equal email")
                    em=Allusers.objects.filter(id=infoid)
                    if em.exists():
                        em=em[0]
                        em.email=email
                        em.save(update_fields=['email'])
                        print("update email")
            elif 'deactivate' in request.POST:
                deactivate=request.POST.get('deactivate')
                if deactivate is not None and deactivate == '0':
                    em=Allusers.objects.filter(id=infoid)
                    if em.exists():
                        em=em[0]
                        em.is_active=False
                        # em.save(update_fields=['is_active'])
                        print("update is_active")
                    # print("Barwal")
                
                
                
            else:
                print(request.POST)
                profileimage=request.FILES.get('avatar')
                profileimage1=request.FILES.get('avatar1')
                name=request.POST.get('fname')
                emal=request.POST.get('email')
                phone=request.POST.get('phone')
                country=request.POST.get('country')
                state=request.POST.get('state')
                city=request.POST.get('city')
                address=request.POST.get('address')
                skill=request.POST.get('skill')
                tag=request.POST.get('tag')
                timezone=request.POST.get('timezone')
                currnecy=request.POST.get('currnecy')
                instausername=request.POST.get('instausername')
                youtubeid=request.POST.get('youtubeid')
                tiktokusername=request.POST.get('tiktokusername')
                link=request.POST.get('link')
                language=request.POST.get('language')
                short_des=request.POST.get('short_des')
                aboutme=request.POST.get('aboutme')
                
                
                if info.exists():
                    info=info[0]
                    info.fullname = name
                    info.desc_title = tag
                    info.short_description = short_des
                    info.skills = skill
                    info.profileimage = profileimage
                    info.mobile = phone
                    info.currency = currnecy
                    info.country = country
                    info.address = address
                    info.aboutme = aboutme
                    info.state = state
                    info.city = city
                    info.profileimage1=profileimage1
                    
                    
                    if phone is not None and len(phone) > 0:
                        info.save(update_fields=['mobile'])
                        print("update phone")
                    
                    if state is not None and len(state) > 0:
                        info.save(update_fields=['state'])
                        print("update state")
                    if city is not None and len(city) > 0:
                        info.save(update_fields=['city'])
                        print("update city")
                    if address is not None and len(address) > 0:
                        info.save(update_fields=['address'])
                        print("update address")
                    if aboutme is not None and len(aboutme) > 0:
                        info.save(update_fields=['aboutme'])
                        print("update aboutme")
                    if profileimage is not None and len(profileimage) > 0:
                        info.save(update_fields=['profileimage'])
                        
                        print("update image")
                    if profileimage1 is not None and len(profileimage1) > 0:
                        info.save(update_fields=['profileimage1'])
                        print("Update Cover Photo")
                    if skill is not None and len(skill) > 0:
                        info.save(update_fields=['skills'])
                        print("update skills")
                    if currnecy is not None and len(currnecy) > 0:
                        info.save(update_fields=['currency'])
                        print("update currency")
                    if short_des is not None and len(short_des) > 0:
                        info.save(update_fields=['short_description'])
                        print("update short_description")
                    if tag is not None and len(tag) > 0:
                        info.save(update_fields=['desc_title'])
                        print("update desc_title")
                    if country is not None and len(country) > 0:
                        info.save(update_fields=['country'])
                        print("update country")
                    if name is not None and len(name) > 0:
                        info.save(update_fields=['fullname'])
                        print("update fullname")
                    
                    if platids.exists():
                        info.platformdetails = list(platids)
                        if platids is not None and len(platids) > 0:
                            info.save(update_fields=['platformdetails'])
                            print("paltform insert")
                    
                
                
                if link is not None and len(link) > 0: 
                    ppl = PlatformProfileLink.objects.filter(
                        usersid=infoid, platformtype='Youtube')
                    if ppl.exists():
                        ppl = ppl[0]
                        ppl.profilelink = link
                        ppl.save(update_fields=['profilelink'])
                        print("update youtube link")
                    else:
                        ppl = PlatformProfileLink(
                            platformtype='Youtube', usersid=infoid, profilelink=link)
                        ppl.save()
                        print("Save youtube link")
                
                if len(instausername) > 0 and instausername is not None:
                    pltformid = Platforms.objects.get(
                        platform_name='Instagram').platformid
                    pd = PlatformDetails.objects.filter(
                        usersid=infoid, platformtype=pltformid)
                    if pd.exists():
                        pd = pd[0]
                        pd.platformcredential = instausername
                        # pd.subscribers_followers=instagramdata(instagram)
                        pd.save(update_fields=['subscribers_followers'])
                        print("instgram followers update")
                    else:
                        dp = PlatformDetails()
                        dp.usersid = infoid
                        dp.platformtype = pltformid
                        dp.platformcredential = instausername
                        # dp.subscribers_followers=instagramdata(instagram)
                        dp.additiontime = datetime.now()
                        dp.save()
                        print("insert instagram")
            
                if len(youtubeid) > 0 and youtubeid is not None:
                    pltformid = Platforms.objects.get(
                        platform_name='Youtube').platformid
                    pd = PlatformDetails.objects.filter(
                        usersid=infoid, platformtype=pltformid)
                    if pd.exists():
                        # fetchytdetails(youtubeid, id, pltformid)
                        print("youtube followers update")
                    else:
                        # fetchytdetails(youtubeid, id, pltformid)
                        print("youtube update")
                    
                if len(tiktokusername) > 0 and tiktokusername is not None:
                    pltformid = Platforms.objects.get(
                        platform_name='Tiktok').platformid
                    pd = PlatformDetails.objects.filter(
                        usersid=infoid, platformtype=pltformid)
                    if pd.exists():
                        pd = pd[0]
                        pd.platformcredential = tiktokusername
                        # pd.subscribers_followers=titikusersdet(tiktok,id,pltformid)
                        pd.save(update_fields=[
                                'subscribers_followers', 'platformcredential'])
                        print("Tiktok followers update")
                
                if len(emal) > 0 and emal is not None:
                    au = Allusers.objects.filter(id=infoid)
                    if au.exists():
                        au = au[0]
                        au.email = emal
                        au.save(update_fields=['email'])
                        print("update email")
                
                # if instagramlink is not None:
                #     ppl = PlatformProfileLink.objects.filter(
                #         usersid=id, platformtype='Instagram')
                #     if ppl.exists():
                #         ppl = ppl[0]
                #         ppl.profilelink = instagramlink
                #         ppl.save(update_fields=['profilelink'])
                #         print("update instgram link")
                #     else:
                #         ppl = PlatformProfileLink(
                #             platformtype='Instagram', usersid=id, profilelink=instagramlink)
                #         ppl.save()
                #         print("Save instagram link")
                
                
                
                
                print(profileimage,name,emal,phone,country,state,city,address,skill,tag,timezone,currnecy,instausername,youtubeid,tiktokusername,link,short_des,aboutme)
                
                
                
                print("execute")
            sys.stdout.close()
            
            return JsonResponse({'result': 'ok'})
        return render(request, "super-Admin/setting.html",{'info':info,'orct':otl,'rate':succ,'earn':earn,'langu':langu})
    return HttpResponseRedirect("/")


def Account_Security(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    infoid = request.session.get('INFOID')
    infoid = 57
    username = Allusers.objects.get(id=str(infoid)).username
    logs = LoginIP.objects.filter(
        username=username).order_by('-LoginIPid')[0:6]
    
    info = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=infoid)
    oderct=Orders.objects.filter(influencerid=infoid)
    otl=oderct.count()
    comp=oderct.filter(orderstatus=1).count()
    succ=(comp/otl)*100
    earn=request.session.get('EARN')
    
    if permissionname == 'admin_permission':
        
        return render(request, "super-Admin/security.html",{'info':info,'orct':otl,'rate':succ,'logs':logs,'earn':earn})
    return HttpResponseRedirect("/")
       

def Account_Activity(request):
    return render(request, "super-Admin/activity.html")


def Account_Billing(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    infoid = request.session.get('INFOID')
    infoid = 57
    info = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=infoid)
    oderct=Orders.objects.filter(influencerid=infoid)
    otl=oderct.count()
    comp=oderct.filter(orderstatus=1).count()
    succ=(comp/otl)*100
    earn=request.session.get('EARN')
    order_details = Orders.objects.select_related(
        'clientid', 'serviceid', 'orderstatus').filter(orderstatus=1).order_by('-ordersid')
    if permissionname == 'admin_permission':
    
    
    
        return render(request, "super-Admin/billing.html",{'info':info,'orct':otl,'rate':succ,'earn':earn,'orders':order_details})
    return HttpResponseRedirect("/")


def Account_Statement(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    infoid = request.session.get('INFOID')
    infoid = 57
    info = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=infoid)
    oderct=Orders.objects.filter(influencerid=infoid)
    otl=oderct.count()
    comp=oderct.filter(orderstatus=1).count()
    succ=(comp/otl)*100
    earn=request.session.get('EARN')
    
    if permissionname == 'admin_permission':
    
        return render(request, "super-Admin/statement.html",{'info':info,'orct':otl,'rate':succ,'earn':earn})
    return HttpResponseRedirect("/")
    


def Account_Referrals(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    infoid = request.session.get('INFOID')
    infoid = 57
    info = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=infoid)
    oderct=Orders.objects.filter(influencerid=infoid)
    otl=oderct.count()
    comp=oderct.filter(orderstatus=1).count()
    succ=(comp/otl)*100
    earn=request.session.get('EARN')
    if permissionname == 'admin_permission':
    
        return render(request, "super-Admin/referrals.html",{'info':info,'orct':otl,'rate':succ,'earn':earn})
    return HttpResponseRedirect("/")
    


def Account_Logs(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    infoid = request.session.get('INFOID')
    infoid = 57
    username = Allusers.objects.get(id=str(infoid)).username
    logs = LoginIP.objects.filter(
        username=username).order_by('-LoginIPid')
    info = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=infoid)
    oderct=Orders.objects.filter(influencerid=infoid)
    otl=oderct.count()
    comp=oderct.filter(orderstatus=1).count()
    succ=(comp/otl)*100
    earn=request.session.get('EARN')
    
    if permissionname == 'admin_permission':
        return render(request, "super-Admin/logs.html",{'info':info,'orct':otl,'rate':succ,'log':logs,'earn':earn})
    return HttpResponseRedirect("/")
    


# @login_required(login_url='/login/')
def Creators(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    influencer_details = InfluencerProfile.objects.select_related(
        'influencer_userid').all().order_by('-influencer_profile_id')[0:11]
    if permissionname == 'admin_permission':
        return render(request, "Super-Admin/creators.html", {'info': influencer_details})
    return HttpResponseRedirect("/")


@cache_page(60)
def Total_Orders(request):

    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    sys.stdout = open("totalorderdetails.txt", "a")
    order_details = Orders.objects.select_related(
        'clientid', 'serviceid', 'orderstatus').all().order_by('-ordersid')[0:100]
    print("Data", order_details, type(order_details))
    sys.stdout.close()
    if permissionname == 'admin_permission':
        return render(request, "super-Admin/total-orders.html", {'order': order_details})
    return HttpResponseRedirect("/")


def Completed_Orders(request):

    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    sys.stdout = open("totalorderdetails.txt", "a")
    order_details = Orders.objects.select_related(
        'clientid', 'serviceid', 'orderstatus').all().order_by('-ordersid')
    sys.stdout.close()
    if permissionname == 'admin_permission':
        return render(request, "super-Admin/completed-orders.html", {'order': order_details})
    return HttpResponseRedirect("/")


def Pendings_Orders(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    sys.stdout = open("totalorderdetails.txt", "a")
    order_details = Orders.objects.select_related(
        'clientid', 'serviceid', 'orderstatus').all().order_by('-ordersid')
    sys.stdout.close()
    if permissionname == 'admin_permission':
        return render(request, "super-Admin/pending-orders.html", {'order': order_details})
    return HttpResponseRedirect("/")


def Cancelled_Orders(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    sys.stdout = open("totalorderdetails.txt", "a")
    order_details = Orders.objects.select_related(
        'clientid', 'serviceid', 'orderstatus').all().order_by('-ordersid')
    sys.stdout.close()
    if permissionname == 'admin_permission':
        return render(request, "super-Admin/cancelled-orders.html", {'order': order_details})
    return HttpResponseRedirect("/")


def Orderdet(request):
    if request.method == 'POST':
        sys.stdout = open("totalorderdetails.txt", "a")
        request.session['ODRID'] = request.POST.get('orderid')
        print("AJAX")
        print(request.session['ODRID'])
        sys.stdout.close()
        return JsonResponse({'results': 'ok'})
    
    
def infoselectid(request):
    if request.method == 'POST':
        request.session['infoselectid'] = request.POST.get('orderid')
        return JsonResponse({'results': 'ok'})
    
    
def infoselectid2(request):
    if request.method == 'POST':
        request.session['infoselectid2'] = request.POST.get('orderid')
        return JsonResponse({'results': 'ok'})
    
    
    
    
    
    
    
def infoselectid1(request):
    if request.method == 'POST':
        request.session['infoselectid1'] = request.POST.get('orderid')
        return JsonResponse({'results': 'ok'})
    

def Kycapproved(request):
    
    
    if request.method == 'POST':
        sys.stdout = open("totalorderdetails.txt", "a")
        infoapproveid= request.POST.get('orderid')
        print('infoid',infoapproveid,type(infoapproveid))
        
                
        if infoapproveid != 0 or infoapproveid != '0':
            cursor = connection.cursor()
            cursor.execute('call kycvalidation(%s)',(infoapproveid,))
            notices = connection.connection.notices  # This is the correct way to access the notices.
            print('notice',notices,type(notices))
            
            if notices[0]=="NOTICE:  Kyc verified\n":
                mangeids=Allusers.objects.filter(roles='manager')
                for i in mangeids:
                    infoname=Allusers.objects.get(id=infoapproveid).username
                    sendmanagernotification(user=i.id,key='manager-influencerisregitered',client_id=None,client_name=None,influencer_name=infoname)
                    print('execute')
                
                sendInfluencernotification(user=infoapproveid,key='influencer-kyccomplete',RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=None,reason=None)
            
            cursor.close()
            connection.close()
            print('inner')
        print('execuete')
        return JsonResponse({'results': notices})
    
    
    
def Disablekyc(request):
    
    
    if request.method == 'POST':
        sys.stdout = open("totalorderdetails.txt", "a")
        infoapproveid= request.POST.get('orderid')
        print('infoid',infoapproveid,type(infoapproveid))
        
                
        if infoapproveid != 0 or infoapproveid != '0':
            try:
                inf=InfluencerSettings.objects.get(influencer_userid=infoapproveid)
                inf.kyc=False
                inf.save()
            except:
                pass
            print('inner')
        print('execuete')
        return JsonResponse({'results': 'ok'})
    
    
    
    
def Roleapproved(request):
    if request.method == 'POST':
        sys.stdout = open("totalorderdetails.txt", "a")
        infoapproveid= request.POST.get('orderid')
        
        print('execute notif' )
        print('clientid',infoapproveid,type(infoapproveid))
                
        if infoapproveid != 0 or infoapproveid != '0':
            cursor = connection.cursor()
            cursor.execute('call usersroleupdation(%s,%s,%s)',(infoapproveid,'client','agency'))       
            notices = connection.connection.notices 
            print('notice',notices)
            cursor.close()
            connection.close()
            try:
                vers1=AgencySettings.objects.get(asettingsuserid=str(infoapproveid))
                vers1.kyc=True
                vers1.save() 
                vers=UnverifedAgencyDetails.objects.get(clientid=str(infoapproveid))
                vers.verified=True
                vers.save()
                Thread(target=lambda:sendagencynotification(user=infoapproveid,key='agency-rolechagetoagency',castingcallid=None,RM_Name=None,Influencer_Name=None,Product_Name=None,Decline_Reason=None,Order_Id=None)).start()        
                
                
                mangeids=Allusers.objects.filter(roles='manager')
                info=Allusers.objects.get(id=infoapproveid)
                noti=notification.objects.filter(user=str(infoapproveid))
                noti.delete()
                
                infoname=info.username
                for i in mangeids:
                    Thread(target=lambda:sendmanagernotification(user=i.id,key='manager-userbecomesagency',client_id=infoapproveid,client_name=infoname,influencer_name=None)).start()
                    
                RM_Name = info.rmprofile.rmid.username
                
                send_customer_email(key='client-newrmassigned',user_email=info.email,
                   client=infoname,influencer=None,order_id=None,service_type=None,
            order_start_date=None,order_end_date=None,rm=RM_Name,casting_call_id=None,brief_pitch=None,decline_reson=None) 
                
                                
                send_customer_email(key='client-rolechangedtoagencysucessfully',user_email=info.email,
                   client=infoname,influencer=None,order_id=None,service_type=None,
            order_start_date=None,order_end_date=None,rm=None,casting_call_id=None,brief_pitch=None,decline_reson=None) 
                
                            
                print('inner')
               
                
                
            except:
                pass
        print('execuete')
        return JsonResponse({'results': notices})
    
    


def Clientselectid(request):
    if request.method == 'POST':
        request.session['clientselectid'] = request.POST.get('orderid')
        return JsonResponse({'results': 'ok'})
    


def Clientselectid2(request):
    if request.method == 'POST':
        request.session['clientselectid2'] = request.POST.get('orderid')
        return JsonResponse({'results': 'ok'})

def bankselectid(request):
    if request.method == 'POST':
        request.session['bankselectid'] = request.POST.get('orderid')
        return JsonResponse({'results': 'ok'})
    
    
from mainapp.enanddc import  decrypt
from django.core import serializers
    
    
def bankdetselectid(request):
    if request.method == 'POST':
        id = request.POST.get('orderid')
        accoun = Useraccounts.objects.get(usersid=id)
        accoun.accountnumber = decrypt(accoun.accountnumber)
        docs = UserDocuments.objects.get(usersid=id,documentname="Cancel Cheque")
        
        # Serialize both querysets to JSON
        accoun_data = serializers.serialize('json', [accoun])
        docs_data = serializers.serialize('json', [docs])  # Remove the [ ] around docs
        
        # Create a dictionary with both serialized querysets
        response_data = {
            'results': accoun_data,
            'docs': docs_data,
        }
        
        return JsonResponse(response_data)
    
    

def Clientselectid1(request):
    if request.method == 'POST':
        request.session['clientselectid1'] = request.POST.get('orderid')
        return JsonResponse({'results': 'ok'})
    



def Agencyselectid(request)    :
    if request.method == 'POST':
        request.session['agencyselectid'] = request.POST.get('orderid')
        return JsonResponse({'results': 'ok'})
    

def Agencyselectid1(request)    :
    if request.method == 'POST':
        request.session['agencyselectid1'] = request.POST.get('orderid')
        return JsonResponse({'results': 'ok'})
    

def delwish(request):
    if request.method == 'POST':
        sys.stdout = open("totalorderdetails.txt", "a")
        wishid = request.POST.get('wishid')
        whobj=Wishlist.objects.get(wishlistid=str(wishid))
        whobj.delete()
        sys.stdout.close()
        return JsonResponse({'results': 'ok'})
    
def delCart(request):
    if request.method == 'POST':
        sys.stdout = open("totalorderdetails.txt", "a")
        cartid = request.POST.get('cartid')
        whobj=Cart.objects.get(Cartid=str(cartid))
        whobj.delete()
        sys.stdout.close()
        return JsonResponse({'results': 'ok'})

def orderres(request):
    if request.method == 'POST':
        sys.stdout = open("totalorderdetails.txt", "a")
        ordi = request.POST.get('orderid')
        print("AJAX")
        orres=Ordercancelreasons.objects.filter(orderid=ordi)[0]
        data = {
        'ordercancelreasons': orres.reason,
        'canceldate':orres.cancellationdate.strftime("%Y-%m-%d %I:%M %p"),
    }
        print('data',data)
        sys.stdout.close()
        return JsonResponse({'results': data})
    
    

def orderinv(request):
    if request.method == 'POST':
        sys.stdout = open("totalorderdetails.txt", "a")
        request.session['INVID'] = request.POST.get('orderid')
        sys.stdout.close()
        return JsonResponse({'results': 'ok'})
    


def Account_Overview(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    infoid = request.session.get('INFOID')
    infoid = 57
    info = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=infoid)
    
    print("Lnaguge")
    lang=info[0].language
    plat=info[0].platformdetails
    
    lang1=[]
    for i in lang:
        ln=Languages.objects.get(languageid=i)
        lang1.append(str(ln.languages))
    
    
    print(lang1)
    print("Platform")
    plt=[]
    for j in plat:
        pt=PlatformDetails.objects.get(platformdetailid=j)
        plt.append((str(pt.platformtype),str(pt.platformcredential)))

    pro=PlatformProfileLink.objects.filter(usersid=infoid)

    oderct=Orders.objects.filter(influencerid=infoid)
    otl=oderct.count()
    comp=oderct.filter(orderstatus=1).count()
    succ=(comp/otl)*100
    infoset=InfluencerSettings.objects.get(influencer_userid=infoid)
    sys.stdout = open("Overview.txt", "a")
    
    inforder= Orders.objects.select_related(
        'clientid', 'serviceid', 'influencerid', 'orderstatus').filter(influencerid=infoid,paymentstatus=True)
    
    com = inforder.filter(orderstatus=1).count()
    can = inforder.filter(orderstatus=3).count()
    pan = inforder.filter(orderstatus=5).count()
    act = inforder.filter(orderstatus=6).count()
    tot = inforder.count()
    
    mon=get_monthly_orders(inforder)
    print("data",mon)
    
    array=[]
    array1=[]
    array2=[]
    for i in mon:
        array.append(i['total_orders'])
        array1.append(i['total_finalamt']+i['total_finalamtafterdiscount'])
        array2.append(i['month'])
    
    # array=[5500, 7500, 6000, 7800, 2200, 8500, 8800, 5500, 7500, 6000, 7800, 2200]
    # array1=[5500, 7500, 6000, 7800, 2200, 8500, 8800, 5500, 7500, 6000, 7800, 2200]
    # array2=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    
    
    totalern=0
    for i in inforder:
        print("Data",i.couponcodeid,type(i.couponcodeid))
        if isinstance(i.couponcodeid, int) and i.couponcodeid != 0:
            cd=Couponcodes.objects.get(couponcodesid=i.couponcodeid).coupondiscount
            if i.orderamt == None or i.orderamt == 0 :
                orderamt=0
                i.orderamt=orderamt
            else:
                disamt=(cd/100)*i.orderamt
                i.orderamt=i.orderamt-disamt
        if i.orderamt is not None or i.orderamt == 0 :
            totalern=totalern+i.orderamt
        print("rate",totalern)
    request.session['EARN']=totalern
        
        
        
        
        
    sys.stdout.close()
    
    
    if permissionname == 'admin_permission':

        return render(request, "super-Admin/overview.html", {'monthname':array2,'revenue':array1,'completed_tasks':array,'act':act,'pan':pan,'com':com,'can':can,'tot':tot,'info': info,'setting':infoset,'lang':lang1,'plt':plt,'pro':pro,'orct':otl,'rate':succ,'oder':inforder,'earn':totalern})
    return HttpResponseRedirect("/")






def Accountdet(request):
    if request.method == 'POST':
        request.session['ACCID'] = request.POST.get('account')
        return JsonResponse({'results': 'ok'})




def Clientdet(request):
    if request.method == 'POST':
        request.session['CLIID'] = request.POST.get('client')
        print(request.session['CLIID'])
        return JsonResponse({'results': 'ok'})
    
    
def Seoid(request):
    if request.method == 'POST':
        request.session['SEOID'] = request.POST.get('seo')
        return JsonResponse({'results': 'ok'})
    
def Rmdet(request):
    if request.method == 'POST':

        request.session['RMID'] = request.POST.get('client')
        print(request.session['RMID'])
        return JsonResponse({'results': 'ok'})


def Infodetails(request):
    if request.method == 'POST':

        request.session['INFOID'] = request.POST.get('client')
        print(request.session['INFOID'])
        return JsonResponse({'results': 'ok'})


def Clients(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    sys.stdout = open("totalorderdetails.txt", "a")
    clidet = ClientProfile.objects.select_related(
        'client_userid').all().order_by('-client_profile_id')[0:200]

    sys.stdout.close()
    if permissionname == 'admin_permission':

        return render(request, "Super-Admin/clients.html", {'clit': clidet})
    return HttpResponseRedirect("/")


def Clients_Details(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']

    clientid = request.session.get('CLIID')
    sys.stdout = open("totalorderdetails.txt", "a")
    clientid = 95773

    username = Allusers.objects.get(id=str(clientid)).username
    logs = LoginIP.objects.filter(
        username=username).order_by('-LoginIPid')[0:6]

    clidet = ClientProfile.objects.select_related(
        'client_userid').filter(client_userid=clientid).all()
    order = Orders.objects.select_related(
        'influencerid', 'serviceid').filter(clientid=clientid)
    completedorder = order.filter(orderstatus=1)
    penorder = order.filter(orderstatus=5)
    proorder = order.filter(orderstatus=6)
    canorder = order.filter(orderstatus=3)

    print("Orders", completedorder)

    if permissionname == 'admin_permission':

        if request.method == 'POST':
            # or=request.POST.get('orderid')
            print("requesy", request.POST)

            if 'profile_email' in request.POST:
                email = request.POST.get('profile_email')
                userid = request.POST.get('preid')
                print("hello", request.POST.get('profile_email'), userid)
                if email is not None and len(email) > 1:
                    clus = Allusers.objects.filter(id=str(userid))
                    if clus.exists():
                        clus = clus[0]
                        clus.email = email
                        clus.save(update_fields=['email'])
                        print("upadte email")
                return JsonResponse({'result': 'ok'})

            elif 'new_password' in request.POST:

                curpass = request.POST.get('current_password')
                paas = request.POST.get('new_password')
                conpass = request.POST.get('confirm_password')
                userid = request.POST.get('preid1')
                print("hello", request.POST.get('new_password'), userid)
                if curpass is not None and len(curpass) > 1:
                    curpass = make_password(curpass)
                    clus = Allusers.objects.filter(id=str(userid))
                    if clus.exists():
                        clus = clus[0]
                        paas1 = clus.password
                        if paas1 == curpass and paas == conpass:
                            clus.password = make_password(conpass)
                            clus.save(update_fields=['password'])
                        print("upadte password")
                return JsonResponse({'result': 'ok'})

            elif 'user_role' in request.POST:

                userrole = request.POST.get('user_role')
                # cursor = connection.cursor()
                if userrole == '3':
                    newrole = 'influencer'
                elif userrole == '1':
                    newrole = 'brand'
                elif userrole == '2':
                    newrole = 'agency'
                else:
                    newrole = 'client'

                clus = Allusers.objects.filter(id=str(clientid))
                if clus.exists():
                    clus = clus[0]
                    role = clus.roles
                    # cursor.execute('call usersroleupdation(%s,%s,%s)',
                    #                (clientid, role, newrole))
                    # user = cursor.fetchall()

                # cursor.close()

                print("hello", request.POST.get(
                    'user_role'), clientid, newrole, role)

                return JsonResponse({'result': 'ok'})

            elif 'profile_mobile' in request.POST:
                phone = request.POST.get('profile_mobile')
                print("hello", request.POST.get('profile_mobile'), clientid)
                if phone is not None and len(phone) > 1:
                    clus = ClientProfile.objects.filter(
                        client_userid=str(clientid))
                    if clus.exists():
                        clus = clus[0]
                        clus.mobile = phone
                        clus.save(update_fields=['mobile'])
                        print("upadte mobile")
                return JsonResponse({'result': 'ok'})

            else:

                name = request.POST.get('name')
                email = request.POST.get('email')
                address1 = request.POST.get('address1')
                city = request.POST.get('city')
                state = request.POST.get('state')
                postcode = request.POST.get('postcode')
                country = request.POST.get('country')
                profileid = request.POST.get('profileid')
                photo = request.FILES.get("avatar")

                print("Dat", name, email, address1, city,
                      state, postcode, country, profileid)

                etprof = ClientProfile.objects.filter(
                    client_profile_id=profileid)
                if etprof.exists():
                    etprof = etprof[0]
                    if name is not None and len(name) > 1:
                        etprof.fullname = name
                        etprof.save(update_fields=['fullname'])
                        print("upadte fullnmae")
                    if address1 is not None and len(address1) > 1:
                        etprof.address = address1
                        etprof.save(update_fields=['address'])
                        print("upadte address")
                    if city is not None and len(city) > 1:
                        etprof.city = city
                        etprof.save(update_fields=['city'])
                        print("upadte city")
                    if state is not None and len(state) > 1:
                        etprof.state = state
                        etprof.save(update_fields=['state'])
                        print("upadte staete")
                    if postcode is not None and len(postcode) > 1:
                        etprof.postalcode = postcode
                        etprof.save(update_fields=['postalcode'])
                        print("upadte pincode")
                    if country is not None and len(country) > 1:
                        etprof.country = country
                        etprof.save(update_fields=['country'])
                        print("upadte country")
                    if photo is not None and len(photo) > 1:
                        etprof.profileimage = photo
                        etprof.save(update_fields=['profileimage'])
                        print("upadte profileimage")

                    userid = etprof.client_userid
                    if email is not None and len(email) > 1:
                        clus = Allusers.objects.filter(id=str(userid))
                        if clus.exists():
                            clus = clus[0]
                            clus.email = email
                            clus.save(update_fields=['email'])
                            print("upadte email")
            return render(request, "super-Admin/clientuser-profile.html", {"cltdet": clidet, 'total': order, 'Comp': completedorder, 'Pen': penorder, 'Pro': proorder, 'Can': canorder, 'logses': logs})
        sys.stdout.close()
        return render(request, "super-Admin/clientuser-profile.html", {"cltdet": clidet, 'total': order, 'Comp': completedorder, 'Pen': penorder, 'Pro': proorder, 'Can': canorder, 'logses': logs})
    return HttpResponseRedirect("/")


def Orders_Details(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    sys.stdout = open("totalorderdetails.txt", "a")
    orderid = request.session.get('ODRID')
    order_details = Orders.objects.select_related(
        'clientid', 'serviceid', 'influencerid', 'orderstatus').filter(ordersid=orderid)
    paymentdet = Payments.objects.filter(ordersid=orderid)
    cltdet = ClientProfile.objects.get(
        client_userid=int(order_details[0].clientid.id))

    # request.session['ODRID']=''
    if permissionname == 'admin_permission':

        print("id of order", orderid)
        return render(request, "super-Admin/orders-details.html", {'order': order_details, 'pymethod': paymentdet, 'cli': cltdet})
    sys.stdout.close()
    return HttpResponseRedirect("/")




def Brand_User_Overview(request):
    return render(request, "super-Admin/brand-overview.html")




def Brand_Profile_Setting(request):
    return render(request, "super-Admin/brandprofile-setting.html")


def Brand_Project(request):
    return render(request, "super-Admin/brand-project.html")


def Brand_Campaigns(request):
    return render(request, "super-Admin/brand-campaigns.html")


def Brand_Activity(request):
    return render(request, "super-Admin/brand-activity.html")


def Brand_Billing(request):
    return render(request, "super-Admin/brand-billing.html")


def Brand_Statement(request):
    return render(request, "super-Admin/brand-statement.html")


def Brand_Security(request):
    return render(request, "super-Admin/brand-security.html")


def Clients_Total_Orders(request):
    return render(request, "super-Admin/client-total-orders.html")


def Clients_Completed_Orders(request):
    return render(request, "super-Admin/client-completed-orders.html")


def Clients_Pendings_Orders(request):
    return render(request, "super-Admin/client-pendings-orders.html")


def Clients_Cancelled_Orders(request):
    return render(request, "super-Admin/client-cancelled-orders.html")


def Private_Chats(request):
    return render(request, "super-Admin/chats.html")


def Groups_Chats(request):
    return render(request, "super-Admin/groups-chats.html")


def Roles_List(request):
    return render(request, "super-Admin/roles-list.html")


def View_Roles(request):
    return render(request, "super-Admin/view-roles.html")


def Agency_Overview(request):
    return render(request, "super-Admin/agency-overview.html")


def Agency_Setting(request):
    return render(request, "super-Admin/agency-setting.html")


def Agency_Security(request):
    return render(request, "super-Admin/agency-security.html")


def Agency_Activity(request):
    return render(request, "super-Admin/agency-activity.html")


def Agency_Billing(request):
    return render(request, "super-Admin/agency-billing.html")


def Agency_Statement(request):
    return render(request, "super-Admin/agency-statement.html")


def Agency_Project(request):
    return render(request, "super-Admin/agency-project.html")


def Agency_Campaigns(request):
    return render(request, "super-Admin/agency-campaigns.html")


def Calendar(request):
    return render(request, "super-Admin/calendar.html")


def RM_Overview(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    sys.stdout = open("rmdetails.txt", "a")

    rmid = request.session.get('RMID')
    print("RM", rmid)
    sys.stdout.close()
    if permissionname == 'admin_permission':
        return render(request, "super-Admin/rm-overview.html")
    return HttpResponseRedirect("/")


def RM_Setting(request):
    return render(request, "super-Admin/rm-setting.html")


def RM_Security(request):
    return render(request, "super-Admin/rm-security.html")


def RM_Activity(request):
    return render(request, "super-Admin/rm-activity.html")


def RM_Brand(request):
    return render(request, "super-Admin/rm-brand.html")


def RM_Creators(request):
    return render(request, "super-Admin/rm-creator.html")


def RM_Clients(request):
    return render(request, "super-Admin/rm-client.html")


def RM_Agencies(request):
    return render(request, "super-Admin/rm-agency.html")


def Manager_Overview(request):
    return render(request, "super-Admin/manager-overview.html")


def Manager_Setting(request):
    return render(request, "super-Admin/manager-setting.html")


def Manager_Security(request):
    return render(request, "super-Admin/manager-security.html")


def Manager_Activity(request):
    return render(request, "super-Admin/manager-activity.html")


def Manager_Brand(request):
    return render(request, "super-Admin/manager-brand.html")


def Manager_Creators(request):
    return render(request, "super-Admin/manager-creators.html")


def Manager_Clients(request):
    return render(request, "super-Admin/manager-client.html")


def Manager_Agencies(request):
    return render(request, "super-Admin/manager-agency.html")


def Manager_RM(request):
    return render(request, "super-Admin/manager-rm.html")


def Upload_Requirments(request):
    jd = Jobhiring.objects.all().order_by('-jobhiringid')
    if request.method == 'POST':
        sys.stdout = open("uploadrequirementsform.txt", "a")
        jobtitle = request.POST.get('jobtitle')
        designation = request.POST.get('designation')
        location = request.POST.get('location')
        about = request.POST.get('about')
        rules = request.POST.get('rules')
        profile = request.POST.get('profile')
        if rules is not None and len(rules) > 5:
            rules = rules.split(". ")
        if profile is not None and len(profile) > 5:
            profile = profile.split(". ")
        print(jobtitle, designation, location, about, rules, profile,)
        if jobtitle is not None and designation is not None and location is not None and about is not None and rules is not None and profile is not None:
            jb = Jobhiring(jobtitle=jobtitle, designation=designation, joblocation=location,
                           aboutthejob=about, rulesandresponsibilities=rules, desiredcandidateprofile=profile)
            jb.save()
            print("job insereted")
        sys.stdout.close()
    return render(request, "super-Admin/upload-requirements.html", {"job": jd})

# @login_required(login_url='/login/')


def deletejob(request, jobid):
    deljd = Jobhiring.objects.get(jobhiringid=jobid)
    deljd.delete()
    return redirect(request.META['HTTP_REFERER'])


# @login_required(login_url='/login/')
def deleteemprew(request, rwid):
    deljd = EmployeeReview.objects.get(employeereviewid=rwid)
    deljd.delete()
    return redirect(request.META['HTTP_REFERER'])




def Interested_Candidates(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    acd=Appliedcandidates.objects.select_related(
        'jobhiringid').all()
    count=acd.count()
    if permissionname == 'admin_permission':
    
    
        return render(request, "super-Admin/interested-candidates.html",{'app':acd,'count':count})
    return HttpResponseRedirect("/")
    

def SEO_Influencer(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
        userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
    infoid = request.session.get('INFOID')
    infoid = 57
    
    info = InfluencerProfile.objects.select_related(
        'influencer_userid').filter(influencer_userid=infoid)
    
    infoseo=InfluencerSeoSettings.objects.filter(influencer_userid=infoid)
    
    oderct=Orders.objects.filter(influencerid=infoid)
    otl=oderct.count()
    comp=oderct.filter(orderstatus=1).count()
    succ=(comp/otl)*100
    earn=request.session.get('EARN')
    if permissionname == 'admin_permission':
        if request.method == 'POST':
            title = request.POST.get('title')
            discription = request.POST.get('discription')
            keyword = request.POST.get('keyword')
            
            inf=InfluencerSeoSettings.objects.filter(influencer_userid=infoid)
            if inf.exists():
                inf=inf[0]
                if title is not None and len(title)>0:
                    inf.title=title
                    inf.save(update_fields=['title'])
                    print("update title")
                if discription is not None and len(discription)>0:
                    inf.description=discription
                    inf.save(update_fields=['description'])
                    print("update description")
                if keyword is not None and len(keyword)>0:
                    inf.keyword=keyword
                    inf.save(update_fields=['keyword'])
                    print("update keyword")
        return render(request, "super-Admin/influencer-seo.html",{'info':info,'orct':otl,'rate':succ,'earn':earn,'infoseo':infoseo})
    return HttpResponseRedirect("/")


def Upload_Blogs(request):
    return render(request, "super-Admin/insert-blog.html")


def Total_Blog_List(request):
    er = Blog.objects.all().order_by('-blogid').values()

    if request.method == 'POST':
        sys.stdout = open("fetchblog.txt", "a")
        target_title = request.POST.get('target_title')
        target_title1 = request.POST.get('target_title1')
        target_title2 = request.POST.get('target_title2')
        target_title3 = request.POST.get('target_title3')
        target_title4 = request.POST.get('target_title4')
        photo = request.FILES.get("avatar")
        blogs_id = request.POST.get('blogs-id')

        Bl = Blog.objects.filter(blogid=blogs_id)
        if Bl.exists():
            Bl = Bl[0]
            if target_title2 is not None:
                Bl.name = target_title2
                Bl.save(update_fields=['name'])
            if target_title is not None:
                Bl.blog_categories = target_title
                Bl.save(update_fields=['blog_categories'])
            if target_title3 is not None:
                # short_discription=markdown.markdown(short_discription)
                Bl.short_discription = target_title3
                Bl.save(update_fields=['short_discription'])
            if target_title4 is not None:
                discription = markdown.markdown(target_title4)
                print("des", discription)
                Bl.discription = discription
                Bl.save(update_fields=['discription'])
            if photo is not None:
                Bl.image = photo
                Bl.save(update_fields=['image'])
            if target_title1 is not None:
                Bl.title = target_title1
                Bl.save(update_fields=['title'])

        print("data", target_title, target_title1,
              target_title2, target_title3, target_title4, photo)
        sys.stdout.close()
        return redirect(request.META['HTTP_REFERER'])
    return render(request, "super-Admin/total-blog-list.html", {'blogs': er})


def fetchblog(request):

    if request.method == 'POST':

        if request.POST.get('blogid') != None:
            blogid = request.POST.get('blogid')
            print("blogid", blogid)
        queryset = Blog.objects.filter(blogid=blogid).values()

    return JsonResponse(list(queryset), safe=False)


def Employee_Review(request):
    userid = request.user.id
    id = Allusers.objects.filter(id=userid)
    id = id[0]
    er = EmployeeReview.objects.all().order_by('-employeereviewid')
    if request.method == 'POST':
        sys.stdout = open("employee-review.txt", "a")
        photo = request.FILES.get("avatar")
        employeename = request.POST.get('employeename')
        description = request.POST.get('description')
        department = request.POST.get('department')
        message = request.POST.get('message')

        if photo is not None and employeename is not None and len(employeename) > 2 and description is not None and len(description) > 2 and department is not None and len(department) > 2 and message is not None and len(message) > 2:
            rwer = EmployeeReview(userid=id, employeename=employeename, employeedesgination=description,
                                  employeedepartment=department, employeemessage=message, employeeimage=photo)
            rwer.save()
            mess = "Yout review is successfully submitted."
            tag = 'success'
            print("Employee data", photo, employeename,
                  description, department, message)
        else:
            mess = "Some Information is missing or incomplete."
            tag = 'danger'
        sys.stdout.close()
        return JsonResponse({'message': mess, 'tags': tag})
    return render(request, "super-Admin/employee-review.html", {'emreview': er})

