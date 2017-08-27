import re
import subprocess
import mechanize
from urllib2 import HTTPError
from twilio.rest import Client
#from plyer import notification
# import BeautifulSoup

# Your Account SID from twilio.com/console
account_sid = "<replace_account_sid>"
# Your Auth Token from twilio.com/console
auth_token  = "<replace_auth_token>"

client = Client(account_sid, auth_token)

br = mechanize.Browser()
request = br.open("http://www.indianrail.gov.in/acc_avl.html")

trains = [["15","09","16629","KZK","CLT"],["22","09","16629","KZK","CLT"]]

i = 0

while i < len(trains) :
    br.select_form("acc_avl")
    br["lccp_day"] = trains[i][0]
    br["lccp_month"] = trains[i][1]
    br["lccp_trnno"] = trains[i][2]
    br["lccp_srccode"] = trains[i][3]
    br["lccp_dstncode"] = trains[i][4]
    br["lccp_class1"] = ["SL"]
    br["lccp_quota"] = ["GN"]
    try:
        response = br.submit()
        res = response.read()
        f = open('html_response_code','w')
        f.write(res)
        f.close()
        pattern = ["AVAILABLE \d+"]
        match = re.search(pattern[0],res)
        statustext = res[match.start():match.end()]
        currentavl = int(statustext.split()[1])
        print(currentavl)
        br.back()
        if currentavl < 160 :
            # message = client.messages.create(
            # to="+919495206270", 
            # from_="+13853932702",
            # body="Train:%s  from  %s-%s on  %s-%s-2017 has only %s seats left." % (train[2],train[3],train[4],train[0],train[1],currentavl))
            print ("Alert Send")
        i +=1
    except HTTPError:
        print ("404 Error")
        request = br.open("http://www.indianrail.gov.in/acc_avl.html")
        continue