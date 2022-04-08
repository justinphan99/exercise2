import uuid
# from app.services.accountService import create_a_merchant_account
from app.utils.baseFunc import connection
import requests
import json

def select_all_merchant():
    conn = connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM public.merchant;
        """)
        data = cur.fetchall()
        print(data)
        print(">>> Select * from table merchant successfully")
        return data
    except Exception as e:
        print(">>> Cannot select * from table merchant")
        print("Error: " +str(e))
        return 404

    finally:
        if conn is not None:
            cur.close()
            conn.close()

def select_a_merchant(merchantId, accountId, conn):
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM public.merchant WHERE merchant.merchantId = '{0}'
        """.format(merchantId))
        data = cur.fetchone()
        merchantName = data[0]
        accountId = accountId
        merchantId = data[1]
        apiKey = data[2]
        merchantUrl = data[3]
        data_dict = {
            "merchantName": merchantName,
            "accountId": accountId,
            "merchantId": merchantId,
            "apiKey": apiKey,
            "merchantUrl": merchantUrl
        }
        data = data_dict
        print("select a merchant")
        return data
    except Exception as e:
        print(">>> Cannot select an merchant from table merchant")
        print("Error: " +str(e))
        return 404

def create_a_merchant(data):
    conn = connection()
    try:
        cur = conn.cursor()
        merchantName = str(data['merchantName'])
        accountId = str(uuid.uuid4())
        merchantId = str(uuid.uuid4())
        apiKey = str(uuid.uuid4())
        merchantUrl = str(data['merchantUrl'])
        cur.execute("""INSERT INTO public.merchant (merchantName,merchantId,apiKey,merchantUrl)
        VALUES ('{0}','{1}', '{2}', '{3}')
        """.format(merchantName,merchantId,apiKey,merchantUrl))
        conn.commit()  
        print("create a merchant")
        # create_a_merchant_account(accountId,merchantId)
        try:
            accountType = 'merchant'
            cur.execute("""INSERT INTO public.account (accountId, accountType, merchantId)
            VALUES ('{0}','{1}','{2}')""".format(accountId,accountType,merchantId))
            conn.commit()    
            print("create a merchant account")
        except:
            print(">>> Cannot create merchant account")
            print("Error: " +str(e))
            return 404

        data = select_a_merchant(merchantId, accountId, conn) 
        return data
    except Exception as e:
        print(">>> Cannot create merchant")
        print("Error: " +str(e))
        return 404

    finally:
        if conn is not None:
            cur.close()
            conn.close()


def merchant_update_order_status(data):
    url = "http://127.0.0.1:5000/order/status"
    headers = {'Content-type': 'application/json'}
    a = requests.post(url=url,data=json.dumps(data), headers=headers)
    print(a.json())
    return a.json()