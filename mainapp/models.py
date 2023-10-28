from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from datetime import timedelta
from datetime import datetime
from django.utils import timezone
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.utils.timezone import make_aware

# Create your models here.


class Allusers(AbstractUser):
    id = models.AutoField(primary_key=True)
    roles = models.TextField(blank=True, null=True, default='client')
    mobileapptoken = models.TextField(blank=True, null=True)
    profilestatus = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


# class IPV4(models.Model):
#     ip_address = models.CharField(
#         max_length=20, blank=True, null=True, db_index=True)
#     country = models.TextField(blank=True, null=True)
#     countrycode = models.CharField(
#         max_length=5, blank=True, null=True, db_index=True)


# class IPV6(models.Model):
#     ip_address = models.CharField(
#         max_length=20, blank=True, null=True, db_index=True)
#     country = models.TextField(blank=True, null=True)
#     countrycode = models.CharField(
#         max_length=5, blank=True, null=True, db_index=True)


class Pages(models.Model):
    pageid = models.AutoField(primary_key=True)
    pagename = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.pagename)


class Seo_Content(models.Model):
    seocontentid = models.AutoField(primary_key=True)
    robot = models.TextField(blank=True, null=True)
    google_site_verification = models.TextField(blank=True, null=True)
    twitter_card = models.TextField(blank=True, null=True)
    twitter_site = models.TextField(blank=True, null=True)
    twitter_creator = models.TextField(blank=True, null=True)
    twitter_title = models.TextField(blank=True, null=True)
    twitter_image_url = models.TextField(blank=True, null=True)
    twitter_image_alt = models.TextField(blank=True, null=True)
    twitter_player = models.TextField(blank=True, null=True)
    twitter_player_width = models.TextField(blank=True, null=True)
    twitter_player_height = models.TextField(blank=True, null=True)
    fb_app_id = models.TextField(blank=True, null=True)
    og_title = models.TextField(blank=True, null=True)
    og_url = models.TextField(blank=True, null=True)
    og_img_url = models.TextField(blank=True, null=True)
    og_img_type = models.TextField(blank=True, null=True)
    og_img_width = models.TextField(blank=True, null=True)
    og_img_height = models.TextField(blank=True, null=True)
    og_type = models.TextField(blank=True, null=True)
    og_locale = models.TextField(blank=True, null=True)
    og_image_url = models.TextField(blank=True, null=True)
    og_img_secure_url = models.TextField(blank=True, null=True)
    og_site_name = models.TextField(blank=True, null=True)
    og_see_also = models.TextField(blank=True, null=True)
    aticle_author = models.TextField(blank=True, null=True)
    format_detecation = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.seocontentid)


# class Log_File(models.Model):
#     logfileid = models.AutoField(primary_key=True)
#     mainapplogfile = models.FileField(upload_to='')

#     def __str__(self):
#         return str(self.logfileid)


class Blog(models.Model):
    blogid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    title_tegs = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    url_structure = models.CharField(
        max_length=500, unique=True, blank=True, null=True)
    title = models.CharField(
        max_length=500, unique=True, blank=True, null=True)
    blog_categories = models.CharField(max_length=100, blank=True, null=True)
    short_discription = models.CharField(max_length=300, blank=True, null=True)
    discription = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='', blank=True, null=True)
    alttext = models.CharField(max_length=100, blank=True, null=True)
    keyword = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Blogcontent(models.Model):
    blogcontentid = models.AutoField(primary_key=True)
    blog = models.ForeignKey(Blog, models.DO_NOTHING)
    title = models.CharField(
        max_length=500, unique=True, blank=True, null=True)
    discription = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='', blank=True, null=True)
    alttext = models.CharField(max_length=100, blank=True, null=True)


class Categories(models.Model):
    categorieid = models.AutoField(primary_key=True)
    categoryname = models.TextField()
    subcategory = models.TextField(blank=True, null=True)
    usersid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='usersid', blank=True, null=True)
    creationdate = models.DateTimeField(blank=True, null=True)
    # Field name made lowercase.
    isapproved = models.BooleanField(default=False, blank=True, null=True)
    approvedby = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='',)
    approvaldate = models.DateTimeField(blank=True, null=True)
    page_title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.categoryname)


class BlogsCate(models.Model):
    blogscateid = models.AutoField(primary_key=True)
    blogscategory = models.TextField()
    page_title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.blogscategory)


class CastingCallCategories(models.Model):
    castingcallcategorieid = models.AutoField(primary_key=True)
    categoryname = models.TextField(blank=True, null=True)
    creationdate = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='',)
    page_title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.categoryname)


class CastingCallSeoPage(models.Model):
    castingcallseopageid = models.AutoField(primary_key=True)
    h1title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    castingcallcategorieid = models.ForeignKey(
        CastingCallCategories, models.DO_NOTHING)

    def __str__(self):
        return str(self.castingcallcategorieid.categoryname)


class BlogCategory(models.Model):
    blogcategoryid = models.AutoField(primary_key=True)
    blogcategory = models.TextField()
    blogcategory_count = models.TextField()

    def __str__(self):
        return str(self.blogcategoryid)


class BlogComments(models.Model):
    commentid = models.AutoField(primary_key=True)
    blog = models.ForeignKey(Blog, models.DO_NOTHING)
    Commenttext = models.TextField()
    name = models.CharField(max_length=20)
    totallikes = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    isapproved = models.BooleanField(default=False, blank=True, null=True)
    approveuserid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='approveuserid', to_field='id', blank=True, null=True)

    def __str__(self):
        return str(self.commentid)


class LoginIP(models.Model):
    LoginIPid = models.AutoField(primary_key=True)
    userid = models.IntegerField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    IP_Address = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    device = models.TextField(blank=True, null=True)
    sessionkey = models.TextField(blank=True, null=True)
    # sessionstatus = models.TextField(blank=True, null=True)
    time = models.TimeField(auto_now=True)
    date = models.DateTimeField(auto_now=True)

    def time_difference(self):
        now = datetime.now().time()
        start_time = datetime.combine(datetime.today(), self.time)
        end_time = datetime.combine(datetime.today(), now)
        diff = end_time - start_time

        years, remainder = divmod(diff.days, 365)
        weeks, days = divmod(remainder, 7)
        minutes, seconds = divmod(diff.seconds, 60)

        time_parts = []
        if years > 0:
            time_parts.append(f"{years} year{'s' if years > 1 else ''}")
        if weeks > 0:
            time_parts.append(f"{weeks} week{'s' if weeks > 1 else ''}")
        if days > 0:
            time_parts.append(f"{days} day{'s' if days > 1 else ''}")
        if minutes > 0:
            time_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
        if seconds > 0:
            time_parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")

        return ', '.join(time_parts) + ' ago'


class PageBanner(models.Model):
    PageBannerid = models.AutoField(primary_key=True)
    Loginimage = models.ImageField(upload_to='', blank=True, null=True)
    signupimage = models.ImageField(upload_to='', blank=True, null=True)
    Contactimage = models.ImageField(upload_to='', blank=True, null=True)
    Refundimage = models.ImageField(upload_to='', blank=True, null=True)
    aboutimage = models.ImageField(upload_to='', blank=True, null=True)
    faqimage = models.ImageField(upload_to='', blank=True, null=True)


