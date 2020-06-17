#-----------------------------------------------------
#
# Dovewallet Api Python Module
#
# Base on https://developer.dovewallet.com/api/v1/
#
# (C) https://mynameispyo.github.io
#
# Bitcoin Donation: 3JmNLneiLvvNtcxGrnBjuemuqJbT44fzdq
#
#-----------------------------------------------------

import hashlib
import Lib.hmac
import requests
import time
import json

class Dovewallet:
    def __init__(self, publicKey, secretKey):
        self.publicKey = publicKey
        self.secretKey = secretKey
    
    def dovewallet_request(self, method,option,nonce=True):
        url = 'https://api.dovewallet.com/v1.1' + method
        now = int(round(time.time() * 1000))
        query = f"apikey={self.publicKey}" 
        for i in option.items():
            query = query + "&" + i[0] + "=" + i[1]
        if nonce:
            query = query + "&" + f"nonce={now}"
        apisign = Lib.hmac.new(self.secretKey.encode(),(url+"?"+query).encode(), hashlib.sha512).hexdigest()
        r = requests.get(url+"?"+query, headers = {"apisign": apisign})
        return json.loads(r.text)
    
    #Public
    def getmarkets(self):
        return self.dovewallet_request("/public/getmarkets", {}, nonce=False)
    
    def getcurrencies(self):
        return self.dovewallet_request("/public/getcurrencies", {}, nonce=False)

    def getticker(self, market):
        return self.dovewallet_request("/public/getticker", {"market":market}, nonce=False)

    def getmarketsummaries(self):
        return self.dovewallet_request("/public/getmarketsummaries", {}, nonce=False)
    
    def getmarketsummary(self, market):
        return self.dovewallet_request("/public/getmarketsummary", {"market": market}, nonce=False)

    def getorderbook(self, market, type):
        return self.dovewallet_request("/public/getorderbook", {"market": market, "type": type}, nonce=False)

    def getmarkethistory(self, market):
        return self.dovewallet_request("/public/getmarkethistory", {"market": market}, nonce=False)

    #Market
    def buylimit(self, market, quantity, rate, walletid=None, nonce=False):
        option = {"market": market, "quantity": quantity, "rate": rate}
        if walletid != None:
            option["walletid"] = walletid
        if nonce != False:
            option["nonce"] = nonce
            nonce = True
        return self.dovewallet_request("/market/buylimit",option , nonce=nonce)
    
    def selllimit(self, market, quantity, rate, walletid=None, nonce=False):
        option = {"market": market, "quantity": quantity, "rate": rate}
        if walletid != None:
            option["walletid"] = walletid
        if nonce != False:
            option["nonce"] = nonce
            nonce = True
        return self.dovewallet_request("/market/selllimit",option , nonce=nonce)

    def cancel(self, uuid, walletid=None, nonce=False):
        option = {"uuid": uuid}
        if walletid != None:
            option["walletid"] = walletid
        if nonce != False:
            option["nonce"] = nonce
            nonce = True
        return self.dovewallet_request("/market/cancel",option , nonce=nonce)

    def getopenorders(self, market=None, walletid=None, nonce=True):
        option = {}
        if market != None:
            option["market"] = market
        if walletid != None:
            option["walletid"] = walletid
        if nonce != True:
            option["nonce"] = str(nonce)
            nonce = False
        return self.dovewallet_request("/market/getopenorders",option , nonce=nonce)

    #Account
    def getbalances(self, walletid=None, nonce=False):
        option = {}
        if walletid != None:
            option["walletid"] = walletid
        if nonce != False:
            option["nonce"] = str(nonce)
            nonce = True
        return self.dovewallet_request("/account/getbalances",option , nonce=nonce)
    
    def getbalance(self, currency, walletid=None, nonce=False):
        option = {"currency": currency}
        if walletid != None:
            option["walletid"] = walletid
        if nonce != False:
            option["nonce"] = str(nonce)
            nonce = True
        return self.dovewallet_request("/account/getbalance",option , nonce=nonce)

    def getdepositaddress(self,currency, walletid=None, nonce=False):
        option = {"currency": currency}
        if walletid != None:
            option["walletid"] = walletid
        if nonce != False:
            option["nonce"] = str(nonce)
            nonce = True
        return self.dovewallet_request("/account/getdepositaddress",option , nonce=nonce)

    def withdraw(self,currency, address, quantity,  walletid=None, nonce=False, memo=None):
        option = {"currency":currency, "address":address, "quantity":quantity}
        if walletid != None:
            option["walletid"] = walletid
        if memo != None:
            option["memo"] = memo
        if nonce != False:
            option["nonce"] = str(nonce)
            nonce = True
        return self.dovewallet_request("/account/withdraw",option , nonce=nonce)

    def transferbetweenmywallets(self,senderwalletid, receiverwalletid, currency,  quantity,  memo1=None, memo2=None, nonce=False):
        option = {"senderwalletid":senderwalletid, "receiverwalletid":receiverwalletid, "currency":currency, "quantity":quantity}
        if memo1 != None:
            option["memo1"] = memo1
        if memo2 != None:
            option["memo2"] = memo2
        if nonce != False:
            option["nonce"] = str(nonce)
            nonce = True
        return self.dovewallet_request("/account/transferbetweenmywallets",option , nonce=nonce)    

    def gettransactionhistory(self,currency, walletid=None,count=None, nonce=False):
        option = {"currency": currency}
        if walletid != None:
            option["walletid"] = walletid
        if count != None:
            option["count"] = count
        if nonce != False:
            option["nonce"] = str(nonce)
            nonce = True
        return self.dovewallet_request("/account/gettransactionhistory",option , nonce=nonce)

    def getorder(self,uuid,nonce=False):
        option = {"uuid": uuid}
        if nonce != False:
            option["nonce"] = str(nonce)
            nonce = True
        return self.dovewallet_request("/account/getorder",option , nonce=nonce)


    def getorderhistory(self,market=None,count=None, walletid=None, nonce=False):
        option = {}
        if market != None:
            option["market"] = market
        if count != None:
            option["count"] = count
        if walletid != None:
            option["walletid"] = walletid
        if nonce != False:
            option["nonce"] = str(nonce)
            nonce = True
        return self.dovewallet_request("/account/getdepositaddress",option , nonce=nonce)

    def getwithdrawalhistory(self,currency=None, count=None,nonce=False):
        option = {}
        if currency != None:
            option["currency"] = currency
        if count != None:
            option["count"] = count
        if nonce != False:
            option["nonce"] = str(nonce)
            nonce = True
        return self.dovewallet_request("/account/getwithdrawalhistory",option , nonce=nonce)


    def getdeposithistory(self,currency=None, count=None,nonce=False):
        option = {}
        if currency != None:
            option["currency"] = currency
        if count != None:
            option["count"] = count
        if nonce != False:
            option["nonce"] = str(nonce)
            nonce = True
        return self.dovewallet_request("/account/getdeposithistory",option , nonce=nonce)
    
    
    def geterror(self, error):
        error_dict = {'NETWORK_ERROR': 'Network Error.', 'DB_ERROR': 'DB Error.', 'UNEXPECTED_ERROR': 'Unexpected Error.', 'NO_DATA': 'There is no data.', 'ACCOUNT_LOCKED': 'The user account is locked.', 'WITHDRAWAL_NOT_AVAILABLE': 'The withdrawal request for the currency is not available.', 'VERIFICATION_NEEDED_FOR_WITHDRAWAL': 'You need higher verification level to make withdrawal requests.', 'EXCEEDED_WITHDRAWAL_LIMIT': 'The withdrawal request is exceeded the one day withdrawal limit.', 'BELOW_MIN_WITHDRAWAL_LIMIT': 'The withdrawal request is below the minimum withdrawal limit.', 'NOT_ENOUGH_BALANCE': "The wallet doesn't have enough currency. Check your available balance.", 'TOO_MANY_ORDERS': 'You have too many open orders.', 'WRONG_KEY': 'There is a no api key.', 'NO_PERMISSION': 'The api key has no permission.', 'KEY_NOT_MATCHING': "The api key doesn't match with yours.", 'INVALID_MARKET': 'The market name is wrong.', 'INVALID_TYPE': 'The order type is wrong.', 'INVALID_NONCE': 'The nonce is wrong.', 'INVALID_NUMBER': 'The number is wrong.', 'INVALID_ORDER_ID': 'The order id is wrong.', 'INVALID_CURRENCY': 'The currency is wrong.', 'INVALID_ADDRESS': 'The address is wrong.', 'INVALID_WALLETID': 'The wallet id is wrong.', 'INVALID_QUANTITY_OR_RATE': 'The quantity or the rate is wrong.', 'INVALID_RANGE_OF_TOTAL': 'The total is over the range.', 'INVALID_UUID': 'The uuid is wrong.', 'INVALID_SIGN': 'The sign is wrong.', 'MARKET_NOT_PROVIDED': 'The market name is missing.', 'TYPE_NOT_PROVIDED': 'The order type is missing.', 'CURRENCY_NOT_PROVIDED': 'The currency is missing.', 'QUANTITY_NOT_PROVIDED': 'The quantity is missing.', 'UUID_NOT_PROVIDED': 'The uuid is missing.', 'APIKEY_OR_APISIGN_NOT_PROVIDED': 'The api key or the apisign is missing.'}
        return error_dict.get(error)
 


#Donations for original project: 35o179Nd4ZbhVJcRkGAeBe2vMpFKFi4zr9 (bitcoin)
