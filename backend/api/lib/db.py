from flask import current_app
from flask import g
import psycopg2


TEST_DB_NAME = 'adventureworks_test'
DB_NAME = 'adventureworks'

test_conn = psycopg2.connect(dbname = TEST_DB_NAME)
test_cursor = test_conn.cursor()

conn = psycopg2.connect(dbname = DB_NAME)
cursor = conn.cursor()

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(dbname = current_app.config['DATABASE'])
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def drop_records(cursor, conn, table_name):
    
    cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()

def drop_table_records(table_names, cursor, conn):
    for table_name in table_names:
        drop_records(cursor, conn, table_name)

def drop_all_table_records(conn, cursor):
    table_names = ["CountryRegion", "PersonPhone", "PhoneNumberType", 
  "Password", "EmailAddress", "BusinessEntityContact", 
  "ContactType", "BusinessEntityAddress", "ContactType",
  "BusinessEntityAddress", "AddressType", "StateProvince", "Person", "BusinessEntity"]
    drop_table_records(table_names, cursor, conn)


