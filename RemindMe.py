import re
import subprocess
import mechanize
from urllib2 import HTTPError
from twilio.rest import Client
import os

# Your Account SID from twilio.com/console
account_sid = os.environ['account_sid']
# Your Auth Token from twilio.com/console
auth_token  = os.environ['auth_token']

client = Client(account_sid, auth_token)

br = mechanize.Browser()
# Open website to check availability
request = br.open("http://www.indianrail.gov.in/acc_avl.html")

# Set avaiability threshold limit 
threshold = 50

# List out day, month, train number, source and destination of trains
trains = [["15","12","16629","KZK","CLT"],["22","12","16629","KZK","CLT"]]

i = 0

while i < len(trains) :
    br.select_form("acc_avl")
    br["lccp_day"] = trains[i][0]
    br["lccp_month"] = trains[i][1]
    br["lccp_trnno"] = trains[i][2]
    br["lccp_srccode"] = trains[i][3]
    br["lccp_dstncode"] = trains[i][4]
    # Set class as Sleeper
    br["lccp_class1"] = ["SL"]
    # Set quota as General
    br["lccp_quota"] = ["GN"]
    
    try:
        # Submit form
        response = br.submit()
        res = response.read()
        
        #Save response source code in file for debugging
        f = open('html_response_code','w')
        f.write(res)
        f.close()
        
        #Pattern matching on response from br.submit()
        pattern = ["AVAILABLE \d+"]
        match = re.search(pattern[0],res)
        statustext = res[match.start():match.end()]
        currentavl = int(statustext.split()[1])
        print(currentavl)
        br.back()
        
        #Check if currrent availability less than threshold set
        if currentavl < threshold :
            message = client.messages.create(
            to="<your_phone_number>", 
            from_="<your_twilio_number>",
            body="Train:%s  from  %s-%s on  %s-%s-2017 has only %s seats left." % (train[2],train[3],train[4],train[0],train[1],currentavl))
            print ("Alert Send")
        
        # Increment i for next iteration
        i +=1
    except HTTPError:
        #Catch HTTP Error and redo the current iteration
        print ("404 Error")
        request = br.open("http://www.indianrail.gov.in/acc_avl.html")
        continue
