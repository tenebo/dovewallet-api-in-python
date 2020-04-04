def dovewallet_request(method,option,nonce=True):  
    import hashlib
    import Lib.hmac
    import requests
    import time
    BASE_URL = 'https://api.dovewallet.com/v1.1'
    publicKey = "PUBLICKEY"
    secretKey = "SECRETKEY"
    url = BASE_URL + method
    now = int(round(time.time() * 1000))
    query = f"apikey={publicKey}" 
    for i in option.items():
        query = query + "&" + i[0] + "=" + i[1]
    if nonce:
        query = query + "&" + f"nonce={now}"
    apisign = Lib.hmac.new(secretKey.encode(),(url+"?"+query).encode(), hashlib.sha512).hexdigest()
    r = requests.get(url+"?"+query, headers = {"apisign": apisign})
    return r.text

#Donations for original project: 35o179Nd4ZbhVJcRkGAeBe2vMpFKFi4zr9 (bitcoin)
