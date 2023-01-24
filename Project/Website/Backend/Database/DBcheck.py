import psycopg2
from Database.DBmain import *

#This will be able to check if a table that is meant to be in the database exists or not. 
def check_table(table):
    conn = db_connection('data')
    cur = conn.cursor()
    cur.execute('select exists ( select * from '+ table + ");")
    exists = cur.fetchall()
    cur.close()
    conn.close()
    return exists




#This will be able to check if the particular productID is already existing in the database
def checkID(productId,table):
    if check_table(table):
        conn = db_connection('data')
        cur = conn.cursor()
        cur.execute('select * from ' + table + ' where uniqueid= \'' + productId + "';")
        products = cur.fetchall()
        cur.close()
        conn.close()
        if len(products) > 0:
            return 201
        else:
            return 200
    else:
        return 400





#This function will be able to check if the category level 1 is present in the table or not
def CategoryPresent(category,table):
    conn = db_connection('data')
    cur = conn.cursor()
    cur.execute('select exists ( select * from '+ table + ' Where catlevel1 = \'' + category + '\');')
    exists = cur.fetchall()
    cur.close()
    conn.close()
    return exists



#This function will be able to check if the category level 2 is present in the table or not 
def CategoryLevel2Present(category1,subCategory,table):
    conn = db_connection('data')
    cur = conn.cursor()
    cur.execute('select exists (select * from '+ table + ' Where catlevel1 = \'' + category1 + '\' AND catlevel2 = \'' + subCategory + '\');')
    exists = cur.fetchall()
    cur.close()
    conn.close()
    return exists