class DifferentCategory(models.Model):
    differentcategoryid = models.AutoField(primary_key=True)
    categorylogo = models.ImageField(upload_to='',)
    categorytitle = models.TextField(blank=True, null=True)
    # categorylink = models.TextField(blank=True, null=True)
    logoalttext = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.categorytitle)


class UnverifedAgencyDetails(models.Model):
    unverifedagencydetailsid = models.AutoField(primary_key=True)
    clientid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='agency_userid', blank=True, null=True)
    comapanyname = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    itrcertficate = models.FileField(
        upload_to='agencydocs/',  blank=True, null=True)
    gstcertificate = models.FileField(
        upload_to='agencydocs/',  blank=True, null=True)
    verified = models.BooleanField(default=False)
    applied = models.BooleanField(default=False)


class AgencySettings(models.Model):
    agencysettingsid = models.AutoField(primary_key=True)
    asettingsuserid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='asettingsuserid', to_field='id', blank=True, null=True)
    email_verified = models.BooleanField(blank=True, null=True)
    mobile_verified = models.BooleanField(blank=True, null=True)
    twofa_verified = models.BooleanField(blank=True, null=True)
    kyc = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.asettingsuserid.username)


class Managerssettings(models.Model):
    msettingsid = models.AutoField(primary_key=True)
    managerid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='managerid')
    name = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    number = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='',)
    # This field type is a guess.
    languagesknown = models.TextField(blank=True, null=True)


class Rmsettings(models.Model):
    rmsettingsid = models.AutoField(primary_key=True)
    rmid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='rmid', blank=True, null=True)
    addressverified = models.BooleanField(blank=True, null=True)
    nameverified = models.BooleanField(blank=True, null=True)
    numberverified = models.BooleanField(blank=True, null=True)
    emailverified = models.BooleanField(blank=True, null=True)
    totalorderscompleted = models.IntegerField(blank=True, null=True)
    totalorderspending = models.IntegerField(blank=True, null=True)
    totalorderscancelled = models.IntegerField(blank=True, null=True)
    # This field type is a guess.
    totalrevenue = models.TextField(blank=True, null=True)
    # This field type is a guess.
    refundedrevenue = models.TextField(blank=True, null=True)
    managerid = models.ForeignKey(Managerssettings, models.DO_NOTHING,
                                  db_column='managerid', to_field='managerid', blank=True, null=True)

    def __str__(self):
        return str(self.rmid.username)


class AgencyProfile(models.Model):
    agency_profile_id = models.AutoField(primary_key=True)
    agency_userid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='agency_userid', blank=True, null=True)
    country = models.TextField(default='India', blank=True, null=True)
    profileimage = models.FileField(
        upload_to='Profileimages/', default='default_avtar.webp', blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)
    timezone = models.TextField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True, default='INR')
    mobile = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    fullname = models.CharField(max_length=50, blank=True, null=True)
    postalcode = models.CharField(max_length=15, blank=True, null=True)
    rmid = models.ForeignKey(Rmsettings, models.DO_NOTHING,
                             db_column='rmid', to_field='rmid', default=103856)
    date = models.DateTimeField(auto_created=True)


class ClientProfile(models.Model):
    client_profile_id = models.AutoField(primary_key=True)
    client_userid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='client_userid',  to_field='id', blank=True, null=True)
    country = models.TextField(default='India', blank=True, null=True)
    profileimage = models.FileField(
        upload_to='Profileimages/', default='default_avtar.webp', blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)
    timezone = models.TextField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True, default='INR')
    mobile = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    fullname = models.CharField(max_length=50, blank=True, null=True)
    postalcode = models.CharField(max_length=15, blank=True, null=True)
    rmid = models.ForeignKey(
        Rmsettings, models.DO_NOTHING, db_column='rmid', to_field='rmid', default=103856)
    date = models.DateTimeField(auto_created=True)


class ClientSettings(models.Model):
    clientsettingsid = models.AutoField(primary_key=True)
    csettingsuserid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='csettingsuserid', to_field='id', blank=True, null=True)
    email_verified = models.BooleanField(blank=True, null=True)
    mobile_verified = models.BooleanField(blank=True, null=True)
    twofa_verified = models.BooleanField(blank=True, null=True)
    kyc = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.csettingsuserid)


class InfluencerSettings(models.Model):
    influencer_settingsid = models.AutoField(primary_key=True)
    influencer_userid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='influencer_userid', blank=True, null=True)
    rm_userid = models.IntegerField(
        db_column='rm_userid', default=None, blank=True, null=True)
    email_verified = models.BooleanField(default=False, blank=True, null=True)
    mobile_verified = models.BooleanField(default=False, blank=True, null=True)
    address_verified = models.BooleanField(
        default=False, blank=True, null=True)
    twofa_verified = models.BooleanField(blank=True, null=True)
    kyc = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.influencer_userid)

    def first_planprice(self):
        pricing_plan = self.influencer_userid.plan_margin.first()
        return pricing_plan.marginpercentage if pricing_plan else None


class InfluencerAnalytics(models.Model):
    analyticsid = models.AutoField(primary_key=True)
    totalorders = models.IntegerField(blank=True, null=True)
    totalrevenues = models.IntegerField(blank=True, null=True)
    monthlyorders = models.IntegerField(blank=True, null=True)
    monthlyrevenues = models.IntegerField(blank=True, null=True)
    quaterlyorders = models.IntegerField(blank=True, null=True)
    quaterlyrevenues = models.IntegerField(blank=True, null=True)
    influencerid = models.ForeignKey(
        InfluencerSettings, models.DO_NOTHING, db_column='influencerid', blank=True, null=True)
    lastupdated = models.DateTimeField(blank=True, null=True)


