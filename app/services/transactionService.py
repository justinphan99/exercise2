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
from datetime import datetime
import requests

def select_a_transaction(transactionId):
    try:
        conn = connection()
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
    finally:
        if conn is not None:
            cur.close()
            conn.close()    


@tokenMerchantRequired
def create_a_transaction(token, data):
    try:
        transactionId = str(uuid.uuid4())
        merchantId = data['merchantId']
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
            data = select_a_transaction(transactionId)
            return data
        
        except Exception as e:
            print(">>> Cannot create transaction")
            print("Error: " +str(e))
            return 404

        finally:
            if conn is not None:
                cur.close()
                conn.close()
    except:
        
        transactionId = str(uuid.uuid4())
        merchantId = data['merchantId']
        incomeAccount = decode_auth_token(token,data)
        amount = data['amount']
        extraData = data['extraData']
        dataTemp = {"merchantId": merchantId, "amount": amount, "extraData": extraData}
        signature = hashlib.md5(json.dumps(dataTemp).encode('utf-8')).hexdigest()
        status = 'FAILED'
       
        try:
            conn = connection()
            query = """INSERT INTO public.transaction 
            (transactionId, merchantId, incomeAccount, amount, extraData, signature, status)
            VALUES ('{0}','{1}', '{2}', {3}, '{4}', '{5}', '{6}');""".format(transactionId, merchantId, incomeAccount, amount, extraData, signature, status)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()    
            data = select_a_transaction(transactionId)
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
    balance_account = float(select_an_account(accountPersonalId)["balance"])
    transaction = select_a_transaction(transactionId)
    amount_transaction = float(transaction["amount"])
    status_old = transaction["status"]
    if status_old != 'INITIALIZED':
        return 404

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
        data = {
            "code": status,
            "message": "transaction {}".format(status)
        }
        update_order_status(transactionId,status)
        return data  
    except Exception as e:
        status = "FAILED"
        update_transaction_status(transactionId,status)
        print(">>> Cannot update transaction")
        print("Error: " +str(e))
        return 404
    finally:
        if conn is not None:
            cur.close()
            conn.close()

@tokenPersonalRequired
def verify_a_transaction(token, data):
    
    accountPersonalId = decode_auth_token(token,data)
    transactionId = data['transactionId']
    balance_account = float(select_an_account(accountPersonalId)["balance"])
    transaction = select_a_transaction(transactionId)
    merchantId = transaction["incomeAccount"]
    amount_transaction = float(transaction["amount"])
    status_old = transaction["status"]
    if status_old != 'CONFIRMED':
        return 404
    if balance_account>0 and balance_account>=amount_transaction:
        status = 'VERIFIED'
        balance_account = balance_account - amount_transaction
        update_balance_account(merchantId,amount_transaction)
    else:
        status = 'FAILED'
    try:
        conn = connection()
        query = """UPDATE public.transaction SET status = '{0}', outcomeAccount = '{1}'
        WHERE transaction.transactionId = '{2}'""".format(status, accountPersonalId, transactionId)
        cur = conn.cursor()
        cur.execute(query)

        query = """UPDATE public.account SET balance = {0}
        WHERE account.accountId = '{1}'""".format(balance_account, accountPersonalId)
        cur.execute(query)
        
        query = """UPDATE public.transaction SET status = '{0}', outcomeAccount = '{1}'
        WHERE transaction.transactionId = '{2}'""".format("COMPLETED", accountPersonalId, transactionId)
        cur.execute(query)

        conn.commit()

        data = {
            "code": status,
            "message": "transaction {}".format(status)
        }

        update_order_status(transactionId,"COMPLETED")
        return data
    
    except Exception as e:
        status = "FAILED"
        update_transaction_status(transactionId,status)
        update_order_status(transactionId,status)
        print(">>> Cannot update transaction")
        print("Error: " +str(e))
        return 404

    finally:
        if conn is not None:
            cur.close()
            conn.close()


@tokenPersonalRequired
def cancel_a_transaction(token, data):
    transactionId = data['transactionId']
    status = 'CANCELED'
    transaction = select_a_transaction(transactionId)
    status_old = transaction["status"]
    if status_old != 'CONFIRMED':
        return 404

    try:
        conn = connection()
        query = """UPDATE public.transaction SET status = '{0}'
        WHERE transaction.transactionId = '{1}'""".format(status, transactionId)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        data = {
            "code": status,
            "message": "transaction {}".format(status)
        }
        update_order_status(transactionId,status)

        return data
    
    except Exception as e:
        status = "FAILED"
        update_transaction_status(transactionId,status)
        update_order_status(transactionId,status)
        print(">>> Cannot cancel transaction")
        print("Error: " +str(e))
        return 404

    finally:
        if conn is not None:
            cur.close()
            conn.close()

def update_transaction_status(transactionId, status):
    query = """UPDATE public.transaction SET status = '{0}'
    WHERE transaction.transactionId = '{1}'""".format(status, transactionId)
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()    
        print("update transaction {0} to status {1}".format(transactionId,status))
        return 200
    except:
        return 404

def update_order_status(transactionId, payment_status):
    extraData = select_a_transaction(transactionId)["extraData"]
    merchantId = select_a_transaction(transactionId)["merchantId"]
    #url = select_a_merchant(merchantId,'',conn)['merchantUrl']
    url = "http://127.0.0.1:5000/order/status"
    data = {
        "order_id": extraData,
        "payment_status": payment_status
    }
    headers = {'Content-type': 'application/json'}
    a = requests.post(url=url,data=json.dumps(data), headers=headers)
    print(a.status_code)
    

def getAllNotExpiredTransaction():
    sql = """SELECT * FROM public.transaction
            WHERE status != 'CANCELED' AND status != 'COMPLETED' AND status != 'EXPIRED'
    """
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        transactions = []
        for item in data:
            transactions.append({
            "transactionId" : item[0],
            "merchantId" : item[1],           
            "incomeAccount" : item[2],
            "outcomeAccount" : item[3],
            "amount" : item[4],
            "extraData" : item[5],
            "signature" : item[6],
            "status" : item[7],
            "createdAt": item[8]
            })
        return transactions
    except Exception as e:
        print("Can\'t get all transaction, error: " + str(e))
        return 404
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def checkTransactionExpire():
    transactions = getAllNotExpiredTransaction()
    if (len(transactions) <= 0):
        print('No expired transaction found')
        return
    else:
        for tran in transactions:
            tranDateTime= tran['createdAt']
            now = datetime.now()
            expiredTime = ((now - tranDateTime).total_seconds())/60
            if (expiredTime > 5):
                update_transaction_status(tran['transactionId'],'EXPIRED')
                update_order_status(tran['transactionId'],'EXPIRED')