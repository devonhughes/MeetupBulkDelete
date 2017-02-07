import requests
import lxml.html
from lxml.cssselect import CSSSelector

session = requests.session()
loginpg = session.get("https://secure.meetup.com/login/")
logindata = lxml.html.fromstring(loginpg.content)

token = logindata.forms[1].getchildren()[0].getchildren()[2].value
creds = {"email":"youremail", "password":"yourpassword", "token":token}

session.post('https://secure.meetup.com/login/', creds)

profilepg = session.get('https://www.meetup.com/members/yourmember#/')
readgroups = lxml.html.fromstring(profilepg.content)
groups = readgroups.cssselect("a.omngj_pswg4")

urls = []
for x in groups:
        urls.append(x.get("href").replace("members/yourmember#/", ""))
		
urls = set(urls)

unsub_urls = []
for x in urls:
    unsub_urls.append(x + "unsubscribe/")
    
for x in unsub_urls:
    unsubpg = session.get(x)
    unsubsession = lxml.html.fromstring(unsubpg.content)
    token = unsubsession.forms[0].getchildren()[0].value
    submit = {"exit comment":"!", "token":token, "op":"submit"}
    session.post(x, submit)	