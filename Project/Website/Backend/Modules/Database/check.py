from psycopg2 import sql
import sys
sys.path.append("..")
from Modules.Database.main import *

#This will be able to check if a table that is meant to be in the database exists or not. 
def check_table(table):
    conn = db_connection('data')
    cur = conn.cursor()
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (table,))
    exists = cur.fetchone()[0]
    cur.close()
    conn.close()
    return exists




#This will be able to check if the particular productID is already existing in the database
def checkID(productId,table):
    if check_table(table):
        conn = db_connection('data')
        cur = conn.cursor()
        query = sql.SQL(""" 
        Select * 
        From  products  
        Where uniqueid= {productId} """).format(productId = sql.Literal(productId))
        cur.execute(query)
        products = cur.fetchall()
        cur.close()
        conn.close()
        if len(products) > 0:
            return 201
        else:
            return 200
    else:
        return 200





#This function will be able to check if the category level 1 is present in the table or not
def CategoryPresent(category,table):
    conn = db_connection('data')
    cur = conn.cursor()
    stmt = sql.SQL("""
    Select Exists 
    ( Select * 
    From {table} 
    Where categoryname = {category} ) """).format(table = sql.Identifier(table) , category = sql.Literal(category))
    cur.execute(stmt)
    exists = cur.fetchall()
    cur.close()
    conn.close()
    return exists



#This function will be able to check if the category level 2 is present in the table or not 
def CategoryLevel2Present(category1,subCategory,table):
    conn = db_connection('data')
    cur = conn.cursor()
    stmt = sql.SQL("""
    Select Exists 
    ( Select * 
    From {table} 
    Where categoryname = {subCategory} AND parentname = {category} )""").format(table = sql.Identifier(table) , category = sql.Literal(category1) , subCategory = sql.Literal(subCategory))
    cur.execute(stmt)
    exists = cur.fetchall()
    cur.close()
    conn.close()
    return exists