class InfluencerProfile(models.Model):
    influencer_profile_id = models.AutoField(primary_key=True)
    influencer_userid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='influencer_userid', blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    fullname = models.CharField(max_length=1000, blank=True, null=True)
    desc_title = models.CharField(max_length=500, blank=True, null=True)
    short_description = models.IntegerField(default=1)
    # Field name made lowercase. This field type is a guess.
    language = ArrayField(models.IntegerField(
        blank=True, null=True), default=list, blank=True, null=True)
    # Field name made lowercase. This field type is a guess.
    categories = ArrayField(models.IntegerField(
        blank=True, null=True), default=list, blank=True, null=True)
    currency = models.TextField(blank=True, null=True, default='inr')
    # This field type is a guess.
    chooseme = models.IntegerField(default=1)
    rulesforgig = models.IntegerField(default=1)
    aboutme = models.IntegerField(default=1)
    # rulesforgig = ArrayField(models.IntegerField(
    #     blank=True, null=True), default=list, blank=True, null=True)
    gender = models.TextField(null=True)
    profileimage = models.ImageField(
        upload_to='Profileimages/', blank=True, null=True, default='default_avtar.webp')

    profileimage1 = models.ImageField(
        upload_to='Profileimages/', blank=True, null=True, default='default_avtar.webp')

    imagegallery = ArrayField(models.IntegerField(
        blank=True, null=True), default=list, blank=True, null=True)
    videogallery = ArrayField(models.IntegerField(
        blank=True, null=True), default=list, blank=True, null=True)
    videolink = ArrayField(models.IntegerField(
        blank=True, null=True), default=list, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    platformdetails = ArrayField(models.IntegerField(
        blank=True, null=True), default=list, blank=True, null=True)
    rating = models.IntegerField(default=5, blank=True, null=True)
    services = ArrayField(models.IntegerField(
        blank=True, null=True), default=list, blank=True, null=True)

    events = ArrayField(models.IntegerField(
        blank=True, null=True), default=list, blank=True, null=True)

    send = models.BooleanField(default=False)
    analyticsid = models.ForeignKey(
        InfluencerAnalytics, models.DO_NOTHING, db_column='analyticsid', blank=True, null=True)

    def __str__(self):
        return str(self.influencer_userid)

    def filled_fields_data(self):
        filled_count = 0
        total_fields = len(self._meta.fields)

        for field in self._meta.fields:
            value = getattr(self, field.name)

            # Special handling for certain field types
            if isinstance(field, (ForeignKey, OneToOneField)) and value is None:
                continue

            if isinstance(field, ImageField) and not value:
                continue  # since you're providing a default value for ImageFields

            # adjust the condition based on what you consider "filled"
            if value not in [None, "", []]:
                filled_count += 1

        return filled_count, total_fields

    def filled_percentage(self):
        filled, total = self.filled_fields_data()
        return (filled / total) * 100


class Seo_Settings(models.Model):
    seoid = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    influencerid = models.OneToOneField(InfluencerSettings, models.DO_NOTHING,
                                        db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    keyword = models.TextField(blank=True, null=True)

    page = models.ForeignKey(
        Pages, models.DO_NOTHING, related_name='page')

    def __str__(self):
        return str(self.seoid)+'||'+str(self.page.pagename)


class ExchangeRates(models.Model):
    ratesid = models.AutoField(primary_key=True)
    countery_abbrevation = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)
    rates = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.countery_abbrevation


class Platforms(models.Model):
    platformid = models.AutoField(primary_key=True)
    platform_name = models.TextField(blank=True, null=True)
    imagepath = models.ImageField(upload_to='',)

    def __str__(self):
        return self.platform_name+"|"+str(self.platformid)


class PlatformDetails(models.Model):
    platformdetailid = models.AutoField(primary_key=True)
    platformtype = models.TextField(blank=True, null=True)
    usersid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='usersid', blank=True, null=True)
    additiontime = models.DateTimeField(blank=True, null=True)
    platformcredential = models.TextField(blank=True, null=True)
    isapproved = models.BooleanField(default=False, blank=True, null=True)
    approvedby = models.IntegerField(blank=True, null=True)
    approvaldate = models.DateTimeField(blank=True, null=True)
    subscribers_followers = models.BigIntegerField(blank=True, null=True)
    allviews = models.BigIntegerField(blank=True, null=True)


class PlatformProfileLink(models.Model):
    platformprofilelinkid = models.AutoField(primary_key=True)
    platformtype = models.TextField(blank=True, null=True)
    usersid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='usersid', blank=True, null=True)
    additiontime = models.DateTimeField(auto_now=True)
    profilelink = models.TextField(blank=True, null=True)


class Wishlist(models.Model):
    wishlistid = models.AutoField(primary_key=True)
    clientid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='clientid', to_field='id', blank=True, null=True)
    influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    addtime = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    Cartid = models.AutoField(primary_key=True)
    clientid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='clientid', to_field='id', blank=True, null=True)
    influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    addtime = models.DateTimeField(auto_now=True)


class Servicetabtitle(models.Model):
    Servicetabtitleid = models.AutoField(primary_key=True)
    influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    brandtag = models.TextField(blank=True, null=True)
    shouttag = models.TextField(blank=True, null=True)
    greetingtag = models.TextField(blank=True, null=True)
    videochattag = models.TextField(blank=True, null=True)
    influenceracquasitiontag = models.TextField(blank=True, null=True)
    addtime = models.DateTimeField(auto_now=True)


class Whychooseme(models.Model):
    whychoosemeid = models.AutoField(primary_key=True)
    question = models.TextField()
    Whychoosetext = models.TextField()
    Whychoosetext1 = models.TextField()
    Whychoosetext2 = models.TextField()
    categoryid = models.ForeignKey(
        Categories, models.DO_NOTHING, db_column='categoryid', blank=True, null=True)
    Whychoosetext3 = models.TextField()
    Whychoosetext4 = models.TextField()

    def __str__(self):
        return self.categoryid.categoryname


class Aboutme(models.Model):
    aboutmeid = models.AutoField(primary_key=True)
    categoryid = models.ForeignKey(
        Categories, models.DO_NOTHING, db_column='categoryid', blank=True, null=True)
    abouttext = models.TextField()

    def __str__(self):
        return str(self.aboutmeid)+'|'+self.categoryid.categoryname


class Shortdescription(models.Model):
    shortdescriptionid = models.AutoField(primary_key=True)
    categoryid = models.ForeignKey(
        Categories, models.DO_NOTHING, db_column='categoryid')
    shortdestext = models.TextField()

    def __str__(self):
        return self.categoryid.categoryname


class Rulesgig(models.Model):
    rulesid = models.AutoField(primary_key=True)
    question = models.TextField()
    heading = models.TextField(blank=True, null=True)
    subheading = models.TextField(blank=True, null=True)
    subheading1 = models.TextField(blank=True, null=True)
    rulesforgig = models.TextField()
    rulesforgig1 = models.TextField()
    rulesforgig2 = models.TextField()
    rulesforgig3 = models.TextField()
    rulesforgig4 = models.TextField()
    rulesforgig5 = models.TextField(blank=True, null=True)
    rulesforgig6 = models.TextField(blank=True, null=True)
    rulesforgig7 = models.TextField(blank=True, null=True)
    rulesforgig8 = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.rulesforgig)


class Permissions(models.Model):
    permissionid = models.AutoField(primary_key=True)
    permission_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.permission_name)


class Userpermissions(models.Model):
    userpermissionid = models.AutoField(primary_key=True)
    userid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='userid', blank=True, null=True)
    permissionid = models.ForeignKey(
        Permissions, models.DO_NOTHING, db_column='permissionid', blank=True, null=True)

    def __str__(self):
        return str(self.permissionid)


class Languages(models.Model):
    languageid = models.AutoField(primary_key=True)
    languages = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.languageid)


class Images(models.Model):
    imageid = models.AutoField(primary_key=True)
    imagecaption = models.CharField(
        max_length=2000, default=None, blank=True, null=True)
    imagepath = models.ImageField(upload_to='',)
    im_userid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='im_userid', blank=True, null=True)

    def __str__(self):
        return str(self.imageid)


