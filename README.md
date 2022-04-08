#### ASSIGNMENT 2      

### You must install Python3 and Pip3 to run this project
    > I suggest using Python 3.9.10 and Pip 21.3.1

### DATABASE: PostgreSQL
    > username: admin
    > password: admin
    > database_name: eWallet

### CREATE AND ACTIVATE VITURAL ENVIROMENT
    > python3 -m venv env
    > source env/bin/activate

### INSTALL LIBRARY
    > pip3 install -r requirements.txt

### CREATE TABLE
    > table: merchant
    query = "
        CREATE TABLE IF NOT EXISTS public.merchant
        (
            merchantName VARCHAR(200),
            merchantId UUID PRIMARY KEY,
            apiKey UUID,
            merchantUrl VARCHAR(200) DEFAULT 'http://localhost:5000/order/status'
        ); 
    "

    > table: account
    query = "
        CREATE TYPE accountType AS ENUM ('merchant', 'personal', 'issuer');
        CREATE TABLE IF NOT EXISTS public.account
        (
            accountId UUID PRIMARY KEY,
            accountType accountType,
            balance FLOAT DEFAULT 0,
            merchantId UUID REFERENCES merchant(merchantId)
        ); 
    "

    > table: transaction
    query: "
        CREATE TYPE statusTransaction AS ENUM ('INITIALIZED', 'CONFIRMED', 'VERIFIED', 'CANCELED', 'EXPIRED', 'FAILED', 'COMPLETED');
        CREATE TABLE IF NOT EXISTS public.transaction(
            transactionId UUID PRIMARY KEY,
            merchantId UUID REFERENCES merchant(merchantId),
            incomeAccount UUID,
            outcomeAccount UUID,
            amount FLOAT DEFAULT 0,
            extraData VARCHAR(200),
            signature VARCHAR(200),
            status statusTransaction,
            createdAt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
        );
    "
### To run the project:
    > python3 main.py