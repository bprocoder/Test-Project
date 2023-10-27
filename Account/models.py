from django.db import models
from mainapp.models import *
# Create your models here.


class Stripepayments(models.Model):
    stripepaymentsid = models.AutoField(primary_key=True)
    id = models.TextField(blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    Seller_Message = models.TextField(blank=True, null=True)
    Created = models.TextField(blank=True, null=True)
    Amount = models.TextField(blank=True, null=True)
    Amount_Refunded = models.TextField(blank=True, null=True)
    Currency = models.TextField(blank=True, null=True)
    Converted_Amount = models.TextField(blank=True, null=True)
    Converted_Amount_Refunded = models.TextField(blank=True, null=True)
    Fee = models.TextField(blank=True, null=True)
    Tax = models.TextField(blank=True, null=True)
    Converted_Currency = models.TextField(blank=True, null=True)
    Mode = models.TextField(blank=True, null=True)
    Status = models.TextField(blank=True, null=True)
    Statement_Descriptor = models.TextField(blank=True, null=True)
    Captured = models.TextField(blank=True, null=True)
    Card_ID = models.TextField(blank=True, null=True)
    Card_Last4 = models.TextField(blank=True, null=True)
    Card_Brand = models.TextField(blank=True, null=True)
    Card_Funding = models.TextField(blank=True, null=True)
    Card_Exp_Month = models.TextField(blank=True, null=True)
    Card_Exp_Year = models.TextField(blank=True, null=True)
    Card_Name = models.TextField(blank=True, null=True)
    Card_Address_Country = models.TextField(blank=True, null=True)
    Card_Issue_Country = models.TextField(blank=True, null=True)
    Card_Fingerprint = models.TextField(blank=True, null=True)
    Card_CVC_Status = models.TextField(blank=True, null=True)
    Disputed_Amount = models.TextField(blank=True, null=True)
    Dispute_Status = models.TextField(blank=True, null=True)
    Dispute_Reason = models.TextField(blank=True, null=True)
    Dispute_Date = models.TextField(blank=True, null=True)
    Dispute_Evidence_Due = models.TextField(blank=True, null=True)
    Payment_Source_Type = models.TextField(blank=True, null=True)
    Is_Link = models.TextField(blank=True, null=True)
    Destination = models.TextField(blank=True, null=True)
    Transfer = models.TextField(blank=True, null=True)
    Transfer_Group = models.TextField(blank=True, null=True)
    PaymentIntent_ID = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.stripepaymentsid)
    
    
class Webhookfullresponse(models.Model):
    webhookfullresponseid = models.AutoField(primary_key=True)
    json_response = models.JSONField(null=True, blank=True)


    def __str__(self):
        return str(self.webhookfullresponseid)
    

class ClientPayout(models.Model):
    payoutid = models.AutoField(primary_key=True)
    
    clientid = models.OneToOneField(Allusers, models.DO_NOTHING,
                                 db_column='clientid', to_field='id')
    
    # influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
    #                                  db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    
    remaining_balance_bank = models.FloatField(blank=True, null=True)
    successful_withdrawal_bank = models.FloatField(blank=True, null=True)
    hold_bank = models.FloatField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)
    is_wallet_used_with_payment_gateway=models.BooleanField(default=False)
   

   
   
   
   

class ClientPayoutHistory(models.Model):
    payouthistoryid = models.AutoField(primary_key=True)
    
    creationdate = models.DateTimeField(auto_now=True)

    clientid = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='clientid', to_field='id')
    paymentid = models.ForeignKey(Payments, models.DO_NOTHING,
                                 db_column='paymentid', to_field='paymentsid',null=True,blank=True)
    wallet_transaction_amount=models.FloatField(default=0)
    requested_currency = models.TextField()
    remark = models.TextField(null=True,blank=True)
    
    
    isrefund_balance = models.BooleanField(default=False) #if true balance credited , if false wallet hold credited
    isrefund_hold = models.BooleanField(default=False) #if true balance credited , if false wallet hold credited
    
    
    
class ClientWithdrawalRequest(models.Model):
    withdrawalrequestid = models.AutoField(primary_key=True)
    
    creationdate = models.DateTimeField(auto_now=True)

    clientid = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='clientid', to_field='id')

    requested_currency = models.TextField()
    requested_method = models.TextField()
    requested_amount = models.FloatField()
    
    
    isrefund_balance = models.BooleanField(default=False) #if true balance credited , if false wallet hold credited
    isrefund_hold = models.BooleanField(default=False) #if true balance credited , if false wallet hold credited

    assigned_rm = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='assigned_rm', to_field='id', blank=True, null=True, related_name='withdrawalrequest_assigned_rm')
    rm_action = models.BooleanField(default=False)


    assigned_accountant = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='assigned_account', to_field='id', blank=True, null=True, related_name='withdrawalrequest_assigned_account')
    accountant_action = models.BooleanField(default=False)
    transaction_amount = models.FloatField(default=0)
    transaction_screenshot = models.ImageField(
        upload_to='transactionscreenshots/',blank=True, null=True)