class Videos(models.Model):
    videosid = models.AutoField(primary_key=True)
    videosname = models.CharField(max_length=2000, blank=True, null=True)
    videospath = models.FileField(upload_to='')
    videopurpose = models.IntegerField(blank=True, null=True)
    purpose = models.CharField(max_length=2000, blank=True, null=True)
    vd_userid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='vd_userid', blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.videosid)


class VideosLink(models.Model):
    videosLinkid = models.AutoField(primary_key=True)
    videosLink = models.TextField(blank=True, null=True)
    videolinkpurpose = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='', blank=True, null=True)
    vl_userid = models.ForeignKey(
        Allusers, models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.videosLinkid)


class Home_Page_Detail(models.Model):
    id = models.AutoField(primary_key=True)
    Banner_Title = models.TextField(max_length=200, unique=True)
    Banner_Description = models.TextField(max_length=600, unique=True)
    Banner_Image = models.ImageField(upload_to='', db_index=True)
    Web_Title = models.CharField(max_length=70, unique=True)
    Web_Description = models.TextField(max_length=2000, unique=True)
    Box_Title1 = models.CharField(max_length=35, unique=True)
    Box_Title2 = models.CharField(max_length=70, unique=True)
    Box_Title3 = models.TextField(max_length=400, unique=True)
    Web_Image = models.ImageField(upload_to='', db_index=True)
    Title1 = models.CharField(max_length=100, unique=True)
    Description1 = models.TextField(unique=True)
    Title2 = models.CharField(max_length=100, unique=True)
    Description2 = models.TextField(unique=True)
    Title3 = models.CharField(max_length=100, unique=True)
    Description3 = models.TextField(unique=True)
    Title4 = models.CharField(max_length=100, unique=True)
    Description4 = models.TextField(unique=True)
    Title5 = models.CharField(max_length=100, unique=True)
    Description5 = models.TextField(unique=True)
    Title6 = models.CharField(max_length=100, unique=True)
    Description6 = models.TextField(unique=True)
    Total_Influencer = models.CharField(max_length=20, unique=True)
    Total_Client = models.CharField(max_length=20, unique=True)
    Total_Job_Completed = models.CharField(max_length=20, unique=True)
    Total_Category = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return str(self.id) + " || "+(self.Banner_Title)


class CompanyLogo(models.Model):
    id = models.AutoField(primary_key=True)
    Partner_Image = models.ImageField(upload_to='', db_index=True)

    def __str__(self):
        return str(self.Partner_Image)


class Testimonails(models.Model):
    id = models.AutoField(primary_key=True)
    Profile_Image = models.ImageField(upload_to='', db_index=True)
    Name = models.CharField(max_length=150,)
    Post = models.CharField(max_length=150,)
    Message = models.TextField()
    rating = models.IntegerField(default=0)
    approveuserid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='approveuserid', to_field='id', blank=True, null=True)
    testimonails_approved = models.BooleanField(
        default=False, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)+" || "+(self.Message)


class FooterDetail(models.Model):
    id = models.AutoField(primary_key=True)
    Footer_Quotes = models.CharField(
        max_length=500, default=None, blank=True, null=True, db_index=True)
    FacebookLink = models.CharField(
        max_length=150, default=None, blank=True, null=True, db_index=True)
    TwitterLink = models.CharField(
        max_length=150, default=None, blank=True, null=True, db_index=True)
    InstagramLink = models.CharField(
        max_length=150, default=None, blank=True, null=True, db_index=True)
    YoutubeLink = models.CharField(
        max_length=150, default=None, blank=True, null=True, db_index=True)
    WhatsappLink = models.CharField(
        max_length=150, default=None, blank=True, null=True, db_index=True)
    LinkedinLink = models.CharField(
        max_length=150, default=None, blank=True, null=True, db_index=True)
    WhatsappLink = models.CharField(
        max_length=150, default=None, blank=True, null=True, db_index=True)
    Emailid = models.CharField(
        max_length=150, default=None, blank=True, null=True, db_index=True)
    Phone1 = models.CharField(
        max_length=150, default=None, blank=True, null=True, db_index=True)
    Phone2 = models.CharField(
        max_length=150, default=None, blank=True, null=True, db_index=True)
    Address = models.CharField(
        max_length=150, default=None, blank=True, null=True, db_index=True)
    choosemeimage = models.ImageField(upload_to='',)

    def __str__(self):
        return str(self.id)


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20, default=None,
                            blank=True, null=True, db_index=True)
    Email = models.CharField(max_length=30, default=None,
                             blank=True, null=True, db_index=True)
    Subject = models.CharField(
        max_length=50, default=None, blank=True, null=True, db_index=True)
    Message = models.CharField(
        max_length=300, default=None, blank=True, null=True, db_index=True)

    def __str__(self):
        return str(self.id)


class FaqDetail(models.Model):
    id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=150, default=None,
                             blank=True, null=True, db_index=True)
    Description = models.CharField(
        max_length=1000, default=None, blank=True, null=True, db_index=True)

    def __str__(self):
        return str(self.id)


class PrivacyPolicyDetail(models.Model):
    id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=150, default=None,
                             blank=True, null=True, db_index=True)
    Description = models.TextField(
        default=None, blank=True, null=True, db_index=True)
    contentimage = models.ImageField(upload_to='', blank=True, null=True)

    def __str__(self):
        return str(self.id)+" || "+str(self.Title)


class TermsofServiceDetail(models.Model):
    id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=100, default=None,
                             blank=True, null=True, db_index=True)
    Description = models.TextField(
        default=None, blank=True, null=True, db_index=True)
    contentimage = models.ImageField(upload_to='', blank=True, null=True)

    def __str__(self):
        return str(self.id)+" || "+str(self.Title)


class AffiliateforbrandDetail(models.Model):

    id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=100, default=None,
                             blank=True, null=True, db_index=True)
    Description = models.TextField(
        default=None, blank=True, null=True, db_index=True)
    contentimage = models.ImageField(upload_to='', blank=True, null=True)

    def __str__(self):
        return str(self.id)+" || "+str(self.Title)


class AffiliateforinfluencerDetail(models.Model):
    id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=100, default=None,
                             blank=True, null=True, db_index=True)
    Description = models.TextField(
        default=None, blank=True, null=True, db_index=True)
    contentimage = models.ImageField(upload_to='', blank=True, null=True)

    def __str__(self):
        return str(self.id)+" || "+str(self.Title)


class RefundPolicyDetail(models.Model):
    id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=100, default=None,
                             blank=True, null=True, db_index=True)
    Description = models.TextField(
        default=None, blank=True, null=True, db_index=True)

    def __str__(self):
        return str(self.id)


class AboutDetail(models.Model):
    id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=150, default=None,
                             blank=True, null=True, db_index=True)
    Description = models.TextField(
        default=None, blank=True, null=True, db_index=True)

    def __str__(self):
        return str(self.id) + " || "+(self.Title)


'''Latest Model Start'''


