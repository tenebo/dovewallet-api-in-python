import hashlib
import Lib.hmac
import requests #you need to install using pip install requests
import time

BASE_URL = 'https://api.dovewallet.com/v1.1'
method = "/account/getbalances" #example of get balances
publicKey = "PUBLICKEY"
secretKey = "SECRETKEY"
url = BASE_URL + method
now = int(round(time.time() * 1000))
query = f"apikey=PUBLICKEY&nonce={now}"  #example of get balances
apisign = Lib.hmac.new(secretKey.encode(),(url+"?"+query).encode(), hashlib.sha512).hexdigest()
r = requests.get(url+"?"+query, headers = {"apisign": apisign})
print(r.text)
        
