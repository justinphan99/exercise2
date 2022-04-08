from app.services.transactionService import *

class TransactionCreateController():
    def __init__(self):
        self.method = None
        self.data = None
        self.accountId = None
        
    def operation(self,token,data,param,query):
        if self.method == "GET":
            pass
        elif self.method == "POST":
            return create_a_transaction(token, data)

class TransactionConfirmController():
    def __init__(self):
        self.method = None
        self.data = None
        self.accountId = None
        
    def operation(self,token,data,param,query):
        if self.method == "GET":
            pass
        elif self.method == "POST":
            return confirm_a_transaction(token, data)


class TransactionVerifyController():
    def __init__(self):
        self.method = None
        self.data = None
        self.accountId = None
        
    def operation(self,token,data,param,query):
        if self.method == "GET":
            pass
        elif self.method == "POST":
            return verify_a_transaction(token, data)


class TransactionCancelController():
    def __init__(self):
        self.method = None
        self.data = None
        self.accountId = None
        
    def operation(self,token,data,param,query):
        if self.method == "GET":
            pass
        elif self.method == "POST":
            return cancel_a_transaction(token, data)