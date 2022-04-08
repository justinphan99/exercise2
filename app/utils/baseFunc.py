import jwt
import datetime
import psycopg2

def connection():
    try:
        conn = psycopg2.connect(
        host="localhost",
        database="eWallet",
        user="admin",
        password="admin")
    except Exception as e:
        print(">>> Cannot connect to Database")
        print("Error: " + str(e))
    return conn

def select_an_account(accountId,conn):
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM public.account WHERE account.accountId = '{}'""".format(accountId))
        data = cur.fetchone()
        print(">>> select_an_account successfully")
        if data == None:
            return data
        else:
            accountType = data[1]
            accountId = data[0]
            balance = data[2]
            merchantId = data[3]
            data_dict = {
                "accountType": accountType,
                "accountId": accountId,
                "balance": balance,
                "merchantId": merchantId
            }
            data = data_dict
            return data
    except Exception as e:
        print(">>> select_an_account failed")
        print("Error: " +str(e))
        return 404


def select_a_merchant(merchantId, accountId, conn):
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM public.merchant WHERE merchant.merchantId = '{}'""".format(merchantId))
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


def encode_auth_token(accountId):
    try:
        conn = connection()
        merchantId = select_an_account(accountId,conn)['merchantId']
        print("merchantId encode")
        print(str(merchantId))
        if merchantId:
            key=select_a_merchant(merchantId,accountId,conn)['apiKey']
        else:
            key='8a2a77be-b657-11ec-b909-0242ac120002'
        print(key)
        payload = {
            'sub': accountId
        }
        token = jwt.encode(
            payload,
            key,
            algorithm='HS256'
        )
        print("token encode: "+str(token))
        return token
    except Exception as e:
        return e

def decode_auth_token(auth_token, data):
    try:
        conn = connection()
        print("data: " +str(data))

        if 'merchantId' in data:
            merchantId = data['merchantId']
            key=select_a_merchant(merchantId,'',conn)['apiKey']
        elif 'transactionId' in data:
            key = '8a2a77be-b657-11ec-b909-0242ac120002'
        else:
            key = '8a2a77be-b657-11ec-b909-0242ac120002'
        
        print("key: "+str(key))
        payload = jwt.decode(auth_token, key, algorithms=["HS256"])
        accountIddecode = payload['sub']
        print("accountIddecode: "+str(accountIddecode))
        return accountIddecode
    except Exception as e:
        print("error : " + str(e))