class Useraccounts(models.Model):
    accountsid = models.AutoField(primary_key=True)
    usersid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='usersid', blank=True, null=True)
    bankname = models.TextField(blank=True, null=True)
    currencycode = models.TextField(blank=True, null=True)
    account_name = models.TextField(blank=True, null=True)
    accountnumber = models.TextField(blank=True, null=True)
    ifsc_codes = models.TextField(blank=True, null=True)


class UserDocuments(models.Model):
    documentsid = models.AutoField(primary_key=True)
    documentname = models.TextField(blank=True, null=True)
    documentpath = models.FileField(upload_to='accounts/',)
    usersid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='usersid', blank=True)
    dockyc = models.BooleanField(default=False)

    def __str__(self):
        return str(self.documentname)


class Services(models.Model):
    serviceid = models.AutoField(primary_key=True)
    servicename = models.TextField(blank=True, null=True)
    service_description = models.TextField(blank=True, null=True)
    subservice = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.serviceid)


class Careerpage(models.Model):
    careerpageid = models.AutoField(primary_key=True)
    bannertitle = models.TextField(blank=True, null=True)
    bannerdescription = models.TextField(blank=True, null=True)
    bannerimage = models.ImageField(upload_to='',)
    who_we_are_title = models.TextField(blank=True, null=True)
    who_we_are_description = models.TextField(blank=True, null=True)
    who_we_are_image = models.ImageField(upload_to='',)
    what_we_value_title = models.TextField(blank=True, null=True)
    what_we_value_description = models.TextField(blank=True, null=True)
    what_we_value_image = models.ImageField(upload_to='',)
    how_we_hire_title = models.TextField(blank=True, null=True)
    how_we_hire_description = models.TextField(blank=True, null=True)
    how_we_hire_image = models.ImageField(upload_to='',)
    what_we_do_title = models.TextField(blank=True, null=True)
    what_we_do_description = models.TextField(blank=True, null=True)
    what_we_do_image = models.ImageField(upload_to='',)

    def __str__(self):
        return str(self.careerpageid)+" || "+(self.bannertitle)


class CastingCallPage(models.Model):
    castingcallpageid = models.AutoField(primary_key=True)
    bannertitle = models.TextField(blank=True, null=True)
    bannerdescription = models.TextField(blank=True, null=True)
    bannerimage = models.ImageField(upload_to='',)

    def __str__(self):
        return str(self.castingcallpageid)


class AffiliateforbrandPage(models.Model):
    affiliateforbrandpageid = models.AutoField(primary_key=True)
    bannertitle = models.TextField(blank=True, null=True)
    bannerdescription = models.TextField(blank=True, null=True)
    bannerimage = models.ImageField(upload_to='',)

    def __str__(self):
        return str(self.affiliateforbrandpageid)


class AffiliateforinfluencerPage(models.Model):
    affiliateforinfluencerpageid = models.AutoField(primary_key=True)
    bannertitle = models.TextField(blank=True, null=True)
    bannerdescription = models.TextField(blank=True, null=True)
    bannerimage = models.ImageField(upload_to='',)

    def __str__(self):
        return str(self.affiliateforinfluencerpageid)


class Jobhiring(models.Model):
    jobhiringid = models.AutoField(primary_key=True)
    jobtitle = models.TextField(blank=True, null=True)
    designation = models.TextField(blank=True, null=True)
    joblocation = models.TextField(blank=True, null=True)
    aboutthejob = models.TextField(blank=True, null=True)
    rulesandresponsibilities = ArrayField(models.TextField(
        blank=True, null=True), default=list, blank=True, null=True)
    desiredcandidateprofile = ArrayField(models.TextField(
        blank=True, null=True), default=list, blank=True, null=True)
    added = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.jobhiringid)


class ServiceTax(models.Model):
    servicetaxid = models.AutoField(primary_key=True)
    servicetaxpercent = models.IntegerField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.servicetaxpercent)


class PricingPlans(models.Model):
    planid = models.AutoField(primary_key=True)
    planprice = models.BigIntegerField()
    plan_type = models.TextField(blank=True, null=True)
    planperks = ArrayField(models.TextField(
        blank=True, null=True), default=list, blank=True, null=True)
    usersid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='usersid', blank=True, null=True, related_name='plan_margin')
    serviceid = models.ForeignKey(
        Services, models.DO_NOTHING, db_column='serviceid', blank=True, null=True)
    # Field name made lowercase.
    deliverytime = models.DurationField(
        db_column='Deliverytime', default=timedelta(days=1), blank=True, null=True)
    exclusivedeliverytime = models.DurationField(
        db_column='exclusivedeliverytime', default=timedelta(days=1), blank=True, null=True)
    exculsiveprice = models.BigIntegerField(blank=True, null=True)
    priorityprice = models.BigIntegerField(blank=True, null=True)
    finalamount = models.BigIntegerField(blank=True, null=True)
    revisiontimes = models.IntegerField(blank=True, null=True)
    marginpercentage = models.FloatField(blank=True, null=True, default=10.0)
    increasedprice = models.BigIntegerField(blank=True, null=True)
    margin_amt = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.usersid)+'|'+str(self.serviceid)+'|'+str(self.plan_type)

    def duration_days(self):
        return int(self.deliverytime.total_seconds() / timedelta(days=1).total_seconds())

    def duration_days_exculsive(self):
        return int(self.exclusivedeliverytime.total_seconds() / timedelta(days=1).total_seconds())


'''Latest Model End'''


