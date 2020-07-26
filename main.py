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
    
    def request(self, method ,option, nonce=int(round(time.time() * 1000))):
        url = 'https://api.dovewallet.com/v1.1' + method
        query = f"apikey={self.publicKey}" 
        for i in option.items():
            query = query + "&" + i[0] + "=" + i[1]
        if nonce != None:
            query = query + "&" + f"nonce={nonce}"
        apisign = Lib.hmac.new(self.secretKey.encode(),(url+"?"+query).encode(), hashlib.sha512).hexdigest()
        r = requests.get(url+"?"+query, headers = {"apisign": apisign})
        return json.loads(r.text)
    
    def getError(self, error):
        error_dict = {'NETWORK_ERROR': 'Network Error.', 'DB_ERROR': 'DB Error.', 'UNEXPECTED_ERROR': 'Unexpected Error.', 'NO_DATA': 'There is no data.', 'ACCOUNT_LOCKED': 'The user account is locked.', 'WITHDRAWAL_NOT_AVAILABLE': 'The withdrawal request for the currency is not available.', 'VERIFICATION_NEEDED_FOR_WITHDRAWAL': 'You need higher verification level to make withdrawal requests.', 'EXCEEDED_WITHDRAWAL_LIMIT': 'The withdrawal request is exceeded the one day withdrawal limit.', 'BELOW_MIN_WITHDRAWAL_LIMIT': 'The withdrawal request is below the minimum withdrawal limit.', 'NOT_ENOUGH_BALANCE': "The wallet doesn't have enough currency. Check your available balance.", 'TOO_MANY_ORDERS': 'You have too many open orders.', 'WRONG_KEY': 'There is a no api key.', 'NO_PERMISSION': 'The api key has no permission.', 'KEY_NOT_MATCHING': "The api key doesn't match with yours.", 'INVALID_MARKET': 'The market name is wrong.', 'INVALID_TYPE': 'The order type is wrong.', 'INVALID_NONCE': 'The nonce is wrong.', 'INVALID_NUMBER': 'The number is wrong.', 'INVALID_ORDER_ID': 'The order id is wrong.', 'INVALID_CURRENCY': 'The currency is wrong.', 'INVALID_ADDRESS': 'The address is wrong.', 'INVALID_WALLETID': 'The wallet id is wrong.', 'INVALID_QUANTITY_OR_RATE': 'The quantity or the rate is wrong.', 'INVALID_RANGE_OF_TOTAL': 'The total is over the range.', 'INVALID_UUID': 'The uuid is wrong.', 'INVALID_SIGN': 'The sign is wrong.', 'MARKET_NOT_PROVIDED': 'The market name is missing.', 'TYPE_NOT_PROVIDED': 'The order type is missing.', 'CURRENCY_NOT_PROVIDED': 'The currency is missing.', 'QUANTITY_NOT_PROVIDED': 'The quantity is missing.', 'UUID_NOT_PROVIDED': 'The uuid is missing.', 'APIKEY_OR_APISIGN_NOT_PROVIDED': 'The api key or the apisign is missing.'}
        return error_dict.get(error)
 


#Donations for original project: 35o179Nd4ZbhVJcRkGAeBe2vMpFKFi4zr9 (bitcoin)
