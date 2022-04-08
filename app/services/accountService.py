import uuid
from app.utils.baseFunc import encode_auth_token
from app.utils.decorator import tokenIssuerRequired
from app.utils.baseFunc import connection

def select_all_account():
    conn = connection()
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM public.account;""")
        data = cur.fetchall()
        print(">>> select_all_account successfully")
        return data
    except Exception as e:
        print(">>> select_all_account failed")
        print("Error: " +str(e))
        return 404

    finally:
        if conn is not None:
            cur.close()
            conn.close()

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
            data_dict = {
                "accountType": accountType,
                "accountId": accountId,
                "balance": balance
            }
            data = data_dict
            return data
    except Exception as e:
        print(">>> select_an_account failed")
        print("Error: " +str(e))
        return 404


def create_an_account(data):
    accountType = str(data['accountType'])
    if accountType == 'personal' or accountType == 'issuer':
        conn = connection()
        try:
            cur = conn.cursor()
            accountId = str(uuid.uuid4())
            cur.execute("""INSERT INTO public.account (accountId, accountType)
            VALUES ('{0}','{1}')""".format(accountId,accountType))
            conn.commit()    
            data = select_an_account(accountId,conn) 
            return data
        except Exception as e:
            print(">>> Cannot create account")
            print("Error: " +str(e))
            return 404

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    else:
        return 404

def create_a_merchant_account(accountId, merchantId):
    conn = connection()
    try:
        accountType = 'merchant'
        cur = conn.cursor()
        cur.execute("""INSERT INTO public.account (accountId, accountType, merchantId)
        VALUES ('{0}','{1}','{2}')""".format(accountId,accountType,merchantId))
        conn.commit()    
        cur.close()
        print("create a merchant account")
    except Exception as e:
        print(">>> Cannot create account")
        print("Error: " +str(e))
        return 404

    finally:
        if conn is not None:
            cur.close()
            conn.close()


def get_account_token(accountId):
    conn = connection()
    data = select_an_account(accountId,conn)
    if not data:
        return 404
    else:
        data = encode_auth_token(accountId)
        return data


@tokenIssuerRequired
def topup_account(token, data, param):
    conn = connection()
    accountId = data['accountId']
    try:
        cur = conn.cursor()
        cur.execute("""SELECT balance FROM public.account WHERE account.accountId = '{}'
        """.format(accountId))
        balance = float(cur.fetchone()[0]) 
        amount = balance + data['amount']

        cur.execute("""UPDATE public.account SET balance = {0}
        WHERE account.accountId = '{1}'""".format(amount, accountId))
        conn.commit()
        return "200"
    except Exception as e:
        print(">>> Cannot select an account from table account")
        print("Error: " +str(e))
        return 404

    finally:
        if conn is not None:
            cur.close()
            conn.close()