class Slots(models.Model):
    slotid = models.AutoField(primary_key=True)
    slottype = models.TextField(blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    slotperminprice = models.BigIntegerField(blank=True, null=True)
    slotduration = models.DurationField(blank=True, null=True)
    bookedduration = models.DurationField(blank=True, null=True)
    singleslotduration = models.IntegerField(default=20, blank=True,)

    isactive = models.BooleanField(default=False, blank=True, null=True)


class Subslots(models.Model):
    subslotid = models.AutoField(primary_key=True)
    slotid = models.ForeignKey(Slots, models.DO_NOTHING,
                               db_column='slotid', to_field='slotid', blank=True, null=True)
    influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    clientuserid = models.ForeignKey(ClientSettings, models.DO_NOTHING,
                                     db_column='clientid', to_field='csettingsuserid', blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    slotprice = models.BigIntegerField(blank=True, null=True)
    slotduration = models.DurationField(blank=True, null=True)
    recordingrequired = models.BooleanField(blank=True, null=True)
    isbooked = models.BooleanField(default=False, blank=True, null=True)
    recordingprice = models.BigIntegerField(default=10, blank=True, null=True)
    slotlink = models.TextField(blank=True, null=True)
    isreferenced = models.BooleanField(blank=True, null=True)


class Orderstatus(models.Model):
    statusid = models.AutoField(primary_key=True)
    status = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    statusdescription = models.TextField(
        db_column='Statusdescription', blank=True, null=True)

    def __str__(self):
        return str(self.statusid)


class Orders(models.Model):
    ordersid = models.AutoField(primary_key=True)
    orderdate = models.DateTimeField(blank=True, null=True)
    serviceid = models.ForeignKey(
        Services, models.DO_NOTHING, db_column='serviceid', blank=True, null=True)
    clientid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='clientid', to_field='id', blank=True, null=True)
    influencerid = models.ForeignKey(InfluencerProfile, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    rmid = models.IntegerField(blank=True, null=True)
    paymentstatus = models.BooleanField(blank=True, null=True)
    orderamt = models.BigIntegerField(blank=True, null=True)
    plantype = models.TextField(blank=True, null=True)

    orderdescription = models.TextField(blank=True, null=True)

    paymentcurrency = models.TextField(blank=True, null=True)
    exchangerate = models.FloatField(blank=True, null=True)
    convertedamt = models.BigIntegerField(blank=True, null=True)
    taxamt = models.FloatField(blank=True, null=True)
    taxpercentage = models.FloatField(blank=True, null=True)
    finalamt = models.BigIntegerField(blank=True, null=True)
    totaldiscount = models.BigIntegerField(blank=True, null=True)
    finalamtafterdiscount = models.BigIntegerField(blank=True, null=True)
    couponcodeid = models.IntegerField(blank=True, null=True)
    iscouponapplied = models.BooleanField(blank=True, null=True)

    planid = models.ForeignKey(
        PricingPlans, models.DO_NOTHING, db_column='planid', blank=True, null=True)
    orderstatus = models.ForeignKey(
        Orderstatus, models.DO_NOTHING, db_column='orderstatus', blank=True, null=True)

    subslotid = models.ForeignKey(
        Subslots, models.DO_NOTHING, db_column='subslotid', to_field='subslotid', blank=True, null=True)
    acceptancedate = models.DateTimeField(blank=True, null=True)
    cancelleddate = models.DateTimeField(blank=True, null=True)
    completedate = models.DateTimeField(blank=True, null=True)
    # For Account approved system the below filed is defined
    isrmapproved = models.BooleanField(default=False, blank=True, null=True)

    isresponseapprovedbyclient = models.BooleanField(
        default=False, blank=True, null=True)
    paymentrelease = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return str(self.ordersid)


class InfluencersReview(models.Model):
    influencersreviewid = models.AutoField(primary_key=True)
    clientid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='clientid', to_field='id', blank=True, null=True)
    influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    orderid = models.OneToOneField(
        Orders, models.DO_NOTHING, db_column='orderid', to_field='ordersid', blank=True, null=True, )
    review_message = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    isapproved = models.BooleanField(default=False, null=True, blank=True)
    approveuserid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='approveuserid', to_field='id', blank=True, null=True, related_name='approveuserid')
    date = models.DateTimeField(auto_now=True)


class OrderChat(models.Model):
    orderchatid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='userid', to_field='id', blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    date = models.DateTimeField(auto_now=True)
    orderid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='orderid', to_field='ordersid', blank=True, null=True, )

    def __str__(self):
        return str(self.orderchatid)

    def time_diff1(self):
        now = timezone.now()
        diff = now - self.date

        years, remainder = divmod(diff.days, 365)
        weeks, days = divmod(remainder, 7)
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_parts = []
        if years > 0:
            time_parts.append(f"{years} year{'s' if years > 1 else ''}")
            return ', '.join(time_parts) + ' ago'
        if weeks > 0:
            time_parts.append(f"{weeks} week{'s' if weeks > 1 else ''}")
            return ', '.join(time_parts) + ' ago'
        if days > 0:
            time_parts.append(f"{days} day{'s' if days > 1 else ''}")
            return ', '.join(time_parts) + ' ago'
        if hours > 0:
            time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
            return ', '.join(time_parts) + ' ago'
        if minutes > 0:
            time_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
            return ', '.join(time_parts) + ' ago'
        if seconds > 0:
            time_parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")
            return ', '.join(time_parts) + ' ago'


class Couponcodes(models.Model):
    couponcodesid = models.AutoField(primary_key=True)
    couponname = models.TextField(blank=True, null=True)
    coupondesc = models.TextField(blank=True, null=True)
    coupondiscount = models.IntegerField(blank=True, null=True, default=1)
    couponterms = models.TextField(unique=True, blank=True, null=True)
    influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    serviceid = models.ForeignKey(
        Services, models.DO_NOTHING, db_column='serviceid', blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    totalcodeused = models.IntegerField(blank=True, null=True)
    codeusedlimit = models.IntegerField(blank=True, null=True)
    activestatus = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.couponcodesid)


class BiddingHistoryTable(models.Model):
    historyid = models.AutoField(primary_key=True)
    orderid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='orderid', blank=True, null=True)
    bidderid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='bidderid', blank=True, null=True)
    bidamt = models.BigIntegerField(blank=True, null=True)
    bidstartingprice = models.BigIntegerField(blank=True, null=True)
    bidtime = models.DateTimeField(blank=True, null=True)
    slotid = models.ForeignKey(
        Slots, models.DO_NOTHING, db_column='slotid', blank=True, null=True)


class Invoices(models.Model):
    invoiceid = models.AutoField(primary_key=True)
    invoicedate = models.DateTimeField(blank=True, null=True)

    invoicedamount = models.BigIntegerField()
    # Field name made lowercase.
    taxamount = models.FloatField(db_column='Taxamount', blank=True, null=True)
    taxpercentage = models.FloatField(blank=True, null=True)
    # Field name made lowercase.
    finalamt = models.BigIntegerField(
        db_column='Finalamt', blank=True, null=True)
    ordersid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='ordersid')
    # Field name made lowercase.
    clientid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='clientid', to_field='id', blank=True, null=True)
    # Field name made lowercase.
    isbrand = models.BooleanField(db_column='IsBrand', blank=True, null=True)
    # Field name made lowercase.
    brandid = models.IntegerField(db_column='Brandid', blank=True, null=True)
    # Field name made lowercase.
    brandgstno = models.TextField(
        db_column='BrandGSTNO', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    brand_address = models.TextField(blank=True, null=True)
    invoicename = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='invoices/', blank=True, null=True)


class Countrytimezone(models.Model):
    countrytimezoneid = models.AutoField(primary_key=True)
    countrycode = models.TextField(blank=True, null=True)
    countryname = models.TextField(blank=True, null=True)
    timezone = models.TextField(blank=True, null=True)
    GMT_offset = models.TextField(blank=True, null=True)


class Webhook_Response(models.Model):
    Webhookresponse_id = models.AutoField(primary_key=True)
    paymentstatus = models.BooleanField(default=False)
    amount = models.BigIntegerField(default=0)
    clientid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='clientid', to_field='id', blank=True, null=True)
    payloadtype = models.TextField(blank=True, null=True)

    currencycode = models.TextField(blank=True, null=True)
    countrycode = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    mode = models.TextField(blank=True, null=True)
    stripepaymentid = models.TextField(blank=True, null=True)
    paymentmethodtype = models.TextField(blank=True, null=True)
    stripeapistatus = models.BooleanField(blank=True, null=True)
    orderid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='orderid', blank=True, null=True)

    def __str__(self):
        return str(self.Webhookresponse_id)


