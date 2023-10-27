# # import instaloader 
# # L = instaloader.Instaloader() 
# # username = "ankit_singhx"
# # L.login("bol7test", "Rbinsta123$")
# # profile = instaloader.Profile.from_username(L.context, username) 
# # print("rahul")
# # print(profile.followers)


# # # import selenium
# # # from selenium import webdriver
# # # from selenium.webdriver.common.by import By
# # # from webdriver_manager.chrome import ChromeDriverManager
# # # from selenium.webdriver.chrome.options import Options
# # # import time

# # # def titikusersdet(user):

# # #     options = Options()
# # #     options.add_argument('--headless')
# # #     options.add_argument('--disable-gpu')

# # #     driver = webdriver.Chrome(
# # #         ChromeDriverManager().install(), chrome_options=options)

# # #     username=user

# # #     link = (f"https://www.tiktok.com/@{username}")

# # #     driver.get("" + link)
# # #     time.sleep(2)

# # #     Followers = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div/div[1]/h2[1]/div[2]/strong').text
# # #     Following = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div/div[1]/h2[1]/div[1]/strong').text
# # #     Likes = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[2]/div[2]/div/div[1]/h2[1]/div[3]/strong').text 

# # #     print(Followers) 
# # #     print(Following) 
# # #     print(Likes)
# # #     return Followers

# # # # # pd=PlatformDetails.objects.filter(usersid=57,platformtype=3)
# # # # if pd.exists():
# # # #     pd=pd[0]
# # # #     pd.subscribers_followers=Followers
# # # #     pd.save(update_fields=['subscribers_followers'])
# # # #     print("function execute")


# # # import instaloader
# # # bot = instaloader.Instaloader()
# # # profile = instaloader.Profile.from_username(bot.context, 'ankit_singhx')
# # # print("Username: ", profile.username)
# # # print("User ID: ", profile.userid)
# # # print("Number of Posts: ", profile.mediacount)
# # # print("Followers Count: ", profile.followers)
# # # print("Following Count: ", profile.followees)
# # # print("Bio: ", profile.biography)
# # # print("External URL: ", profile.external_url)

# # lis=[(20, 26, None, 'Brand Promotion'),(200, 26, None, 'Brand Promotion')]

# # print("dfsd",lis[1][0])
# # import secrets
# # import string
# # import hashlib

# # def generatetoken():
# #     # alphabet = string.ascii_letters + string.digits
# #     # token = ''.join(secrets.choice(alphabet) for i in range(64))
# #     salt = secrets.token_urlsafe(16)
    
# #     # Generate a unique token using a combination of salt and a strong random value
# #     token = salt + secrets.token_urlsafe(16)
    
# #     # Hash the token using a strong hash function like SHA-256
# #     token = hashlib.sha256(token.encode()).hexdigest()
    
# #     print(salt)
# #     print(token)
# #     return token

# # rb=generatetoken()
# # print("rbtoken",rb)



# # my_list = [{'subslotid': 377, 'slotid_id': 22, 'influencerid_id': 57, 'clientuserid_id': None, 'starttime': '2023-03-17 11:29:10.004907+00:00', 'endtime': '2023-03-17 11:39:10.004907+00:00', 'slotprice': 15250, 'slotduration': '0:10:00', 'recordingrequired': False, 'isbooked': False, 'slotlink': None, 'isreferenced': False, 'starttime_formatted': '11:29:10.004907', 'endtime_formatted': '11:39:10.004907'}, {'subslotid': 379, 'slotid_id': 22, 'influencerid_id': 57, 'clientuserid_id': None, 'starttime': '2023-03-17 11:49:10.004907+00:00', 'endtime': '2023-03-17 11:59:10.004907+00:00', 'slotprice': 15250, 'slotduration': '0:10:00', 'recordingrequired': False, 'isbooked': False, 'slotlink': None, 'isreferenced': False, 'starttime_formatted': '11:49:10.004907', 'endtime_formatted': '11:59:10.004907'}, {'subslotid': 380, 'slotid_id': 22, 'influencerid_id': 57, 'clientuserid_id': None, 'starttime': '2023-03-17 11:59:10.004907+00:00', 'endtime': '2023-03-17 12:09:10.004907+00:00', 'slotprice': 15250, 'slotduration': '0:10:00', 'recordingrequired': False, 'isbooked': False, 'slotlink': None, 'isreferenced': False, 'starttime_formatted': '11:59:10.004907', 'endtime_formatted': '12:09:10.004907'}]

