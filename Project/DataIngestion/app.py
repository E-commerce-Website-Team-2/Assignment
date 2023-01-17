import os
import psycopg2
from flask import Flask, request,url_for,redirect

app = Flask(__name__)

def db_connection(db_name):
    conn = psycopg2.connect(host='localhost',
                            database=db_name,
                            user='gourav' ,    #os.environ['DB_USERNAME'],
                            password='gourav')         #os.environ['DB_PASSWORD'])
    return conn


def validate(product):
    if(all(x in list(product.keys()) for x in ['uniqueId','name','price','productDescription','catlevel1Name','catlevel2Name','productImage'])):
        pass
    else:
        return 301
    if(str(type(product['price'])) not in ["<class 'float'>","<class 'int'>","<class 'double'>"]) :
        return 302
    if(str(type(product['name'])) != "<class 'str'>"):
        return 300
    if(str(type(product['uniqueId'])) != "<class 'str'>"):
        return 300
    if(str(type(product['productDescription'])) != "<class 'str'>"):
        return 300
    if(str(type(product['productImage'])) != "<class 'str'>"):
        return 300
    if(str(type(product['catlevel1Name'])) != "<class 'str'>"):
        return 300
    if(str(type(product['catlevel2Name'])) != "<class 'str'>"):
        return 300
    flag = checkID(product['uniqueId'],"products")
    return flag 

# Add the product details with the fields to the table
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
    



# Check if a table exists in the database
def check_table(table):
    conn = db_connection('data')
    cur = conn.cursor()
    cur.execute('select exists ( select * from '+ table + ");")
    exists = cur.fetchall()
    cur.close()
    conn.close()
    return exists


# Check if the particular productID is already existing in the database
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




@app.route('/products',methods = (['POST']))
def products():
    if request.method == 'POST':
        data = request.get_json()
        final_response = ""
        for product in data:
            status = validate(product)
            if(status == 200):
                databasestatus = write(product,['uniqueId','name','price','productDescription','catlevel1Name','catlevel2Name','productImage'],"products",False)
                if(databasestatus != 200):
                    final_response += product['uniqueId'] + "could not be added due to database error \n"
                else:
                    final_response += product['uniqueId'] + "added successfully \n"
            elif(status == 201):
                databasestatus = write(product,['uniqueId','name','price','productDescription','catlevel1Name','catlevel2Name','productImage'],"products",True)
                if(databasestatus != 200):
                    final_response += product['uniqueId'] + "could not be added due to database error \n"
                else:
                    final_response += product['uniqueId'] + "updated successfully \n"
            elif(status == 300):
                final_response += product['uniqueId'] + " the features of the product was not valid. Please recheck the features \n"
            elif(status == 301):
                final_response += product['uniqueId'] + "Features are missing \n"
            elif(status == 302):
                final_response += product['uniqueId'] + "Price feature is wrong \n"
            elif(status == 400):
                final_response += " Table doesnt exist \n"
            else:
                final_response += product['uniqueId'] + " had an unknown error \n"
        return final_response

app.run()


