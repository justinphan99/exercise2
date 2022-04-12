from app.utils.baseFunc import connection

def create_table_merchant():
    try:
        conn = connection()
        cur = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS public.merchant
            (
                merchantName VARCHAR(200),
                merchantId UUID PRIMARY KEY,
                apiKey UUID,
                merchantUrl VARCHAR(200) DEFAULT 'http://localhost:5000/order/status'
            ); """
        cur.execute(query)
        conn.commit()
        print(">>> create table merchant successfully")
    except Exception as e:
        print(">>> ccreate table merchat failed")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def create_table_account():
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("""CREATE TYPE accountType AS ENUM ('merchant', 'personal', 'issuer');""")
        cur.execute("""CREATE TABLE IF NOT EXISTS public.account
        (
            accountId UUID PRIMARY KEY,
            accountType accountType,
            balance FLOAT DEFAULT 0,
            merchantId UUID REFERENCES merchant(merchantId)
        ); 
        """)
        conn.commit()
        print(">>> create table account successfully")
    except Exception as e:
        print(">>> ccreate table account failed")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def create_table_transaction():
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("""CREATE TYPE statusTransaction AS ENUM ('INITIALIZED', 'CONFIRMED', 'VERIFIED', 'CANCELED', 'EXPIRED', 'FAILED', 'COMPLETED')
        """)
        cur.execute("""CREATE TABLE IF NOT EXISTS public.transaction(
                transactionId UUID PRIMARY KEY,
                merchantId UUID REFERENCES merchant(merchantId),
                incomeAccount UUID,
                outcomeAccount UUID,
                amount FLOAT DEFAULT 0,
                extraData VARCHAR(200),
                signature VARCHAR(200),
                status statusTransaction,
                createdAt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print(">>> create table transaction successfully")
    except Exception as e:
        print(">>> ccreate table transaction failed")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_table_merchant()
    create_table_account()
    create_table_transaction()