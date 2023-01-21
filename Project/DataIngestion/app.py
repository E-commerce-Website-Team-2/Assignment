import os
import psycopg2
from flask import Flask, request,url_for,redirect

app = Flask(__name__)



#This function will be able to create a connection to the database. It will be called everytime a connection 
# is asked for and should return a connection to the database as and when requested. 
def db_connection(db_name):
    conn = psycopg2.connect(host='localhost',
                            database=db_name,
                            user='gourav' ,    #os.environ['DB_USERNAME'],
                            password='gourav')         #os.environ['DB_PASSWORD'])
    return conn



#This function will be able to validate any product that comes as input to the catalog. It will check if all the 
# necessary features are provided and if these features are valid or not. It will also check if the product is 
# being updated or a new one. The documentation explaining the meaning behind each error code will be given
def validate(product):
    string = "<class 'str'>"
    required = ['uniqueId','name','price','productDescription','catlevel1Name','catlevel2Name','productImage']
    if(all(x in list(product.keys()) for x in required)):
        pass
    else:
        missingFeatures = set(required) - set(list(product.keys()))
        error  = ""
        for i in missingFeatures:
            error += " " + i
        return [301,error]
    if(str(type(product['price'])) not in ["<class 'float'>","<class 'int'>","<class 'double'>"]) :
        return [302,"Price feature is wrong"]
    if(str(type(product['name'])) != string):
        return [303,"Name feature is wrong"]
    if(str(type(product['uniqueId'])) != string):
        return [304,"Unique Id is specified wrongly"]
    if(str(type(product['productDescription'])) != string):
        return [305,"Product Description is wrong"]
    if(str(type(product['productImage'])) != string):
        return [306,"Product Image is wrong"]
    if(str(type(product['catlevel1Name'])) != string):
        return [307,"Category Level 1 is wrong"]
    if(str(type(product['catlevel2Name'])) != string):
        return [308,"Category Level 2 is wrong"]
    flag = checkID(product['uniqueId'],"products")
    return [flag,"Good for database"] 




# This function will be capable of writing to the products table present in the database. 
def write(product,field,table,update):
    conn = db_connection('data')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ' + table + '(uniqueid varchar(10) PRIMARY KEY,'
                                 'name varchar (150) ,'
                                 'price decimal(7,2) ,'
                                 'product_description varchar(10485760) ,'
                                 'catlevel1name varchar(100),'
                                 'catlevel2name varchar(100),'
                                 'productImage varchar(10485760) NOT NULL);'
                                 )
    if update == False:
        cur.execute('INSERT INTO products (uniqueid, name, price, product_description, catlevel1name, catlevel2name, productImage)'
                'VALUES (%s,%s, %s, %s, %s, %s, %s)',
                (product['uniqueId'],product['name'],product['price'],product['productDescription'],product['catlevel1Name'],product['catlevel2Name'],product['productImage']))
        conn.commit()
        cur.close()
        conn.close()
        return 200
    else:
        cur.execute("UPDATE products SET name = $$\'" + product['name'] + "\'$$ ,price =\'" + str(product['price']) + '\', product_description = $$\'' + product['productDescription'] + '\'$$ ,catlevel1name =\'' + product['catlevel1Name'] + '\' ,catlevel2name =\'' + product['catlevel2Name'] + '\' ,productImage =\'' + product['productImage'] + '\' WHERE uniqueid = \'' + str(product['uniqueId']) + '\'')  
        conn.commit()
        cur.close()
        conn.close()
        return 200
    

#This will be able to add a level 1 category to the database
def writeCategoryLevel1(category,table,field):
    tablepresent = check_table(table)
    present = False
    category = str(category)
    if tablepresent:
        present = CategoryPresent(category,table)
    if present[0][0] == False:
        conn = db_connection('data')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS ' + table + '(catlevel1 varchar(10000) PRIMARY KEY)')
        cur.execute('INSERT INTO ' + table + ' (catlevel1) VALUES (\'{0}\'); '.format(str(category)))
        conn.commit()
        cur.close()
        conn.close()
        return 200
    else:
        return 200
    


#This will be able to add a level 2 category to the database
def writeCategoryLevel2(category1,subCategory,table):
    present = CategoryLevel2Present(category1,subCategory,table)
    if present[0][0] == False:
        conn = db_connection('data')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS ' + table + '( catlevel1 varchar(10000),' 
                                                        ' catlevel2 varchar(10000),'
                                                        'PRIMARY KEY (catlevel1,catlevel2) )')
        cur.execute('INSERT INTO ' + table + ' (catlevel1,catlevel2) VALUES (%s,%s)',(category1,subCategory))
        conn.commit()
        cur.close()
        conn.close()
    return 200


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


#This is the main API function that will be called with a POST HTTP request when needed to add products into the database
@app.route('/products',methods = (['POST']))
def products():
    if request.method == 'POST':
        new = 0
        failure = 0
        updates = 0 
        missing_features = 0
        missing = []
        data = request.get_json()
        final_response = ""
        for product in data:
            status = validate(product)
            message = status[1]
            status = status[0]
            if(status == 200):
                databasestatus = write(product,['uniqueId','name','price','productDescription','catlevel1Name','catlevel2Name','productImage'],"products",False)
                if(databasestatus != 200):
                    final_response += product['uniqueId'] + "could not be added due to database error \n"
                    failure += 1
                else:
                    #final_response += product['uniqueId'] + "added successfully \n"
                    new += 1
            elif(status == 201):
                databasestatus = write(product,['uniqueId','name','price','productDescription','catlevel1Name','catlevel2Name','productImage'],"products",True)
                if(databasestatus != 200):
                    final_response += product['uniqueId'] + "could not be added due to database error \n"
                    failure += 1
                else:
                    #final_response += product['uniqueId'] + "updated successfully \n"
                    updates += 1
            elif(status > 300 and status < 400):
                final_response += product['uniqueId'] + " " + message + "\n"
                missing_features += 1
            elif(status == 400):
                final_response += " Table doesnt exist \n"
                failure += 1
            else:
                final_response += product['uniqueId'] + " had an unknown error \n"
        return final_response + "New Products added: " + str(new) + "\n Products Updated: " + str(updates) + "\n Missing Features: " + str(missing_features) + "\n Failures due to database:" + str(failure)



#This will be the part of the API that will be able to add/update the category table. We will be expecting data 
#to be given in the following format. {"catLevel1":["List of all"] "catlevel2:["List of all"]}
@app.route('/category',methods = (['POST']))
def category():
    if request.method == "POST":
        data = request.get_json()
        final_response = ""
        for category in data:
            level1status  = writeCategoryLevel1(list(category.keys())[0],"CategoryLevel1",[])
            if(level1status == 200):
                final_response += "The category " + list(category.keys())[0] + " has been added \n"
                for categories in category[list(category.keys())[0]]:
                    level2status = writeCategoryLevel2(list(category.keys())[0],categories,"CategoryLevel2")
                    if(level2status != 200):
                        final_response += "The category " + list(category.keys())[0] + " Sub-category " + categories + " Failed due to database error. Please retry.\n"
                    else:
                        final_response += "The category " + list(category.keys())[0] + " Sub-category " + categories + " Has been added.\n"
            else:
                final_response += "The " + list(category.keys())[0] + " has failed due to database error. \n"
        return final_response
    

# This will be part of the API that will be able to load the trending items that are meant to be shown when 
# the user visits the website. Has not been implemeneted in either side. 
@app.route('/trending',methods = (['POST']))
def trending():
    pass


app.run()


