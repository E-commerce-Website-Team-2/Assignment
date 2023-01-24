import psycopg2
from Database.DBmain import *
from Database.DBcheck import *



# This function is able to perform a read request from the database. It will be able to do a Select From Where command
def readDB(table ,fields ,condition = False ):
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
        if(condition != False):
            query += "Where "
            numberOfConditions = len(condition)
            passed = 0
            for field in condition:
                passed += 1
                if(passed != numberOfConditions):
                    query += field + " = \'" + condition[field] + "\'" + " AND "
                else:
                    query += field + " = \'" + condition[field] + "\'"
        #With this the query is complete. We will now open a connection to the database and get the request from there. 
        conn = db_connection('data')
        cur = conn.cursor()    
        cur.execute(query)
        data = cur.fetchall()
        return [200,data]
    else:
        return [400,"Table Doesnt Exist"]
    