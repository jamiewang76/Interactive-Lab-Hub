# -*- coding: utf-8 -*- 
username = 'ziyingwang76@gmail.com' # Your ClickSend username 
api_key = '0592FD37-2D0D-150E-7A56-000E6821998B' # Your Secure Unique API key 
msg_to = '+19178259760' # Recipient Mobile Number in international format (+61411111111 test number). 
msg_from = '' # Custom sender ID (leave blank to accept replies). 
msg_body = 'This is a test message' # The message to be sent. 
import json, subprocess 
request = { "messages" : [ { "source":"rpi", "from":msg_from, "to":msg_to, "body":msg_body } ] } 
request = json.dumps(request) 
cmd = "curl https://rest.clicksend.com/v3/sms/send -u " + username + ":" + api_key + " -H \"Content-Type: application/json\" -X POST --data-raw '" + request + "'" 
p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True) 
(output,err) = p.communicate() 
print 
output