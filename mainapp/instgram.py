



from bs4 import BeautifulSoup
import requests


# For Fetching Followers from Instagram
URL = "https://www.instagram.com/{}/"


def parse_data(s):
    data = {}
    s = s.split("-")[0]
    s = s.split(" ")
    data['Followers'] = s[0]
    data['Following'] = s[2]
    data['Posts'] = s[4]
    return data


def scrape_data(username):

    r = requests.get(URL.format(username))
    print("r",r)
    s = BeautifulSoup(r.text, "html.parser")
    print("s",s)
    meta = s.find("meta", property="og:description")
    print("meta",meta)
    return parse_data(meta.attrs['content'])

data=scrape_data('ankit_singhx')
print("data",data)