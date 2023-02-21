import psycopg2
import sys
sys.path.append("..")
from Modules.database.main import *
from Modules.database.check import *

# This function is able to perform a read request from the database. It will be able to do a Select From Where command. 
#Functionality is being added to also perform an average and groupby as it is needed for trending
def read(table ,fields ,condition = {} , order = 0 ,check = 0,average = "",groupby = ""):
    if(type(table) == list):
        for tables in table:
            checkTable = check_table(tables)
            if(not checkTable):
                return [400,"Table Doesnt Exist"]
    else:
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
            if(average != ""):
                query += ",AVG(" + average + ") AS average "
        if(type(table) == list):
            number_of_tables = len(table)
            query += " From "
            for tables in range(number_of_tables):
                if(tables == number_of_tables-1):
                    query += table[tables] + " "
                else:
                    query += table[tables] + ","
        else:
            query += " From " + table + " "
        if(condition != {} and check == 0):
            query += "Where "
            numberOfConditions = len(condition)
            passed = 0
            if(type(table) == list):
                for field in condition:
                    passed += 1
                    if(passed != numberOfConditions):
                        query += field + " = " + condition[field] + "" + " AND "
                    else:
                        query += field + " = " + condition[field] + " "
            else:
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
            if(type(table) == list):
                for field in condition:
                    passed += 1
                    if(passed != numberOfConditions):
                        query += field + " = " + condition[field] + "" + " AND "
                    else:
                        query += field + " = " + condition[field] + " "
            else:
                for field in condition:
                    passed += 1
                    if(passed != numberOfConditions):
                        query += field + " = \'" + condition[field] + "\'" + " OR "
                    else:
                        query += field + " IN " + condition[field] 
        if(groupby != ""):
            query += "Group By " + groupby +  " "
        if(order != 0):
            if(order == 1):
                query += "Order By price ASC"
            elif(order == 2):
                query += "Order By price DESC"
            elif(order == 3):
                query += "Order By average DESC"
        #With this the query is complete. We will now open a connection to the database and get the request from there. 
        conn = database_connection('data')
        cur = conn.cursor()    
        cur.execute(query)
        data = cur.fetchall()
        return [200,data]
    else:
        return [400,"Table Doesnt Exist"]
    

