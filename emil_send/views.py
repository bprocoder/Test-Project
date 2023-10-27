from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf.global_settings import *
from pathlib import Path
import os
from email.mime.image import MIMEImage
import requests
import json, time
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def user(request):
    # created list of html templates we have in influencer-mail folder
    file_path = str(Path(__file__).resolve().parent.parent/'emil_send/templates')
    files = os.listdir(str(Path(__file__).resolve().parent.parent/'emil_send/templates'))
    templates = []
    for item in files:
        if item[-4:] == 'html' and item != 'user.html':
            templates.append(item)
    
    templates.sort()
    template_path = []
    for tem in templates:
        tem_path = os.path.join(file_path, tem)
        template_path.append(tem_path)
    
    return render(request, 'user.html', {'templates': templates, 'temp_path':template_path})


def send_mail(request):
    user_type = request.POST.get('user_type')
    if user_type == 'new_user':
        return new_user(request)
    else:
        return existing_user(request)

#################################
# variables

cart_checkout_link = 'https://www.influencerhiring.com/kart'
reactivation_link = 'https://www.influencerhiring.com/reactivation'
# verification_link = 'https://www.influencerhiring.com/verification'
benefits = "wll get 100% off for first 2 services"
violation_description = 'you have coilated the guidelines'
suspension_duration = '5 year'
instructions_for_appeal_process = 'beg for mercy'
discount_code = "ABBC5040"
discount = '40%'
offer_validity = '1 Month'
event_data = '20/02/2024'
event_time = '18:00'
event_vanue = 'Bol7 Noida'
rspv_link = 'https://www.influencerhiring.com/RSPV'
promotion_validity = '30days'
feedback_link = 'https://www.influencerhiring.com/feedback'
password_reset_link = 'https://www.influencerhiring.com/password-reset'
specific_niche = 'Fashion'
brand_name = 'BOL7'
campaign_theme = 'will meet and discuss further'
campaign_goal = 'give overview of the product'
list_of_benifits_and_incentives_for_selected_influencers = '<ol><li>wiill get extra money</li><br><ol>can get 2 or more brand promotion</ol></ol>'
casting_call_date = '20/03/2032'
casting_call_vanue = 'Bol7 Delhi'
order_no = '007'
order_date = '20/4/2022'
order_total = '2 orders'
payment_amount = '$2k'
payment_method = 'UPI'
influencer_name = 'carryminati'
completion_date = '20/05/2023'
spacial_request = 'A'
tracking_no = '001'
brief_of_work = 'WIP'
delivery_date = '20/05/2023'
dispute_description = 'N/A'
dispute_status = "Ongoing"
dispute_resolve_steps = 'please specify'
brief_explanation = 'Product is not working as specified'
instruction = 'get going and inform the PR'
refund_amount = '$0k'
refund_method = 'Bank Transfer'
expected_refund_date = '20/06/2023'
reward_details = 'iPhone 9'
start_date = '30/03/2024'
end_date = '31/03/2024'
discount_category = 'Fashion, cosmetics'
product = 'get your subscriber'

################################

new_user_templates = ['new-user-registration.html','welcome-email.html','account-verification.html']

