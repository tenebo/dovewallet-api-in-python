  
############################################################
#
# DOVEWALLET SELL COIN V_1
# 
# (c) mynameispyo.github.io
#
# More Info https://blog.naver.com/the3countrys/221961774253
#
# Donation Bitcoin: 3JmNLneiLvvNtcxGrnBjuemuqJbT44fzdq
#
#############################################################
import hashlib
import Lib.hmac
import requests
import time
import json

def dovewallet_request(method,option,nonce=True):
    BASE_URL = 'https://api.dovewallet.com/v1.1'
    global publicKey, secretKey
    url = BASE_URL + method
    now = int(round(time.time() * 1000))
    query = f"apikey={publicKey}" 
    for i in option.items():
        query = query + "&" + i[0] + "=" + i[1]
    if nonce:
        query = query + "&" + f"nonce={now}"
    apisign = Lib.hmac.new(secretKey.encode(),(url+"?"+query).encode(), hashlib.sha512).hexdigest()
    r = requests.get(url+"?"+query, headers = {"apisign": apisign})
    return json.loads(r.text)


def get_balance(currency):
    req = dovewallet_request("/account/getbalance", {"currency":currency}, nonce=False)
    req = req["result"]["Balance"]
    req = float(req)
    return req  

def get_orderbook(market, buy_or_sell):
    import json
    req = requests.get(f"https://api.dovewallet.com/v1.1/public/getorderbook?market={market}&type={buy_or_sell}")
    req = req.text
    req = json.loads(req)
    return req
    
def cancel_order(uuid):
    dovewallet_request("/market/cancel",{"uuid":uuid}, nonce=False)
    
### user setting ###
try:

    f  = open("sell_data.txt", "r")
    s = f.read().split()
    f.close()

    market = s[0]
    least_price = float(s[1])
    currency = s[2]
    quantity = s[3]
    publicKey = s[4]
    secretKey = s[5]

except:
    print("error")
else:
####################


    buy = True
    uuids = 0
    buy_price =0

    while True:
        if  buy:
            buy_price = (float(get_orderbook(market, "sell")["result"][0]["Rate"]) - 0.001) * 100000000 // 1 / 100000000
            if buy_price < least_price:
                buy_price = least_price
                time.sleep(10)
            method1 = "/market/selllimit"
            option1 = {
                "market": market,
                "quantity": str((get_balance(currency) / 1000 * 997) * 10000000000000000 // 1 / 10000000000000000  - 0.0001),
                "rate": str(buy_price),
            }
            a = dovewallet_request(method1, option1, nonce=False)
            #print(a)
            buy = False
            try:
                uuids = a["result"]["uuid"]
            except TypeError:
                print("amount error")
                buy=True
            print(f"sell in {buy_price}")
        time.sleep(1)
            
        if get_orderbook(market, "sell")["result"][0]["Rate"] < buy_price and buy == False:
            dovewallet_request("/market/cancel",{"uuid":str(uuids)}, nonce=False)
            print("cancel order")
            buy = True


