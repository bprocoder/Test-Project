from django.contrib import admin
from .models import *

# Register your models here.

class AllusersAdmin(admin.ModelAdmin):
    # Fields to search in the search bar
    search_fields = ['username', 'email', 'roles','id']

    # Filters to be added to the right side of the list view
    list_filter = ['roles', 'profilestatus','date_joined', 'last_activity']

    # Displayed columns in the list view
    list_display = ['id', 'username', 'email', 'roles', 'profilestatus', 'date_joined']


admin.site.register(Allusers, AllusersAdmin)




admin.site.register((Orderstatus,Eventtype,CastingCallSeoPage,Blogcontent,BlogsCate,CastingCallCategories,Wishlist, Shortdescription,Templates,AffiliateforinfluencerPage,AffiliateforbrandPage,AffiliateforinfluencerDetail,AffiliateforbrandDetail,PitchingCastingCall,LoginIP,CastingCallPage,EmployeeReview, Jobhiring,Careerpage,Callcastingquestions,Casting_Call,Servicetabtitle,Rmprofile,Rmsettings,Notifications,Ordercancelreasons,Managerssettings,ExchangeRates,BlogCategory,BlogComments,VideosLink,Services,Payments,Seo_Content,TermsofServiceDetail,Pages,RefundPolicyDetail,PrivacyPolicyDetail, Blog, PageBanner,DifferentCategory,Seo_Settings,PlatformDetails,Platforms,InfluencerSettings,Useraccounts,Orders,PricingPlans,UserDocuments,Aboutme,Rulesgig,Whychooseme,Images,Videos,Categories,Languages,ClientSettings,Permissions,Userpermissions,InfluencerProfile, AgencyProfile,ClientProfile,CompanyLogo,Testimonails,FooterDetail,Contact,AboutDetail,FaqDetail,Home_Page_Detail))
