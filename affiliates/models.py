from django.db import models
from mainapp.models import *
# Create your models here.

##############################################################
class AdvertiserOffer(models.Model): #offer goes to rm for approvasl then shows in affiliate offer
    #same as Affiliatesoffers but with server ip
    offerid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(
        AgencySettings, models.DO_NOTHING, db_column='userid',  to_field='asettingsuserid',blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    server_ip = models.TextField(blank=True, null=True) #Whitelist IPs of advertiser servers to reduce fraudulent postback hits.
    location = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    productlink = models.TextField(blank=True, null=True)
    # currency = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    approvedrate = models.FloatField(blank=True, null=True)
    payout = models.FloatField(blank=True, null=True)
    platform_margin = models.FloatField(default=10)
    affiliate_payout = models.FloatField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    
    creationdate = models.DateTimeField(auto_now=True)
    isapproved=models.BooleanField(default=False)
    rmid = models.ForeignKey(Rmsettings, models.DO_NOTHING, db_column='rmid', to_field='rmid',default=103856) #this offer is assigned to this rm for approval
    image = models.ImageField(
        upload_to='affiliatemedia/', blank=True, null=True)
    isremoved = models.BooleanField(default=False)

class AdvertiserWithdrawalRequest(models.Model):# request by Rm shows here
    request_from_rm =  models.ForeignKey(
        Rmsettings, models.DO_NOTHING, db_column='request_from_rm',  to_field='rmid',blank=True, null=True)
    for_offersids = models.ForeignKey(AdvertiserOffer,models.DO_NOTHING)
    transaction_id = models.TextField(blank=True, null=True)
    payment_method = models.TextField(blank=True, null=True)
    amount = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
class AdvertiserOverview(models.Model):
    pass 

#########################################################################

class RmAdvertiserOffer(models.Model):
    pass #show content of AdvertisersOffer
class RmAffiliateBankDetail(models.Model):
    pass #show data from AffiliateBankDetails and give access to change isverified
class RmAffiliatePendingPayout(models.Model):
    pass # show filtered data by status(payout request)=requested from Affiliatesleads and give access to change its value from rquested to paid

class RmAffiliateOfferApplication(models.Model): #caution! here, for affiliateid user can be both client and influencer so implement same in foreign key(currently only client)
    # affiliateid = models.ForeignKey(ClientSettings, models.DO_NOTHING,
    #                                 db_column='affiliateid', to_field='csettingsuserid', blank=True, null=True)
    affiliateid = models.ForeignKey(Allusers, models.DO_NOTHING,
                                    db_column='affiliateid', to_field='id', blank=True, null=True)
    
    offerid = models.ForeignKey(AdvertiserOffer, models.SET_NULL,
                                    db_column='offerid', to_field='offerid', blank=True, null=True)
    
    productlink_updatedutm = models.TextField(blank=True, null=True)
    productlink_updatedutm_newdomain = models.TextField(blank=True, null=True)
    click_count = models.IntegerField(blank=True, null=True)
    traffic_source = models.TextField(blank=True, null=True)
    expected_volume_of_leads = models.IntegerField(blank=True, null=True)
    optional_message = models.TextField(blank=True, null=True)
    rmid = models.ForeignKey(
        Rmsettings, models.DO_NOTHING, db_column='rmid', blank=True, null=True) #this offer is assigned to this rm for approval
    
    isapproved = models.BooleanField(default=False)
    
class AffiliateWebhook(models.Model):
    creationdate = models.DateTimeField(auto_now=True)
    uuid = models.TextField(blank=True, null=True)
    # affiliateid = models.OneToOneField(RmAffiliateOfferApplication, models.DO_NOTHING,
    #                                 db_column='affiliateid', to_field='affiliateid', blank=True, null=True)
    
    # offerid = models.ForeignKey(RmAffiliateOfferApplication, models.SET_NULL,
    #                                 db_column='offerid', to_field='offerid', blank=True, null=True)
    
    utm_source = models.TextField(blank=True, null=True)
    utm_affiliate_id = models.TextField(blank=True, null=True)
    utm_offerid = models.TextField(blank=True, null=True)
    utm_productname = models.TextField(blank=True, null=True)
    campaingname = models.TextField(blank=True, null=True)
    payout = models.FloatField(blank=True, null=True)
    affiliate_payout = models.FloatField(blank=True, null=True)
    server_ip = models.TextField(blank=True, null=True)
    status=models.BooleanField(default=False)#IS LEAD VALID(ip whitelisted)
    
class PlatformPayout(models.Model):
    # offerid = models.ForeignKey(
    #     AdvertiserOffer,models.SET_NULL, db_column='offerid',  to_field='offerid',blank=True, null=True) 
    offerid = models.TextField(blank=True, null=True)
    userid = models.ForeignKey(
        AgencySettings, models.DO_NOTHING, db_column='userid',  to_field='asettingsuserid',blank=True, null=True)
    
    successful_withdrawal_bank = models.FloatField(default=0)
    hold_bank = models.FloatField(default=0)
    
    successful_withdrawal_usdt = models.FloatField(default=0)
    hold_usdt = models.FloatField(default=0)

    successful_withdrawal_btc = models.FloatField(default=0)
    hold_btc = models.FloatField(default=0)

class PlatformPayoutRequest(models.Model):
    
    creationdate = models.DateTimeField(auto_now=True)
###########################################################################################
    #request from:
    assigned_rm = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='assigned_rm', to_field='id', blank=True, null=True, related_name='PlatformPayoutRequest_assigned_rm')
    rm_action = models.BooleanField(default=False)
    
    assigned_account = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='assigned_account', to_field='id', blank=True, null=True, related_name='PlatformPayoutRequest_assigned_account')
    account_action = models.BooleanField(default=False)
    
    for_offer_id = models.TextField(blank=True, null=True)
    productname = models.TextField(blank=True, null=True)
    requested_method = models.TextField(blank=True, null=True)
    requested_amount = models.FloatField(blank=True, null=True)
    remaining_balance_on_dateofrequest = models.FloatField(blank=True, null=True)