class Banktransfersfrompaymentgateway(models.Model):
    banktransfersfrompaymentgatewayid = models.AutoField(primary_key=True)
    paymentgatewaytype = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    id = models.TextField(blank=True, null=True)
    created = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)
    convertedamt = models.FloatField(blank=True, null=True)
    fees = models.FloatField(blank=True, null=True)
    netamount = models.FloatField(blank=True, null=True)
    convertedcurrency = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.banktransfersfrompaymentgatewayid)


class Payments(models.Model):
    paymentsid = models.AutoField(primary_key=True)
    paymentdate = models.DateTimeField(blank=True, null=True)
    ordersid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='ordersid', blank=True, null=True)
    webresponseid = models.ForeignKey(Webhook_Response, models.DO_NOTHING,
                                      db_column='webresponseid', to_field='Webhookresponse_id', blank=True, null=True)
    # Field name made lowercase.

    clientid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='clientid', to_field='id', blank=True, null=True, )
    invoiceid = models.ForeignKey(
        Invoices, models.DO_NOTHING, db_column='invoiceid', blank=True, null=True)
    paymentmethod = models.TextField(blank=True, null=True)
    amountpaid = models.IntegerField(blank=True, null=True)
    # Field name made lowercase.
    accountantid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='Accountantid', blank=True, null=True, related_name='accountuserid')
    transactionid = models.TextField(blank=True, null=True)

    is_refunded = models.BooleanField(
        db_column='is refunded', blank=True, null=True)
    insertiontime = models.DateTimeField(
        db_column='Insertiontime', blank=True, null=True)


class Refunds(models.Model):
    refundid = models.AutoField(primary_key=True)
    refundstatus = models.BooleanField(blank=True, null=True)
    refunddate = models.DateTimeField(blank=True, null=True)
    refundedfrom = models.BigIntegerField(blank=True, null=True)
    refundedto = models.BigIntegerField(blank=True, null=True)
    usersid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='usersid', blank=True, null=True)
    invoiceid = models.ForeignKey(
        Invoices, models.DO_NOTHING, db_column='invoiceid', blank=True, null=True)
    payments = models.ForeignKey(
        Payments, models.DO_NOTHING, db_column='payments', blank=True, null=True)
    refundedamt = models.BigIntegerField(blank=True, null=True)
    clientid = models.ForeignKey(
        ClientSettings, models.DO_NOTHING, db_column='clientid')
    orderid = models.ForeignKey(Orders, models.DO_NOTHING, db_column='orderid')


class Subscriptionplans(models.Model):
    planid = models.AutoField(primary_key=True)
    planname = models.TextField(blank=True, null=True)
    planamount = models.BigIntegerField(blank=True, null=True)
    planduration = models.DurationField(blank=True, null=True)
    planperks = models.TextField(blank=True, null=True)


class Subscribedusers(models.Model):
    subscriptionid = models.AutoField(primary_key=True)
    subscribeduserid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='subscribeduserid', blank=True, null=True)
    planid = models.ForeignKey(
        Subscriptionplans, models.DO_NOTHING, db_column='planid', blank=True, null=True)
    planactivationdate = models.DateTimeField(blank=True, null=True)
    planexpirydate = models.DateTimeField(blank=True, null=True)
    isactivesubscription = models.BooleanField(blank=True, null=True)


class Ordercancelreasons(models.Model):
    reasonid = models.AutoField(primary_key=True)
    orderid = models.OneToOneField(
        Orders, models.DO_NOTHING, db_column='orderid', blank=True, null=True)
    cancellationdate = models.DateTimeField(auto_now=True)
    reason = models.TextField(blank=True, null=True)
    usersid = models.ForeignKey(
        InfluencerProfile, models.DO_NOTHING, db_column='usersid', blank=True, null=True)
    clientid = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='clientid', to_field='id', blank=True, null=True)


class Alluserlogs(models.Model):
    alluserlogsid = models.AutoField(primary_key=True)
    userid = models.TextField(blank=True, null=True)
    path = models.TextField(blank=True, null=True)
    statuscode = models.TextField(blank=True, null=True)
    statustype = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)


class Accountprofile(models.Model):
    acoountprofileid = models.AutoField(primary_key=True)
    accountuserid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='accountuserid', blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    number = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='',)
    date = models.DateField(auto_now=True)


class Rmprofile(models.Model):
    profileid = models.AutoField(primary_key=True)
    rmid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='rmid', blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    number = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # This field type is a guess.
    languagesknown = ArrayField(models.IntegerField(
        blank=True, null=True), default=list, blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    profilepic = models.ImageField(
        upload_to='rmprofileimages/', blank=True, null=True)


class Kycprofile(models.Model):
    profileid = models.AutoField(primary_key=True)
    kycid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='kycid', blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    number = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # This field type is a guess.
    languagesknown = ArrayField(models.IntegerField(
        blank=True, null=True), default=list, blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    profilepic = models.ImageField(
        upload_to='kycuserimages/', default='default_avtar.webp', blank=True, null=True)


class Notifications(models.Model):
    notificationid = models.AutoField(primary_key=True)
    fromuserid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='fromuserid', blank=True, null=True, related_name='sender')
    touserid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='touserid', blank=True, null=True, related_name='receiver')
    rmid = models.ForeignKey(
        Rmsettings, models.DO_NOTHING, db_column='rmid', blank=True,  to_field='rmid', null=True)
    orderid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='orderid', blank=True, null=True)
    notificationpurpose = models.TextField(blank=True, null=True)
    notificationtime = models.DateTimeField(auto_now=True)
    notificationcontent = models.TextField(blank=True, null=True)
    notificationstatus = models.BooleanField(default=False, null=True)
    notificationtype = models.CharField(max_length=20, blank=True, null=True)

    def total_hours(self):
        now = datetime.now(timezone.utc)
        delta = now - self.notificationtime
        return delta.total_seconds() / 3600

    def rounded_total_hours(self, num_decimal_places=2):
        return round(self.total_hours(), num_decimal_places)

    def time_diff(self):
        now = timezone.now()
        diff = now - self.notificationtime

        years, remainder = divmod(diff.days, 365)
        weeks, days = divmod(remainder, 7)
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_parts = []
        if years > 0:
            time_parts.append(f"{years} year{'s' if years > 1 else ''}")
            return ', '.join(time_parts) + ' ago'
        if weeks > 0:
            time_parts.append(f"{weeks} week{'s' if weeks > 1 else ''}")
            return ', '.join(time_parts) + ' ago'
        if days > 0:
            time_parts.append(f"{days} day{'s' if days > 1 else ''}")
            return ', '.join(time_parts) + ' ago'
        if hours > 0:
            time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
            return ', '.join(time_parts) + ' ago'
        if minutes > 0:
            time_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
            return ', '.join(time_parts) + ' ago'
        if seconds > 0:
            time_parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")
            return ', '.join(time_parts) + ' ago'

        # now = datetime.now()
        # diff = now - make_aware(self.notificationtime)

        # days = diff.days
        # hours, remainder = divmod(diff.seconds, 3600)
        # minutes, seconds = divmod(remainder, 60)

        # return f"{days} days, {hours} hours, {minutes} minutes"


