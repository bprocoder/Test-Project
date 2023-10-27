from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AdvertiserOffer)
admin.site.register(AdvertiserWithdrawalRequest)
admin.site.register(AdvertiserOverview)
admin.site.register(RmAdvertiserOffer)

admin.site.register(RmAffiliateBankDetail)
admin.site.register(RmAffiliatePendingPayout)
# admin.site.register(Affiliatecampaingn)
# admin.site.register(Affiliatelead)
admin.site.register(AffiliateBankDetail)
admin.site.register(AffiliatePayout)
admin.site.register(PostbackWebhook)