###########################################################################################
    #request to:
    advertiserid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='advertiserid',  to_field='id',blank=True, null=True, related_name='PlatformPayoutRequest_advertiserid')
    
    transaction_amount = models.FloatField(default=0)
    transaction_screenshot = models.ImageField(
        upload_to='affiliatemedia/', blank=True, null=True)
        
    advertiser_action = models.BooleanField(default=False)
    isremoved = models.BooleanField(default=False)
###########################################################################################


class AffiliateBankDetail(models.Model):
    clientid = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='clientid', to_field='id', blank=True, null=True)
    
    payment_method = models.TextField(blank=True, null=True)
    
    upi_address = models.TextField(blank=True, null=True)
    upi_address_isverified = models.BooleanField(default=False)
    
    usdt_address = models.TextField(blank=True, null=True)
    btc_address = models.TextField(blank=True, null=True)
    # bank_details
    account_holder_name = models.TextField(blank=True, null=True)
    account_no = models.TextField(blank=True, null=True)
    bank_name = models.TextField(blank=True, null=True)
    branch_ifsc_code = models.TextField(blank=True, null=True)
    
    pancard_taxid = models.ImageField()
    pancard_taxid_isverified = models.BooleanField(default=False)
    
    adhaarcard_drivinglicence = models.ImageField()
    adhaarcard_drivinglicence_isverified = models.BooleanField(default=False)
    
    cancelled_cheque = models.ImageField()
    cancelled_cheque_isverified = models.BooleanField(default=False)
    
    passport_copy = models.ImageField()
    passport_copy_isverified = models.BooleanField(default=False)
    
