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
            print(">>> TransactionCreateController post")
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
            print(">>> TransactionConfirmController post")
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
            print(">>> TransactionVerifyController post")
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
            print(">>> TransactionCancelController post")
            return cancel_a_transaction(token, data)