def existing_user(request,name=None,user_type=None,email_add=None,template_name=None,subject=None,password_reset_link=None,order_date=None,order_no=None,influencer_name=None,completion_date=None,spacial_request=None,brief_explanation=None,instruction=None,tracking_no=None,payment_amount=None,payment_method=None):
    # time.sleep(30)
    # name = request.POST.get('name')
    # user_type = request.POST.get('user_type')
    # email_add = request.POST.get('email')
    # template_name = request.POST.get('temp')
    if template_name in new_user_templates:
        return HttpResponse('<div><h1>You are already registerd please login!!</h1></div>')
    else:
        template =  render_to_string(template_name, 
                                    {'user_name':name, 
                                    'cart_checkout_link':cart_checkout_link, 
                                    'reactivation_link':reactivation_link,
                                    'benefits':benefits,
                                    'violation_description':violation_description,
                                    'suspension_duration':suspension_duration,
                                    'instructions_for_appeal_process':instructions_for_appeal_process,
                                    'discount_code':discount_code,
                                    'discount':discount,
                                    'offer_validity':offer_validity,
                                    'event_data':event_data,
                                    'event_time':event_time,
                                    'event_vanue':event_vanue,
                                    'rspv_link':rspv_link,
                                    'promotion_validity':promotion_validity,
                                    'feedback_link':feedback_link,
                                    'password_reset_link':password_reset_link,
                                    'specific_niche':specific_niche,
                                    'brand_name':brand_name,
                                    'campaign_theme':campaign_theme,
                                    'campaign_goal':campaign_goal,
                                    'list_of_benifits_and_incentives_for_selected_influencers':list_of_benifits_and_incentives_for_selected_influencers,
                                    'casting_call_date':casting_call_date,
                                    'casting_call_vanue':casting_call_vanue,
                                    'order_no':order_no,
                                    'order_date':order_date,
                                    'order_total':order_total,
                                    'payment_amount':payment_amount,
                                    'payment_method':payment_method,
                                    'influencer_name':influencer_name,
                                    'completion_date':completion_date,
                                    'spacial_request':spacial_request,
                                    'tracking_no':tracking_no,
                                    'brief_of_work':brief_of_work,
                                    'delivery_date':delivery_date,
                                    'dispute_description':dispute_description,
                                    'dispute_status':dispute_status,
                                    'dispute_resolve_steps':dispute_resolve_steps,
                                    'brief_explanation':brief_explanation,
                                    'instruction':instruction,
                                    'refund_amount':refund_amount,
                                    'refund_method':refund_method,
                                    'expected_refund_date':expected_refund_date,
                                    'reward_details':reward_details,
                                    'start_date':start_date,
                                    'end_date':end_date,
                                    'discount_category':discount_category,
                                    'product':product,
                                    })
        # text_content = strip_tags(template)
        email = EmailMultiAlternatives(subject,template,settings.EMAIL_HOST_USER,[email_add])
        email.attach_alternative(template, "text/html")
        # adding image in email template
        img_dir = str(Path(__file__).resolve().parent.parent/'mainapp/static/images')
        
        image_list = ["youtube.png","icon-facebook.png","icon-linkedin.png","icon-twitter.png","instagram.png"]
        for image in image_list:
            file_path = os.path.join(img_dir, image)
            img_type = image[-3:]
            with open(file_path, 'rb') as f:
                img = MIMEImage(f.read(), _subtype=img_type)
                img.add_header('Content-ID','<{name}>'.format(name=image))
                img.add_header('Content-Disposition', 'inline', filename=image)
            email.attach(img)
            
        email.send()
        
        return HttpResponse(f'<div><h1> Hi {name} please check your email this is {user_type}!!</h1><br></div>')

def new_user(request,name=None,user_type=None,email_add=None,template_name=None,subject=None,verification_link=None):
    #########
    # defined variables
    # account_varification_link = 'https://www.influencerhiring.com/varify'
    #########
    # name = request.POST.get('name')
    # user_type = request.POST.get('user_type')
    # email_add = request.POST.get('email')
    # template_name = request.POST.get('temp')
    
    if template_name not in new_user_templates:
        return HttpResponse('<div><h1>You are Not registerd please register!!</h1></div>')
    else:
        template = render_to_string(template_name, {'user_name':name,
                                                    'verification_link':verification_link,
                                                    })
        # text_content = strip_tags(template)
        email = EmailMultiAlternatives(subject,template,settings.EMAIL_HOST_USER,[email_add])
        email.attach_alternative(template, "text/html")
        # adding image in email template
        img_dir = str(Path(__file__).resolve().parent.parent/'mainapp/static/images')
        
        image_list = ["youtube.png","icon-facebook.png","icon-linkedin.png","icon-twitter.png","instagram.png"]
        for image in image_list:
            file_path = os.path.join(img_dir, image)
            img_type = image[-3:]
            with open(file_path, 'rb') as f:
                img = MIMEImage(f.read(), _subtype=img_type)
                img.add_header('Content-ID','<{name}>'.format(name=image))
                img.add_header('Content-Disposition', 'inline', filename=image)
            email.attach(img)
            
        email.send()
        
        return HttpResponse(f'<div><h1> Hi {name} please check your email this is {user_type}!!</h1><br></div>')




