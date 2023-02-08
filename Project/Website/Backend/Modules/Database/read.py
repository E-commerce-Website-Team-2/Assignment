import psycopg2
import sys
sys.path.append("..")
from Modules.Database.main import *
from Modules.Database.check import *

# This function is able to perform a read request from the database. It will be able to do a Select From Where command
def read(table ,fields ,condition = {} , order = 0 ,check = 0):
    checkTable = check_table(table)
    numberOfFields = len(fields)
    if(checkTable):
        query = "Select "
        if(fields == "*"):
            query += "* "
        else:
            for field in range(numberOfFields):
                if(field == numberOfFields-1):
                    query += fields[field] + " "
                else:
                    query += fields[field] + ","
        query += " From " + table + " "
        if(condition != {} and check == 0):
            query += "Where "
            numberOfConditions = len(condition)
            passed = 0
            for field in condition:
                passed += 1
                if(passed != numberOfConditions):
                    query += field + " = \'" + condition[field] + "\'" + " AND "
                else:
                    query += field + " = \'" + condition[field] + "\'"
        if(condition != {} and check == 1):
            query += "Where "
            numberOfConditions = len(condition)
            passed = 0
            for field in condition:
                passed += 1
                if(passed != numberOfConditions):
                    query += field + " = \'" + condition[field] + "\'" + " OR "
                else:
                    query += field + " IN " + condition[field] 
        if(order != 0):
            if(order == 1):
                query += "Order By price ASC"
            elif(order == 2):
                query += "Order By price DESC"
        #With this the query is complete. We will now open a connection to the database and get the request from there. 
        conn = db_connection('data')
        cur = conn.cursor()    
        cur.execute(query)
        data = cur.fetchall()
        return [200,data]
    else:
        return [400,"Table Doesnt Exist"]
    