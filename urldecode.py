#urldecode tool
#tool imports
import base64
import hashlib
import hmac
import uuid
import datetime
import requests
import re

base_url = "https://xx-api.mimecast.com"
uri = "/api/ttp/url/decode-url"
url = base_url + uri
access_key = ""
secret_key = ""
app_id = ""
app_key = ""

def decodeurl(inputurl):
    secret_key2=base64.b64decode(secret_key)
    request_id = str(uuid.uuid4())
    hdr_date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " UTC"
    #https://docs.python.org/3/library/hmac.html
    listing=[hdr_date,request_id,uri,app_key]
    sep=':'
    stringtest=(sep.join(listing))
    salted=stringtest.encode('utf-8')
    hmac_sha1=hmac.new(secret_key2,salted,hashlib.sha1)
    sig=base64.b64encode(hmac_sha1.digest())
    sig=sig.decode()
    headers = {
        'Authorization': 'MC ' + access_key + ':' + sig,
        'x-mc-app-id': app_id,
        'x-mc-date': hdr_date,
        'x-mc-req-id': request_id,
        'Content-Type': 'application/json'
    }
    payload = {
            'data': [
                {
                    "url": inputurl
                }
            ]
        }
    r = requests.post(url=url, headers=headers, data=str(payload))
    og=r.text
    urls = re.search('((?<="url":")(.*?"))', og)
    result = urls.group()
    result = result[0:-1]
    return(result)
desiredresult=decodeurl(inputurl=input("Enter your url:"))
print(desiredresult)
