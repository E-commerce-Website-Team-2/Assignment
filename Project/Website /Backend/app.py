from flask import Flask ,request, jsonify, request
from flask_cors import CORS
import psycopg2,requests,json


app = Flask(__name__)
CORS(app)



#This function will be able to create a connection to the database. It will be called everytime a connection 
# is asked for and should return a connection to the database as and when requested. 
def db_connection(db_name):
    conn = psycopg2.connect(host='localhost',
                            database=db_name,
                            user='gourav' ,    #os.environ['DB_USERNAME'],
                            password='gourav')         #os.environ['DB_PASSWORD'])
    return conn



#This will be able to check if a table that is meant to be in the database exists or not. 
def check_table(table):
    conn = db_connection('data')
    cur = conn.cursor()
    cur.execute('select exists ( select * from '+ table + ");")
    exists = cur.fetchall()
    cur.close()
    conn.close()
    return exists



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
    


#This will be able to search for products that have been passed as a query and will be re-routed to the Unbxd Search API. 
@app.route('/products/search', methods=["GET"])
def query():
    searchquery = request.args.get('query')
    start = 0   #(pagenumber - 1)*9
    rows = 9
    unbxdsearchAPI = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?q="
    finalquery = unbxdsearchAPI + searchquery + "&start=" + str(start) + "&rows=" + str(rows) + "&fields=" + "uniqueId,name,price,productImage"
    responseFromSearch = (requests.get(finalquery).content)
    responseFromSearch = json.loads(responseFromSearch)
    #Pagination will be carried out by using a page number as a variable in the URL 
    return responseFromSearch["response"]["products"]



#This will be able perform category filtering and will return products with an exact match. 
@app.route('/products/category', methods=["GET"])
def category():
    catlevel1 = request.args.get('cat1')
    catlevel2 = request.args.get('cat2')
    start = 0    #(pagenumber - 1)*9
    rows = 9
    if(catlevel1 == None):
        if(catlevel2 == None):
            return "There is no such filter possible"
            #This means that both were null. There is no way for me to filter from the database. 
        else:
            #This means only catlevel2 was given
            response = readDB("CategoryLevel2","*",{"catlevel2":catlevel2})
            if(response[1] != []):
                #This means that the category 2 is valid. Then we can query the products and return first 9. 
                response = readDB("products",["uniqueID","name","price","productimage"],{"catlevel2name":catlevel2})
                finalresponse = []
                for product in response[1][start:start+rows]:
                    finalresponse.append({"uniqueID":product[0],"name":product[1],"price":product[2],"productimage":product[3]})
                return finalresponse
            else:
                return {"Error":"The category chosen does not exist. "}
    elif(catlevel2 == None):
        #This means that only catlevel1 was given
        response = readDB("CategoryLevel1","*",{"catlevel1":catlevel1})
        if(response[1] != []):
            #This means that the category 1 is valid. Then we can query the products and return first 9.
            response = readDB("products",["uniqueID","name","price","productimage"],{"catlevel1name":catlevel1})
            finalresponse = []
            for product in response[1][start:start+rows]:
                finalresponse.append({"uniqueID":product[0],"name":product[1],"price":product[2],"productimage":product[3]})
            return finalresponse 
        else:
            return {"Error":"The category chosen does not exist. "} 
    else:
        #This means that both were given
        response = readDB("CategoryLevel2","*",{"catlevel1":catlevel1 , "catlevel2":catlevel2})
        if(response[1] != [] ):
            ##This means that both level of categories that have been given are correct. Therefore, we can query the products and return ther first 9. 
            response = readDB("products",["uniqueID","name","price","productimage"],{"catlevel1name":catlevel1 , "catlevel2name":catlevel2})
            finalresponse = []
            for product in response[1][start:start+rows]:
                finalresponse.append({"uniqueID":product[0],"name":product[1],"price":product[2],"productimage":product[3]})
            return finalresponse
        else:
            return {"Error":"The categories that have been selected are invalid."}






@app.route('/products/trending', methods=["GET"])
def trending():
    pass





#Will be able to load the entire category tree and send back a JSON to the front-end
@app.route('/products/getcategory', methods = ["GET"])
def getcategory():
    final = {}
    table1 = readDB('categorylevel1',"*")
    if(table1[0] == 200):
        for level1 in table1[1]:
            catlevel1 = level1[0]
            table2 = readDB("categorylevel2",["catlevel2"],{"catlevel1":catlevel1})
            catlevel2 = table2[1]
            for i in range(len(catlevel2)):
                catlevel2[i] = catlevel2[i][0]
            final[catlevel1] = catlevel2
    return final




#Will be able to send the extra details that need to be sent when the product itself is clicked. 
@app.route('/products/details/<productId>', methods=["GET"])
def details(productId):
    response = readDB("products",["product_description"],{"uniqueId":productId})
    return response[1] 


app.run()