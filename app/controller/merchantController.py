from aiohttp import request
from app.services.merchantService import select_a_merchant,create_a_merchant,merchant_update_order_status

class MerchantController():
    def __init__(self):
        self.method = None
        self.data = None
        self.accountId = None
        
    def operation(self,token,data,param,query):
        if self.method == "GET":
            return select_a_merchant()
        elif self.method == "POST":
            print("POST merchant")
            return create_a_merchant(data)

class MerchantUpdateOrderController():
    def __init__(self):
        self.method = None
        self.data = None
        self.accountId = None
        
    def operation(self,token,data,param,query):
        if self.method == "GET":
            pass
        elif self.method == "POST":
            print("UPDATE ORDER STATUS")
            return merchant_update_order_status(data)