class Influencerhiringhistorytable(models.Model):
    historyid = models.AutoField(primary_key=True)
    producttype = models.TextField(blank=True, null=True)
    productid = models.TextField(blank=True, null=True)
    actions = models.TextField(blank=True, null=True)
    executiondate = models.DateTimeField(blank=True, null=True)
    rejectionreason = models.TextField(blank=True, null=True)
    actiondate = models.DateTimeField(blank=True, null=True)
    clientid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='clientid', blank=True, null=True)
    orderid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='orderid', blank=True, null=True)


class Rmtoinfluencermappings(models.Model):
    mappingid = models.AutoField(primary_key=True)
    mappingsdate = models.DateTimeField(auto_now=True)
    mapperid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='mapperid', to_field='id',  blank=True, null=True)
    mappedid = models.OneToOneField(
        InfluencerSettings, models.DO_NOTHING, db_column='mappedid', to_field='influencer_userid', blank=True, null=True, related_name='mappings')
    mappedtoid = models.ForeignKey(
        Rmsettings, models.DO_NOTHING, db_column='mappedtoid', to_field='rmid', blank=True, null=True)


class Casting_Call(models.Model):
    castingcallid = models.AutoField(primary_key=True)
    clientid = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='clientid', to_field='id', blank=True, null=True)
    brandlogo = models.ImageField(upload_to='', blank=True, null=True)
    brandbanner = models.ImageField(upload_to='', blank=True, null=True)
    productimage = models.ImageField(upload_to='', blank=True, null=True)
    posttitle = models.TextField(blank=True, null=True, unique=True)
    country = models.TextField(default='India', blank=True, null=True)
    allcountry = ArrayField(models.TextField(
        blank=True, null=True), default=list, blank=True, null=True)
    brandname = models.TextField(blank=True, null=True)
    requiredplatform = models.TextField(blank=True, null=True)
    compensation = models.TextField(blank=True, null=True)
    postkeyword = models.TextField(blank=True, null=True)
    postdescription = models.TextField(blank=True, null=True)
    cardcolor = models.TextField(blank=True, null=True)
    categoryid = models.ForeignKey(CastingCallCategories, models.DO_NOTHING, db_column='categoryid', to_field='castingcallcategorieid',
                                   blank=True, null=True)
    approved = models.BooleanField(blank=True, null=True)
    approvedby = models.ForeignKey(Rmsettings, models.DO_NOTHING,
                                   db_column='approvedby', to_field='rmid', blank=True, null=True)
    expirydate = models.DateField(blank=True, null=True)
    creationdate = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.castingcallid)


class PitchingCastingCall(models.Model):
    pitchingCastingCallid = models.AutoField(primary_key=True)
    castingcallid = models.ForeignKey(Casting_Call, models.DO_NOTHING,
                                      db_column='castingcallid', to_field='castingcallid', blank=True, null=True)
    influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    pitchtext = models.TextField(blank=True, null=True)
    workstatus = models.TextField(default='Not Completed')
    approved = models.BooleanField(default=False)
    pitchingfile = models.FileField(upload_to='')
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.pitchingCastingCallid)


class Callcastingquestions(models.Model):
    questionid = models.AutoField(primary_key=True)
    callcastid = models.ForeignKey(
        Casting_Call, models.DO_NOTHING, db_column='callcastid', blank=True, null=True)
    additiondate = models.DateTimeField(auto_now=True)
    title = models.TextField(blank=True, null=True)
    des = models.TextField(blank=True, null=True)
    clientid = models.ForeignKey(Allusers, models.DO_NOTHING,
                                 db_column='clientid', to_field='id', blank=True, null=True)


class Callcastingreasons(models.Model):
    reasonid = models.AutoField(primary_key=True)
    callcastid = models.OneToOneField(
        Casting_Call, models.DO_NOTHING, db_column='callcastid', blank=True, null=True)
    cancellationdate = models.DateTimeField(auto_now=True)
    reason = models.TextField(blank=True, null=True)
    cancelledby = models.ForeignKey(Rmsettings, models.DO_NOTHING,
                                    db_column='cancelledby', to_field='rmid', blank=True, null=True)


class Templates(models.Model):
    Template_type = [
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('wedding', 'Wedding'),
        ('motivation', 'Motivation'),
        ('others', 'Others'),
    ]
    templatesid = models.AutoField(primary_key=True)
    templatetext = models.TextField(blank=True, null=True)
    templatename = models.TextField(blank=True, null=True)
    templatetype = models.TextField(choices=Template_type)
    date = models.DateField(auto_now=True)
    userid = models.ForeignKey(Allusers, models.DO_NOTHING,
                               db_column='userid', to_field='id', blank=True, null=True)


class Eventtype(models.Model):
    eventtypeid = models.AutoField(primary_key=True)
    eventtype = models.TextField(blank=True, null=True)


class Eventtime(models.Model):
    eventtimeid = models.AutoField(primary_key=True)
    eventtime = models.TimeField(blank=True, null=True)


class Events(models.Model):
    eventid = models.AutoField(primary_key=True)
    eventname = models.TextField(blank=True, null=True)
    eventbookdate = models.DateField(blank=True, null=True)
    eventtypeid = models.ForeignKey(Eventtype, models.DO_NOTHING,
                                    db_column='eventtypeid', to_field='eventtypeid', blank=True, null=True)
    clientid = models.ForeignKey(ClientSettings, models.DO_NOTHING,
                                 db_column='clientid', to_field='csettingsuserid', blank=True, null=True)
    influencerid = models.ForeignKey(InfluencerSettings, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    bookinghours = models.DurationField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    clienttimezone = models.TextField(blank=True, null=True)
    eventorderdate = models.DateField(auto_now=True)


class Ordersrequirements(models.Model):
    requirementsid = models.AutoField(primary_key=True)
    ordersid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='ordersid', blank=True, null=True)
    serviceid = models.ForeignKey(
        Services, models.DO_NOTHING, db_column='serviceid', blank=True, null=True)
    subslotid = models.ForeignKey(
        Subslots, models.DO_NOTHING, db_column='subslotid', to_field='subslotid', blank=True, null=True)
    templatesid = models.ForeignKey(
        Templates, models.DO_NOTHING, db_column='templatesid', to_field='templatesid', blank=True, null=True)
    eventid = models.ForeignKey(
        Events, models.DO_NOTHING, db_column='eventid', to_field='eventid', blank=True, null=True)
    requirement = models.TextField(blank=True, null=True)


class EmployeeReview(models.Model):
    employeereviewid = models.AutoField(primary_key=True)
    employeename = models.TextField(blank=True, null=True)
    employeedesgination = models.TextField(blank=True, null=True)
    employeedepartment = models.TextField(blank=True, null=True)
    employeemessage = models.TextField(blank=True, null=True)
    employeeimage = models.ImageField(upload_to='',)
    creationdate = models.DateTimeField(auto_now=True, blank=True, null=True)
    userid = models.ForeignKey(
        Allusers, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return str(self.employeereviewid)+" || "+(self.employeename)
