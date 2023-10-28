

from django.contrib import admin
from django.urls import path, include
from mainapp.views import *
from Creator.views import *
from Account.views import *
from Admin.views import *
from Client.views import *
from RM.views import *
from Agency.views import *
from Manager.views import *
from Payment.views import *
from Razor.views import *
from paypalapp.views import *
from affiliates.views import *
from pdf_validation_app.views import home1, generate_qr_code, validate_pdf_document,my_view
from django.views.generic.base import TemplateView
from zoomeet.views import *
from pushnotificationapp.views import *
from whatsapp_login.views import whatsapplogin
from inappnotifications.views import *
from emil_send.views import *
from mainapp.backgroundfunctions import topcreator
from marketingapp.views import *
# from django.shortcuts import redirect


from django.conf import settings
from django.conf.urls.static import serve
from django.urls import re_path
from agora_chat.views import *
from whatsapp_login.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    #For Site-Map
    path('sitemap.xml', site),
    path('htaccess.txt', HttsView.as_view(), name='htaccess_file'),
    path('topcreator/',topcreator),
    
    # path('robots.txt/', read_file),
    path('robots.txt', RobotsView.as_view(), name='robots_file'),
    
    path('', include('emil_send.urls')),
    # Adding social auth path
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('convertrates/', convertrates, name='convertrates'),
    # For Influencer or Normal User Admin
    path('', Index, name='home'),
    path('wishlist/', whishlist, name='wishlist'),
    path('mywishlist/', mywishlist, name='mywishlist'),
    path('delmywhishlist/', delmywhishlist, name='delmywhishlist'),
    path('delmycart/', delmycart, name='delmycart'),
    path('mycart/', mycart, name="mycart"),
    path('delwhishlist/', delwhishlist, name='delwhishlist'),
    path('influencers/wishlist/', whishlist),
    path('influencers/delwhishlist/', delwhishlist),
    path('checkbox/', box),
    path('checkbox1/', cbox),
    path('cate/', cate),
    path('catbox/', catbox),
    

    
    path('activate/<str:uidb64>/<str:token>/',activate, name='activate'),
    path('resendactivatelink/<str:username>/',resendactivatelink ),
    path('about/', About),
    path('faq/', Faq),
    path('Package-Details/<str:username>/', Package),
    path('activationlink/', Activationlink),
    # 
    path('influencerchat/<str:username>/', Influencer_Chat),
    # path('Influencer-Chat/', Influencer_Chat),
    path('PackagePlan/', PackagePlan, name="package"),
    path('EventPlan/', EventPlan, name="event"),
    path('my-data/', my_data, name="my_data"),
    path('Shoutout-Details/<str:username>/', Shoutout_Payment),
    path('VideochatPrice/', VideochatPrice, name="VideochatPrice"),
    path('Videochatrecord/', Videochatrecord, name="Videochatrecord"),
    path('Videochattime/', Videochattime, name="Videochattime"),
    path('influencer/<str:username>/', Services1,name='fetch'),
    path('influencer/', ServicePostid, name="service"),
    path('actype/', Actypeid, name="actype"),
    path('shoutservice/', Shoutservice, name="shoutservice"),
    path('Pitchinginfoid/', Pitchinginfoid, name="Pitchinginfoid"),
    path('influencers/<str:cate>/', Influencers),
    path('influencers/', Influencers, name="filter"),
    path('contact/', Contactus),
    path('login/', Login, name='login'),
    path('Service/login/<str:infoname>/', Login,name='login1'),
    path('register/', Register, name='register'),
    path('privacy-policy/', Privacy_Policy),
    path('refund-policy/', Refund_Policy),
    path('reset/', Reset),
    path('terms-of-service/', Terms_Of_Service),
    path('whitepaper/', Whitepaper),
    path('blogs/', Blogs),
    path('Walletpurchase/',Walletpurchase,name="Walletpurchase"),
    path('career/', Career,name='Career'),
    path('Greeting-Payments/<str:username>/', Greeting_Payment),
    path('Event-Collaboration/<str:username>/', Influencer_Meet),
    path('casting-call/', Call_Casting),
    path('casting-call/<str:cate>/', Call_Casting),
    path('casting-call-details/<str:id>/', Call_Casting_Details),
    path('blogs/<str:cate>/', Blogscate),
    path('blog-details/<str:name>/', Blog_Deatils, name='Blog_Deatils'),
    path('likes/', likes, name="likes"),
    path('resetpassword/<str:uid>/<str:token>/', ResetPassword),
    path('affilate-marketing-for-brand/', Affilate_Marketing_Brands),
    path('affilate-marketing-for-influencer/', Affilate_Marketing_Influencer),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

    # For Creator
    path('Influencer-Dashboard/', Influencer_Dashboard),
    path('Photo-Gallery/', Photo_Gallery, name='upload'),
    path('Activity/', Activity),
    path('Bank-Details/', Bank_Details),
    path('Cancel-Orders/', Cancel_Orders),
    path('Completed-Orders/', Complete_Orders),
    path('Accepted-Orders/', Accepted_Orders),
    path('Earnings/', Earning),
    path('Orders/', Order1),
    path('Service-Plan/', Service_Plan),
    path('Settings/', Settings),
    path('Statement/', Statements),
    path('Referral/', Referrals),
    path('Login-Logs/', Login_Logs),
    path('Page-SEO-Setting/', SEO),
    path('Video-Gallery/', Video_Gallery),
    path('Overview/', Overview),
    path('deleteimage/<int:num>', deleteImage),
    path('deletesubslots/<int:num>', deleteSubslots),
    path('deletevideos/<int:num>/', deleteVideo),
    path('deletevideoslink/<int:num>/', deleteVideolink),
    path('deletecart/<int:cartid>/', deletemycart),
    path('deletewish/<int:wishid>/', deletewish),
    path('Blogs-Home/',Blogs_Home_Creator),
    path('Blogs-Home/<str:cate>/',Blogs_Home_Creator),
    path('BlogsPost/<str:name>/', Blogs_Post_Creator),
    path('Brand-Pitch/', Brandpitch),
    path('Pitchng-Report-list/', Pitching_List),
    path('Ordersdetails/', OrderDetails),
    path('Select-Account-Type/', Select_Account,name='Select_Account'),
    # path('Select_Account_for_whatsapp/<str:token>/',Select_Account_for_whatsapp,name='Select_Account_for_whatsapp'),
    path('add-webstories/', Add_webstories),

    # For Account
    path('Account-Dashboard/', Account_Dashboard),
    path('logout/', Logout),
    path('Clients-Refund-Payments/', Payment),
    path('Influencers-Payments/', Influencers_Payments),
    path('Total-Earnings/', Total_Earnings),
    path('Profile-Details/', Profile_Settings),
    path('Blog-Comments-Status/', Blog_Comments),
    path('InsertBlog/', Bloginsert),
    path('Create-Invoice/', Createinvoice),
    path('Invoice/<str:orderid>/', Invoice),
    path('fetchdetails/<int:order>/', fetchdetails),
    path('fetchtestimonails/<int:testimonailid>/', fetchtestimonails),
    path('fetchblogcomment/<int:commentid>/', fetchblogcomment),
    path('fetchblog1/<int:commentid>/', fetchblog1),
    path('fetchblogconnet/<int:commentid>/', fetchblogconnet),
    path('fetchinforeview/<int:reviewid>/', fetchinforeview),
    path('fetchcallcasting/<int:castingcallid>/', fetchcallcasting),
    path('BlogsHome/',Blogs_Home_Ac),
    path('Blog-Content/',Blogs_Content_Edit),
    path('Blog-Edit/',Blogs_Edit),
    path('BlogsHome/<str:cate>/',Blogs_Home_Ac),
    path('BlogsDetails/<str:name>/', Blogs_Post_Ac),
    path('addblogcontent/', Blog_Content),
    path('Cancel-orders/', Cancelorders),
    path('Complete-orders/', Completeorders),
    path('Total-orders/', Orders_Ac),
    path('Active-orders/', Activeorders),
    path('Mailviewinvoice/', Mailviewinvoice),
    path('Creatorslist/', Creators_List),
    path('Agencylist/', Agency_List),
    path('Clientslist/', Client_List),
    path('Creators-Overview/', Creators_over),
    path('Creators-Setting/', Creators_setting),
    path('Creators-Serviceplan/', Creators_serviceplan),
    path('Creators-Bankdetails/', Creators_bank),
    path('Creators-SEO-Setting/', Creators_seo),
    path('Client-Profile/', ClientsProfile),
    path('kycbrandprofile/',kycbrandprofile),
    path('set-margin/',Marginset),
    path('orders_details/', accountordersdet , name="orders_details"),
    path('payout-request/',payout_request),
    
    path('order-purchase-transaction/',orders_purchase_log),
    path('advertiser-transaction/',advertiser_txn),
    path('affiliate-transaction/',affiliate_txn),
    path('wallet-transaction/',wallet_txn),
    path('wallet-withdrawal-request/',wallet_withdrawal_req),
    path('Sendperdaytransactions/',DownloadPerDayTransactionLog),


    #kyc dashboard
    path('kyc-dashboard/', kycdashboard),
    path('pending-kyc-request/', Total_KYC_Request),
    
    path('brand-kyc-request/',Total_KYC_Request1),
    
    path('completed-kyc-request/', Completed_KYC),
    path('completed-brand-kyc/',Completed_KYC1),
    path('brands-lists/', Brands_Lists),
    path('creators-lists/', Creators_Lists),
    path('clients-lists/', Clients_Lists),
    path('profile-settings/', KYC_Profilesetting),
    path('blogshome/', Blogshome),
    path('blogdetails/<str:name>/', Blogsdetails),
    path('blogshome/<str:cate>/',Blogshome),
    path('platform-review/', Platform_Review),
    path('influencer-review/', Influencer_Review), 
    path('all-castingcall/', Allcastings),
    path('active-castingcall/', Activecastings),
    path('blogs-comments/', BlogCommments_Status),
    path('webstories-approval/', webstoriesapproval),
    path('bankdetails/', user_bankdetails),


    #for all invalid urls
    # For Client Dashboard
    path('User-Dashboard/', User_Dashboard),
    path('Completed-Project/', Completed_Project),
    path('Pending-Project/', Pending_Project),
    path('Cancel-Project/', Cancel_Project),
    path('Active-Project/', Active_Project),
    path('Activities/', Activities),
    path('Profile-Setting/', Setting),
    path('Orders-Detail/', OrdersDetails),
    path('Pitching-Details/',Pitching_Detail),
    path('landing/', homepage, name='landing'),
    path('create-checkout-session/', create_checkout_session, name='checkout'),
    path('success.html/', success, name='success'),
    path('payment-wallet-success/', success1, name='success1'),
    path('cancel.html/', cancel, name='cancel'),
    path('webhooks/stripe/', webhook, name="webhookstripe1"),
    path('webhooks/paypal/', webhookpaypal, name="webhookpaypal"),
    path('BlogHome/',Blogs_Home_User),
    path('BlogHome/<str:cate>/',Blogs_Home_User),
    path('BlogPost/<str:name>/', Blogs_Post_User),
    path('Orders-Invoice/', Orders_Invoice1),
    path('Client-Referral/', Client_Referral),
    path('My-Wishlist/', My_Wishlist),
    path('My-Cart/', MyCart),
    path('webstories/', Web_Story),
    path('webstories/<str:title>/',Web_Story_Details),

    # For agency dashboard
    path('testing/',testing),
    path('agency_dashboard/', agency_dashboard),
    path('completed_project/', completed_project),
    path('pending_project/', pending_project),
    path('cancel_project/', cancel_project),
    path('active_project/', active_project),
    path('insert_casting_call/', castingcall),
    path('total_casting_call/', totalcastingcall),
    path('profile_setting/', setting),
    path('orders_detail/', ordersdetail),
    path('casting_call_pitching_details/',view_casting_call_pitching ),
    path('pitching_details/',pitching_detail),
    path('bloghome/',blogs_home_user),
    path('bloghome/<str:cate>/',blogs_home_user),
    path('blogpost/<str:name>/', blogs_post_user),
    path('orders_invoice/', orders_invoice),
    path('agency_referral/', client_referral),
    path('my_wishlist/', my_wishlist),
    path('my_cart/', agencymycart),
    path('ajax/check_title/',check_title,),
    
    #check mailid ajax
    path('check_email/', check_email, name='check_email'),

    # path('paymentslip/', paymentslip ),
    # path('test/', test ),

    #####wallet#####
    path('wallet/', client_payout),
    path('user-wallet-info/', user_wallet),
