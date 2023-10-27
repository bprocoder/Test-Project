
from .models import *
from datetime import datetime
import sys

def clientwishlist(clientid,country1):
    if country1 == 'India':
        currency = 'INR'
        country2='India'
    else:
        currency = 'USD'
        country2='United States'
    rates = ExchangeRates.objects.filter(country__icontains=country2).values('rates')[:1]
    rate_value = rates[0]['rates'] if rates else 1
    
    myctdata = []
    if clientid is not None:
        myct = Wishlist.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                # sys.stdout = open("approved.txt", "a")
                id3 = str(i.influencerid)
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                
                print('desc',shortdes)
                shortdes = Shortdescription.objects.get(
                    shortdescriptionid=shortdes).shortdestext
                image = str(name.profileimage)
                pr = PricingPlans.objects.get(
                    usersid=id3, plan_type='Basic', serviceid=1)
                basicpr = pr.increasedprice*rate_value
                wishlistid = i.wishlistid
                curre = currency
                useranme=Allusers.objects.get(id=id3).username
                locct = (fullname, destitle, shortdes,
                         basicpr, wishlistid, image, curre, id3,useranme)
                myctdata.append(locct)
    return myctdata



def clientcart(clientid,country1):
    if country1 == 'India':
        currency = 'INR'
        country2='India'
    else:
        currency = 'USD'
        country2='United States'
    rates = ExchangeRates.objects.filter(country__icontains=country2).values('rates')[:1]
    rate_value = rates[0]['rates'] if rates else 1
    usctdata = []
    if clientid is not None:
        myct = Cart.objects.filter(clientid=clientid)
        if myct.exists():
            for i in myct:
                print("cartid", i.Cartid)
                print("data", i.influencerid)
                id3 = str(i.influencerid)
                username = Allusers.objects.get(id=id3).username
                name = InfluencerProfile.objects.get(influencer_userid=id3)
                fullname = name.fullname
                destitle = name.desc_title
                shortdes = name.short_description
                shortdes = Shortdescription.objects.get(
                    shortdescriptionid=shortdes).shortdestext

                image = str(name.profileimage)
                pr = PricingPlans.objects.get(
                    usersid=id3, plan_type='Basic', serviceid=1)
                basicpr = pr.increasedprice*rate_value

                Cartid = i.Cartid
                curre = currency
                locct = (fullname, destitle, shortdes,
                         basicpr, Cartid, image, curre, id3, username)
                usctdata.append(locct)
    return usctdata


def generatewallettransaction_id(transaction_id):
    # Generate a UUID4, which is a randomly generated UUID
    
    
    # Convert the UUID to a string
    transaction_id_str = str(transaction_id)

    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time as a string
    datetime_str = current_datetime.strftime("%Y%m%d%H%M%S")

    # Combine the "wallet" string, date, time, and UUID to create the unique ID
    unique_id = f"wallet{datetime_str}{transaction_id_str}"
    
    return unique_id