class AffiliatePayout(models.Model):
    affiliateid = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='affiliateid', to_field='id', blank=True, null=True)
    
    # influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
    #                                  db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    
    remaining_balance_bank = models.FloatField(blank=True, null=True)
    successful_withdrawal_bank = models.FloatField(blank=True, null=True)
    hold_bank = models.FloatField(blank=True, null=True)
    #total_bank
    
    remaining_balance_usdt = models.FloatField(blank=True, null=True)
    successful_withdrawal_usdt = models.FloatField(blank=True, null=True)
    hold_usdt = models.FloatField(blank=True, null=True)
    # total_usdt
    
    remaining_balance_btc = models.FloatField(blank=True, null=True)
    successful_withdrawal_btc = models.FloatField(blank=True, null=True)
    hold_btc = models.FloatField(blank=True, null=True)
    # total_btc

class AffiliatePayoutRequest(models.Model):
    creationdate = models.DateTimeField(auto_now=True)

    affiliateid = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='affiliateid', to_field='id', blank=True, null=True, related_name='AffiliatePayoutRequest_affiliateid')
    requested_currency = models.TextField()
    requested_method = models.TextField(blank=True, null=True)
    requested_amount = models.FloatField(blank=True, null=True)

    assigned_rm = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='assigned_rm', to_field='id', blank=True, null=True, related_name='AffiliatePayoutRequest_assigned_rm')
    rm_action = models.BooleanField(default=False)


    assigned_account = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='assigned_account', to_field='id', blank=True, null=True, related_name='AffiliatePayoutRequest_assigned_account')
    transaction_amount = models.FloatField(default=0)
    transaction_screenshot = models.ImageField(
        upload_to='affiliatemedia/', blank=True, null=True)
    
    account_action = models.BooleanField(default=False)
    
    status = models.BooleanField(default=False) #hold, successful withdrawal, 


# class PlatformPayoutHistory(models.Model):
#     pass

############################################################################
class PostbackWebhook(models.Model):#check if requestfor post back is coming from whitelist ip
    pass

'''
class Advertisersoffer(models.Model):
    offersid = models.AutoField(primary_key=True)
    usersid = models.ForeignKey(
        AgencySettings, models.DO_NOTHING, db_column='usersid',  to_field='asettingsuserid',blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    server_ip = models.TextField(blank=True, null=True) #Whitelist IPs of advertiser servers to reduce fraudulent postback hits.
    location = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    approvedrate = models.FloatField(blank=True, null=True)
    payout = models.FloatField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    offerlink = models.TextField(blank=True, null=True)
    
    creationdate = models.DateTimeField(auto_now=True)
    isapproved=models.BooleanField(default=False)
    rmid = models.ForeignKey(
        Rmsettings, models.DO_NOTHING, db_column='rmid', blank=True,  to_field='rmid', null=True)
    image = models.ImageField(upload_to='',)

    def __str__(self):
        return str(self.usersid)


class Affiliatescampaingns(models.Model):
    affiliatesid = models.AutoField(primary_key=True)
    clientid = models.ForeignKey(ClientSettings, models.DO_NOTHING,
                                 db_column='clientid', to_field='csettingsuserid', blank=True, null=True)
    influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    productname = models.TextField(blank=True, null=True)
    campaingname = models.TextField(blank=True, null=True)
    links = models.TextField(blank=True, null=True)
    creationdate = models.DateTimeField(auto_now=True)



class Affiliatesleads(models.Model):
    affiliatesleadsid = models.AutoField(primary_key=True)
    affiliatesid = models.ForeignKey(Affiliatescampaingns, models.DO_NOTHING,
                                 db_column='affiliatesid', to_field='affiliatesid', blank=True, null=True)
    
    
    offername = models.TextField(blank=True, null=True)
    campaingname = models.TextField(blank=True, null=True)
    payout = models.FloatField(blank=True, null=True)
    status=models.BooleanField(default=False)
    creationdate = models.DateTimeField(auto_now=True)



'''