# Completed

    # For RM Dashboard
    path('rm-dashboard/', RM_Dashboard),
    path('completed-orders/', RM_Completed_orders),
    path('active-orders/', RM_Active_orders),
    path('pending-orders/', RM_Pending_orders),
    path('cancelled-orders/', RM_Cancelled_orders),
    path('profile-setting/', RM_Profile_Setting),
    path('influencer-overview/', RM_Influencer_Overview),
    path('influencer-setting/', RM_Influencer_Setting),
    path('influencer-serviceplan/', RM_Influencer_Serviceplan),
    path('influencer-bankdetails/', RM_Influencer_Bank),
    path('influencer-seo-setting/', RM_Influencer_SEO),
    path('orders-details/', RM_Orders_Details),
    path('influencer-payment/', RM_Influencer_Payment),
    path('influencers-list/', RM_Influencers),
    path('clientslist/', RMClients),
    path('rm-approval/', RM_Approval),
    path('clientsprofile/', rmclient_profile),
    path('brandlist/', rmbrandlist),
    path('brandprofile/', rmbrandprofile),
    path('orderinvoice/', rmordersinvoice),
    path('withdrawal-request/', withdrawalrequest),
    path('get_story_by_id/', get_story_by_id, name='get_story_by_id'),
    path('users-wallet-info/', users_wallet_info),
    path('coupons/',Generatecoupon),
    path('check_coupon_term/', check_coupon_term, name='check_coupon_term'),
    path('notifyforprofileupdation/',notifyforprofileupdation),

    # For Manager Dashboard
    path('manager-dashboard/', Manager_Dashboard),
    path('activeorders/', ActiveOrders),
    path('pendingorders/', PendingOrders),
    path('cancelorders/', CancelOrders),
    path('completeorders/', CompleteOrders),
    path('totalearning/', TotalEarnings),
    path('rm-profile/', RM_ProfileDetails),
    
    path('manager-profile/', Manager_Profile),
    path('creatoroverview/', creatoroverview),
    path('creatorsetting/', creatorsetting),
    path('creatorserviceplan/', creatorserviceplan),
    path('creatorbank/', creatorbank),
    path('creatorseo/', creatorseo),
    path('ordersdetails/', ordersdetails),
    path('assignrmclient/', assignrmclient),
    path('assignrmbrand/', assignrmbrand),
    path('assignrm/', assignrm),
    path('clientprofile/',clientprofile),
    path('agencyprofile/',Agencyprofile),
    path('influencer-profile/', Influencers_ProfileDetails),
    path('client-profile/', Clients_ProfileDetails),
    path('brand-profile/', Brands_ProfileDetails),
    path('rm-review/',rmreview),
   
    # For RazorPay
    path('create_order/', create_order, name='payment'),

    # For paypal
    path('paypalipn/', include('paypal.standard.ipn.urls')),
    path('paypalbutton/', paypalbutton, name= 'paypalbutton'),
    path('paypal_reverse/', paypal_reverse, name = 'paypal_reverse'),
    path('paypal_cancel/', paypal_cancel, name = 'paypal_cancel'),

    # For Android Application
    # Get API's
    path('<str:var>/<int:loginid>', Index),
    path('<str:var>/influencer/<str:username>/<int:loginid>', Services1),
    path('<str:var>/blog', Blogs),
    path('<str:var>/privacy-policy', Privacy_Policy),
    path('<str:var>/Casting-Call/<str:cate>', Call_Casting),
    path('api/CastingCall', call_api),
    path('<str:var>/Casting-Call-Details/<int:id>', Call_Casting_Details),
    path('<str:var>/blogs/<str:cate>', Blogscate),
    path('<str:var>/refund-policy', Refund_Policy),
    path('<str:var>/terms-of-service', Terms_Of_Service),
    path('<str:var>/About', About),
    path('<str:var>/faq', Faq),


    # Post Api's
    path('api/register', Registerapi),
    path('api/login', Loginapi),
    path('api/bloglikes', blogslikes),
    path('api/influencers/<str:cate>/<int:loginid>', Influencersapi),
    path('api/Contactus', Contactusapi),


    # Get and Post API's
    path('<str:var>/blog-details/<str:name>', Blog_Deatils_api),
    path('ankit/', ankit),
    

