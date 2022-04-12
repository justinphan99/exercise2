from ..utils.baseFunc import decode_auth_token
import app.services.accountService as AccountService
import psycopg2

def connection():
    try:
        conn = psycopg2.connect(
        host="localhost",
        database="exe2",
        user="admin",
        password="admin")
    except Exception as e:
        print(">>> Cannot connect to Database")
        print("Error: " + str(e))
    return conn

def getLoggedInAccount(authToken,data):
    if (authToken):
        resp = decode_auth_token(authToken,data)
        conn = connection()
        if resp:
            account = AccountService.select_an_account(resp)
            return account
        else:
            return None
    return None