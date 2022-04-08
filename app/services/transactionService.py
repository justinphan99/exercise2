import re
import uuid
from app.services.merchantService import select_a_merchant
from app.utils.baseFunc import decode_auth_token
import hashlib
import json
from app.services.accountService import *
from app.utils.decorator import tokenMerchantRequired, tokenPersonalRequired
from app.utils.baseFunc import connection
from app.utils.timeOut import timeout
import time
import requests

def select_a_transaction(transactionId,conn):
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM public.transaction WHERE transaction.transactionId = '{}'""".format(transactionId))
        data = cur.fetchone()
        if data == ():
            return data
        else:
            transactionId = data[0]
            merchantId = data[1]
            incomeAccount = data[2]
            outcomeAccount = data[3]
            amount = data[4]
            extraData = data[5]
            signature = data[6]
            status = data[7]
            data_dict = {
                "transactionId": transactionId,
                "merchantId": merchantId,
                "incomeAccount": incomeAccount,
                "outcomeAccount": outcomeAccount,
                "amount": amount,
                "extraData": extraData,
                "signature": signature,
                "status": status
            }
            data = data_dict
            return data
    except Exception as e:
        print(">>> Cannot select an transaction from table transaction")
        print("Error: " +str(e))
        return 404


@timeout(5)
def check_transaction_status(transactionId, conn):
    try:
        data = select_a_transaction(transactionId, conn)
        status = data['status']
        print(status)
        if status == "COMPLETED":
            return 1
        else:
            return check_transaction_status(transactionId,conn)
    except:
        print("outtttttt")


@tokenMerchantRequired
@timeout(5)
def create_a_transaction(token, data):
    try:
        print(data)
        transactionId = str(uuid.uuid4())
        merchantId = data['merchantId']
        print("9999999999999999")
        incomeAccount = decode_auth_token(token,data)
        amount = data['amount']
        extraData = data['extraData']
        dataTemp = {"merchantId": merchantId, "amount": amount, "extraData": extraData}
        signature = hashlib.md5(json.dumps(dataTemp).encode('utf-8')).hexdigest()
        status = 'INITIALIZED'
        try:
            conn = connection()
            query = """INSERT INTO public.transaction 
            (transactionId, merchantId, incomeAccount, amount, extraData, signature, status)
            VALUES ('{0}','{1}', '{2}', {3}, '{4}', '{5}', '{6}');""".format(transactionId, merchantId, incomeAccount, amount, extraData, signature, status)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()    
            print("create a transaction")
            data = select_a_transaction(transactionId, conn)
            print("not time out")
            return data
        
        except Exception as e:
            print(">>> Cannot create transaction")
            print("Error: " +str(e))
            return 404

        finally:
            if conn is not None:
                cur.close()
                conn.close()
    except TimeoutError():
        print("time out")
        transactionId = str(uuid.uuid4())
        merchantId = data['merchantId']
        incomeAccount = decode_auth_token(token,data)
        amount = data['amount']
        extraData = data['extraData']
        dataTemp = {"merchantId": merchantId, "amount": amount, "extraData": extraData}
        signature = hashlib.md5(json.dumps(dataTemp).encode('utf-8')).hexdigest()
        status = 'EXPIRED'
        merchantUrl = select_a_transaction(merchantId, conn)['merchantUrl']
        order_data = {
            "order_id": extraData,
            "payment_status": "EXPIRED"
        }
        try:
            conn = connection()
            query = """INSERT INTO public.transaction 
            (transactionId, merchantId, incomeAccount, amount, extraData, signature, status)
            VALUES ('{0}','{1}', '{2}', {3}, '{4}', '{5}', '{6}');""".format(transactionId, merchantId, incomeAccount, amount, extraData, signature, status)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()    
            print("create a transaction")
            data = select_a_transaction(transactionId, conn)
            print("not time out")

            requests.post(url=merchantUrl, data=order_data)

            return data
        
        except Exception as e:
            print(">>> Cannot create transaction")
            print("Error: " +str(e))
            return 404

        finally:
            if conn is not None:
                cur.close()
                conn.close()
     

@tokenPersonalRequired
def confirm_a_transaction(token, data):
    conn = connection()
    accountPersonalId = decode_auth_token(token,data)
    transactionId = data['transactionId']
    
    balance_account = float(select_an_account(accountPersonalId,conn)["balance"])
    amount_transaction = float(select_a_transaction(transactionId, conn)["amount"])

    if balance_account>0 and balance_account>=amount_transaction:
        status = 'CONFIRMED'
    else:
        status = 'FAILED'
    try:
        query = """UPDATE public.transaction SET status = '{0}', outcomeAccount = '{1}'
        WHERE transaction.transactionId = '{2}'""".format(status, accountPersonalId, transactionId)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()    
        print("confirm a transaction")
        data = {
            "code": status,
            "message": "transaction {}".format(status)
        }

        #update_order_status(transactionId,status,conn)

        return data
        
    except Exception as e:
        status = "FAILED"
        update_transaction_status(transactionId,status,conn)
        print(">>> Cannot update transaction")
        print("Error: " +str(e))
        return 404

    finally:
        if conn is not None:
            cur.close()
            conn.close()


@tokenPersonalRequired
def verify_a_transaction(token, data):
    conn = connection()
    accountPersonalId = decode_auth_token(token,data)
    transactionId = data['transactionId']
    balance_account = float(select_an_account(accountPersonalId,conn)["balance"])
    amount_transaction = float(select_a_transaction(transactionId, conn)["amount"])

    if balance_account>0 and balance_account>=amount_transaction:
        status = 'VERIFIED'
        balance_account = balance_account - amount_transaction
    else:
        status = 'FAILED'
    try:
        query = """UPDATE public.transaction SET status = '{0}', outcomeAccount = '{1}'
        WHERE transaction.transactionId = '{2}'""".format(status, accountPersonalId, transactionId)
        cur = conn.cursor()
        cur.execute(query)

        query = """UPDATE public.account SET balance = {0}
        WHERE account.accountId = '{1}'""".format(balance_account, accountPersonalId)
        cur.execute(query)
        conn.commit()

        #update_order_status(transactionId,status,conn)

        print("verify a transaction")

        data = {
            "code": status,
            "message": "transaction {}".format(status)
        }

        return data
    
    except Exception as e:
        status = "FAILED"
        update_transaction_status(transactionId,status,conn)
        print(">>> Cannot update transaction")
        print("Error: " +str(e))
        return 404

    finally:
        if conn is not None:
            cur.close()
            conn.close()


@tokenPersonalRequired
def cancel_a_transaction(token, data):
    conn = connection()
    transactionId = data['transactionId']
    status = 'CANCELED'

    try:
        query = """UPDATE public.transaction SET status = '{0}'
        WHERE transaction.transactionId = '{1}'""".format(status, transactionId)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        print("cancel a transaction")

        data = {
            "code": status,
            "message": "transaction {}".format(status)
        }
        #update_order_status(transactionId,status,conn)
        return data
    
    except Exception as e:
        status = "FAILED"
        update_transaction_status(transactionId,status,conn)
        print(">>> Cannot cancel transaction")
        print("Error: " +str(e))
        return 404

    finally:
        if conn is not None:
            cur.close()
            conn.close()

def update_transaction_status(transactionId, status, conn):
    query = """UPDATE public.transaction SET status = '{0}'
    WHERE transaction.transactionId = '{1}'""".format(status, transactionId)
    try:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()    
        return 200
    except:
        return 404

def update_order_status(transactionId, payment_status, conn):
    extraData = select_a_transaction(transactionId, conn)["extraData"]
    merchantId = select_a_transaction(transactionId, conn)["merchantId"]
    url = select_a_merchant(merchantId,'',conn)['merchantUrl']
    data = {
        "order_id": extraData,
        "payment_status": payment_status
    }
    headers = {'Content-type': 'application/json'}
    print(url)
    print(data)
    
    headers = {'Content-type': 'application/json'}

    a = requests.post(url=url,data=json.dumps(data), headers=headers)
    print(a.status_code)
    
