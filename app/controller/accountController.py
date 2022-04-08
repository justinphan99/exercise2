from app.services.accountService import select_all_account,create_an_account,get_account_token,topup_account

class AccountController():
    def __init__(self):
        self.method = None
        self.data = None
        
    def operation(self,token,data,param,query):
        if self.method == "GET":
            return select_all_account()
        elif self.method == "POST":
            return create_an_account(data)
        
class AccountTokenController():
    def __init__(self):
        self.method = None
        self.data = None
        
    def operation(self,token,data,param,query):
        if self.method == "GET":
            print("GET ACCOUNT TOKEN")
            return get_account_token(param)
        elif self.method == "POST":
            pass

class AccountTopupController():
    def __init__(self):
        self.method = None
        self.data = None
        
    def operation(self,token,data,param,query):
        if self.method == "GET":
            pass
        elif self.method == "POST":
            return topup_account(token,data,param)