#    path('chat/', include('chat.urls')),

    #advertiser
    path('advertiser-instruction/', advertiser_instruction),
    path('advertiser-offer/', advertiser_offer),
    path('advertiser-withdrawal-request/', advertiser_withdrawal_request),
    #rm
    path('rm-advertiser-approval/', rm_advertiser_approval),
    path('rm-affiliate-payout-request/', rm_affiliate_payout_request),
    path('rm-request-advertiser-payout/', platform_request_advertiser_payout),
    path('rm-request-advertiser-payout-history/', platform_request_advertiser_payout_history),
    #account
    path('account-affiliate-payout-request/', account_affiliate_payout_request),
    
    #manager
    path('manager-affiliate-payout-request/', manager_affiliate_payout_request),
    #manager_affiliate_payout_request
    #affiliate
    path('affiliate-offer/', affiliate_offer),
    path('affiliate-campaign/', affiliate_campaign),
    path('affiliate-lead/', affiliate_lead),
    path('affiliate-webhook/', affiliate_webhook),
    path('bankdetail/', affiliate_bankdetail),
    path('affiliate-payout/', affiliate_payout),
    
    #marketingapp
    path('marketing-dashboard/', marketing_dashboard),
    path('facebook-campaign/', facebook_campaign),
    path('instagram-campaign/', instagram_campaign),
    path('linkedin-campaign/',linkedin_campaign),
    path('tiktok-campaign/',tiktok_campaign),
    path('youtube-campaign/',youtube_campaign),
    path('twitter-campaign/',twitter_campaign),
    path('marketing-profile/', marketing_profile),
    
    
    #Super-Admin
    path('Admin-Dashboard/', Admin_Dashboard),
    path('Agencies-List/', Agencies),
    path('Account-User-List/', AccountUser),
    path('Brands-List/', Brands),
    path('Clients-List/', Clients),
    path('Creators-List/', Creators),
    path('RM-List/', RM_List),
    path('Managers-List/', Managers),
    path('Account-Info/', Account_Info),
    path('Welcome-Message/', Welcome_Message),
    path('Reset-Password-Message/', Reset_Password_Message),
    path('Orders-Confirmed-Message/', Orders_Confirmed_Message),
    path('Card-Declined-Message/', Card_Declined_Message),
    path('Promotions-Email1-Message/', Promotions_Email1),
    path('Promotions-Email2-Message/', Promotions_Email2),
    path('Promotions-Email3-Message/', Promotions_Email3),
    path('Blogs-Home/', Blogs_Home_Admin),
    path('Blogs-Home/<str:cate>/', Blogs_Home_Admin),
    path('Blogs-Post/<str:name>/', Blogs_Post_Admin),
    path('Data-Charts/', Data_Charts),
    path('Data-Tables/', Data_Tables),
    path('Data-Mixed/', Data_Mixed),
    path('Account-Overview/', Account_Overview),
    path('Account-Settings/',Account_Setting),
    path('Account-Security/',Account_Security),
    path('Account-Activity/',Account_Activity),
    path('Account-Billing/',Account_Billing),
    path('Account-Statement/',Account_Statement),
    path('Account-Referrals/',Account_Referrals),
    path('Account-Logs/',Account_Logs),
    path('Total-Orders/',Total_Orders),
    path('Complete-Orders/',Completed_Orders),
    path('Pending-Orders/',Pendings_Orders),
    path('Cancelled-Orders/',Cancelled_Orders),
    path('Ordersdetails/',Orders_Details),
    path('Account-User-Profile/',Account_User_Profile),
    path('Brand-Profile-Overview/',Brand_User_Overview),
    path('Brand-Profile-Setting/',Brand_Profile_Setting),
    path('Brand-Project/',Brand_Project),
    path('Brand-Campaigns/',Brand_Campaigns),
    path('Brand-Activity/',Brand_Activity),
    path('Brand-Billing/',Brand_Billing),
    path('Brand-Statement/',Brand_Statement),
    path('Brand-Security/',Brand_Security),
    path('Clients-Profile-Details/',Clients_Details),
    path('Clients-Total-Orders/',Clients_Total_Orders),
    path('Clients-Completed-Orders/',Clients_Completed_Orders),
    path('Clients-Pendings-Orders/',Clients_Pendings_Orders),
    path('Clients-Cancelled-Orders/',Clients_Cancelled_Orders),
    path('Private-Chats/',Private_Chats),
    path('Groups-Chats/',Groups_Chats),
    path('Role-Management/',Roles_List),
    path('View-Roles/',View_Roles),
    path('Agency-Profile-Overview/',Agency_Overview),
    path('Agency-Profile-Setting/',Agency_Setting),
    path('Agency-Security/',Agency_Security),
    path('Agency-Activity/',Agency_Activity),
    path('Agency-Billing/',Agency_Billing),
    path('Agency-Statement/',Agency_Statement),
    path('Agency-Project/',Agency_Project),
    path('Agency-Campaigns/',Agency_Campaigns),
    path('Calendar/',Calendar),
    path('RM_Overview/',RM_Overview),
    path('RM_Setting/',RM_Setting),
    path('RM_Security/',RM_Security),
    path('RM_Activity/',RM_Activity),
    path('Total-Brands-Under-RM/',RM_Brand),
    path('Total-Creators-Under-RM/',RM_Creators),
    path('Total-Clients-Under-RM/',RM_Clients),
    path('Total-Agencies-Under-RM/',RM_Clients),
    path('Manager-Overview/',Manager_Overview),
    path('Manager-Setting/',Manager_Setting),
    path('Manager-Security/',Manager_Security),
    path('Manager-Activity/',Manager_Activity),
    path('Total-Brands-Under-Manager/',Manager_Brand),
    path('Total-Creators-Under-Manager/',Manager_Creators),
    path('Total-Clients-Under-Manager/',Manager_Clients),
    path('Total-Agencies-Under-Manager/',Manager_Agencies),
    path('Total-RM-Under-Manager/',Manager_RM),
    path('Upload-Job-Requirements/',Upload_Requirments),
    path('deletejob/<int:jobid>/',deletejob),
    path('deleteblog/<int:blogid>/',deleteblog),
    path('deleteemployeereview/<int:rwid>/',deleteemprew),
    path('Interested-Candidates/',Interested_Candidates),
    path('Employee-Review/',Employee_Review),
    path('Upload-Blogs/',Upload_Blogs),
    path('Total-Blog-List/',Total_Blog_List),
    path('fetchblog/', fetchblog, name="fetchblog"),
    path('orderdet/', Orderdet, name="orderdet"),
    path('infoselectid/', infoselectid, name="infoselectid"),
    path('infoselectid2/', infoselectid2, name="infoselectid2"),
    path('accinfoselectid/', infoselectid1, name="accinfoselectid"),    
    
    path('kycapproved/', Kycapproved, name="kycapproved"),
    
    path('disablekyc/', Disablekyc, name="disablekyc"),
    
    path('roleapproved/', Roleapproved, name="roleapproved"),
    path('clientselectid/', Clientselectid, name="clientselectid"),
    path('clientselectid2/', Clientselectid2, name="clientselectid2"),
    path('bankselectid/', bankselectid, name="bankselectid"),
    path('bankdetselectid/',bankdetselectid,name="bankdetselectid"),
    path('accclientselectid/', Clientselectid1, name="accclientselectid"),
    path('agencyselectid/', Agencyselectid, name="agencyselectid"),
    path('agencyselectid1/', Agencyselectid1, name="agencyselectid1"),
    path('orderinv/', orderinv, name="orderinv"),
    path('delwish/', delwish, name="delwish"),
    path('delCart/', delCart, name="delCart"),
    path('Orderres/', orderres, name="orderres"),
    path('Clientdet/', Clientdet, name="Clientdet"),
    path('Seoid/', Seoid, name="Seoid"),
    path('Accountdet/', Accountdet, name="Accountdet"),
    path('RMdet/', Rmdet, name="RMdet"),
    path('Infodetails/', Infodetails, name="Infodetails"),
    path('Influencer-Seo-Settings/', SEO_Influencer),
    path('All-Page-SEO-Content/', All_Page_SEOContent),
    path('Pagewise-SEOContent/', PageWise_SEOContent),
    path('Change-SeoSetting/', Change_SEOSetting),
    path('User-Referral/', User_Referral),
    path('User-Referral-Count/', User_Referral_Count),
    #For Qr Code Generator
    path('home/', home1, name='home1'),
    path('generate_qr_code/<int:document_id>/', generate_qr_code, name='generate_qr_code'),
    path('validate_pdf_document/', validate_pdf_document, name='validate_pdf_document'),
    path('my_view/', my_view, name='my_view'),
    


    #agora_chat app urls
    path('Group-Chat/', login_user,),
    # path('agora/', TemplateView.as_view(template_name='login.html')),
    # path('join/<str:name>/<str:channel>', join, name='join_nd_show_feed'),
    path('add/', add_post, name='add_message'),
    path('single-chat-add/', single_chat_add_post, name='single_chat_add_message'),
    # path('channel/', create_Channel, name='create_channel'),
    path('deactivate/<str:name>/<str:channel>', deavtivate_channel, name='deactivate_channelinput'),
    # path('test/', TemplateView.as_view(template_name='group-chat.html')),
    path('Group-Chat/show_chat/<str:name>/<str:channel>', show_chat, name="show_chat"),
    path('chat-file-upload/', get_signed_url),
    path('get-file-download-url/<str:filename>/<str:foldername>', file_make_public),
    path('update-last-activity/',updateGetLastActivity),
    path('Group-Chat/get-contact-unreadmessage-groupchat/',sendunreadMessageCountGroupChat),
    ### single user chat between client and influencer
    path('client-influencer-start-chat/<str:influencer>/',create_Channel),
    path('client-influencer-chat/',influencerchat, name="client-influencer-temp-chat"),
    path('influencer-show_chat/<str:name>/<str:channel>',single_show_chat),
    ### single user chat between client and RM
    path('get-RM-chat/', show_RM_chat),
    path('client-chat/', rm_client_chat),
    path('client-chat/show-chat/<str:name>/<str:channel>', RM_single_show_chat),
    path('get-contact-unreadmessage-singlechat/',sendUnreadMessageCount),
    # getting unraed status for client and creater
    path('get-unread-status/',getunreadmessagecount),
    # get newly recived msg
    path('getorderchatnewmsg/', getorderchatnewmsg),
    path('getsinglechatnewmsg/', getsinglechatnewmsg),
    #webook 1
    path('webhook1/', Webhook1), 

    ## zoom meeting links
    path('oauth/login/', oauth_login, name='oauth_login'),
    path('oauth/callback/', oauth_callback, name='oauth_callback'),
    # path('get-code-using-refersh-token/<int:order_id>/', refresh_access_token,name="without-user-ineratcion"),
    path('schedule-meet/<int:order_id>/', schedule_zoom_meeting, name='schedule-meet'),
    path('get_recording_download_link/<int:meeting_id>/<str:order>/',get_recording_download_link),
    # # path('end_meeting/<int:meeting_id>/',end_meeting),

    # push notification urls
    path('get_token/', TemplateView.as_view(template_name='zabdra.html')),
    # path('send/', send_agency_email, name="send_notification"),
    path('firebase-messaging-sw.js', showFirebaseJS, name="show_firebase_js"),
    path('savebrowsertoken/<str:token>/', savebrowesrid),
    

    #INAPP notification urls
    #path('', first_view, name='first-view'),
    path('updatenotificationdata/', notificationstatus),
    # update notification read status
    path('updatenotificatoinreadstatus/',updatenotificatoinreadstatus),

    # For notification
    path('notification/', Notification),
    # path('updateallnotificatonread/', updateallnotificatonread),


    # send telegram notifications---
    path('send-telegram-notifications/',sendmessagetelegram),
    path('serve_image_from_static/',send_telegram_image),
    path('send-mail/',send_customer_email),
    # path('api/save_chat_id/', save_chat_id, name='save_chat_id'),

    # telegram webhook
    path('telegram/webhook/', telegram_webhook),

    #### whatsapp login videos
    path('Whatsapp_webhook/', Whatsapp_webhook, name='Whatsapp_webhook'),
    path('whatsapplogin/<str:token>/',whatsapplogin),
    path('generate_jwt/<str:link>/<int:mobile>/',hit_api),
    path('Loginappuser/<str:token>/',Loginappuser),
    
    # whtapp url shortner#####
    # path('<str:short_code>/', redirect_view, name='redirect_view'),
    
    # path('schedule_zoom/<str:order_id>', schedule_zoom_meeting)

    # send notification data in json form api
    path('sendnotiaboutvc/', Notificationapi),

###### prfile link
    path('get_influencer_profile_links/',get_influencer_profilelink),
    path('post_influencer_profiledata/',post_influencer_profiledata),

    ## send mail to account
    path('send_accounts_email/',send_accounts_email),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