# # for d in my_list:
# #     if d['subslotid'] == 379:
# #         print("Subslot ID 37 found!")
# #         pricwe=d['slotprice']
        
# # print(pricwe)


# # import pytz
# import pycountry
# # from datetime import datetime

# # # set the IST time as a datetime object
# # ist_time = datetime.now(pytz.timezone('Asia/Kolkata'))
# # print(type(ist_time),ist_time)
# # # time_str = '13:49:10.004907'
# # # time_format = '%H:%M:%S.%f' # format string to match the time format

# # # ist_time = datetime.strptime(time_str, time_format)

# # # set the target country
# # target_country = 'United States'

# # # get the ISO country code for the target country
# # iso_code = pycountry.countries.get(name=target_country).alpha_2

# # # get the timezone for the target country
# # target_tz = pytz.country_timezones.get(iso_code)[0]

# # # convert the IST time to the target timezone
# # target_time = ist_time.astimezone(pytz.timezone(target_tz))

# # print('IST Time:', ist_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
# # print(f'{target_country} Time:', target_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

# # import pytz
# # from datetime import datetime

# # # set the time string and the original timezone
# # def changetimeaccording_to_country(time):
# #     time_str = time
# #     original_tz = pytz.timezone('Asia/Kolkata')

# #     # set the target timezone based on the country
# #     target_country = 'United States'
# #     iso_code = pycountry.countries.get(name=target_country).alpha_2

# #     target_tz = pytz.country_timezones.get(iso_code)[0]

# #     # create a datetime object with the original time and timezone
# #     original_time = datetime.strptime(time_str, '%H:%M:%S.%f')
# #     original_time = original_tz.localize(original_time)

# #     # convert the original time to the target timezone
# #     target_time = str(original_time.astimezone(pytz.timezone(target_tz)))
# #     time_obj = datetime.fromisoformat(target_time)

# # # get the time with AM/PM format
# #     time_str1 = time_obj.strftime('%I:%M:%S %p') 

# #     print(f'Original Time: {time_str}')
# #     print(f'{target_country} Time: {time_str1}')
# #     return time_str1
    
# # t=changetimeaccording_to_country('13:49:10.004907')
# # print("Rahul",t)



# # import datetime
# # import pytz


# # utc_time = datetime.datetime.strptime('14:39:10.004907', '%H:%M:%S.%f').time()  # convert string to time object
# # utc_datetime = datetime.datetime.combine(datetime.datetime.now().date(), utc_time)  # create datetime object with today's date
# # utc_timezone = pytz.timezone('UTC')  # define UTC timezone
# # local_timezone = pytz.timezone('Asia/Kolkata')  # define your local timezone

# # local_datetime = utc_timezone.localize(utc_datetime).astimezone(local_timezone)  # convert UTC datetime to local datetime

# # print(local_datetime.time())

# # temp = ['apple', 'banana', 'orange', 'grape', 'pear','rahul','ss']
# # tup_temp = [(temp[i], temp[i+1]) if i+1 < len(temp) else (temp[i],) for i in range(0, len(temp), 2)]


# # print(tup_temp)


# from datetime import datetime, timedelta

# # get the current date
# def next30days():
#     current_date = datetime.now().date()

#     # create an empty list to store the next 30 dates
#     next_30_dates = []

#     # loop 30 times to generate the next 30 dates
#     for i in range(30):
#         # calculate the next date by adding one day to the current date
#         next_date = current_date + timedelta(days=i)

#         # append the next date to the list
#         next_30_dates.append(next_date)
#     return next_30_dates

# # print the next 30 dates
# days=next30days()
# print("list",days)