from psycopg2 import sql
import sys
import pandas as pd
sys.path.append("..")
from Modules.database.main import *
from Modules.database.check import *
from Modules.database.read import *



# This function will be capable of writing to the products table present in the database. 
def write(product,field,table,update):
    #Have to write code to get the category ID
    catid = read("category",["catid"],{"categoryname" : product["catlevel2Name"], "parentname": product["catlevel1Name"]})
    catid = catid[1][0][0]
    conn = database_connection('data')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ' + table + '(uniqueid varchar(10) PRIMARY KEY,'
                                 'name varchar (150) ,'
                                 'price decimal(7,2) ,'
                                 'product_description varchar(10485760) ,'
                                 'catid int,'
                                 'productImage varchar(10485760) NOT NULL,'
                                 'CONSTRAINT category '
                                 'FOREIGN KEY(catid) ' 
	                             'REFERENCES category(catid) );'

                                 )
    if update == False:
        stmt = sql.SQL('INSERT INTO products (uniqueid, name, price, product_description, catid, productImage)'
                'VALUES ({uniqueId},{name}, {price}, {productDescription}, {catid}, {productImage})').format(uniqueId = sql.Literal(product['uniqueId']),name = sql.Literal(product['name']),price = sql.Literal(product['price']),productDescription = sql.Literal(product['productDescription']),catid = sql.Literal(catid),productImage = sql.Literal(product['productImage']))
        cur.execute(stmt)
        conn.commit()
        cur.close()
        conn.close()
        return 200
    else:
        stmt = sql.SQL("UPDATE products SET name = {name},price = {price},product_description = {productDescription} ,catid = {catid}  ,productImage ={productImage} WHERE uniqueid = {uniqueId}").format(uniqueId = sql.Literal(product['uniqueId']),name = sql.Literal(product['name']),price = sql.Literal(product['price']),productDescription = sql.Literal(product['productDescription']),catid = sql.Literal(catid),productImage = sql.Literal(product['productImage']))
        cur.execute(stmt)  
        conn.commit()
        cur.close()
        conn.close()
        return 200



    

#This will be able to add a level 1 category to the database
def write_category_level_1(category,table,field):
    tablepresent = check_table(table)
    present = False
    category = str(category)
    if tablepresent:
        present = category_present(category,table)[0][0]
    if present == False:
        conn = database_connection('data')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS ' + table + '(catid SERIAL  PRIMARY KEY,  '
                                                            'categoryname varchar(10485760) ,'
                                                            'parentname varchar(10485760),'
                                                            'CONSTRAINT category '
                                                            'FOREIGN KEY(catid) ' 
	                                                        'REFERENCES category(catid) )' 
                                                              )
        cur.execute('INSERT INTO ' + table + ' (categoryname,parentname) VALUES (\'{0}\',\'{1}\'); '.format(str(category),"None"))
        conn.commit()
        cur.close()
        conn.close()
        return 200
    else:
        return 200



#This will be able to add a level 2 category to the database
def write_category_level_2(category1,subCategory,table):
    present = category_level_2_present(category1,subCategory,table)
    if present[0][0] == False:
        conn = database_connection('data')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS ' + table + '(catid SERIAL PRIMARY KEY ,  '
                                                            'categoryname varchar(10485760) ,'
                                                            'parentname varchar(10485760) )'
                                                               )
        cur.execute('INSERT INTO ' + table + ' (categoryname,parentname) VALUES (\'{0}\',\'{1}\'); '.format(str(subCategory),str(category1)))
        conn.commit()
        cur.close()
        conn.close()
    return 200





def writeEncoding(encoding,table):
    conn = database_connection('data')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ' + table + '(uniqueid varchar(10) PRIMARY KEY ,  '
                                                            'name_encoding DECIMAL(11,10) ARRAY ,'
                                                            'product_encoding DECIMAL(11,10) ARRAY, '
                                                            'CONSTRAINT product '
                                                            'FOREIGN KEY(uniqueid) ' 
	                                                        'REFERENCES products(uniqueid) )'
                                                               )
    stmt = sql.SQL('INSERT INTO ' + table + ' (uniqueid,name_encoding,product_encoding) '
                   'VALUES ({uniqueId},{name_encoding},{product_encoding}); ').format(uniqueId=sql.Literal(str(encoding["uniqueID"])),name_encoding=sql.Literal(encoding["name_encoding"].tolist()),product_encoding=sql.Literal(encoding["product_encoding"].tolist()))
    cur.execute(stmt)    
    conn.commit()
    cur.close()
    conn.close()
    return 200



def write_product_rating(product_rating,table):
    conn = database_connection('data')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ' + table + '(userid varchar(10)  ,  '
                                                            'productid varchar(10) ,'
                                                            'rating int, '
                                                            'CONSTRAINT product_id '
                                                            'FOREIGN KEY(productid) ' 
	                                                        'REFERENCES products(uniqueid) ,'
                                                            'PRIMARY KEY (productid,userid) )'
                                                               )
    stmt = sql.SQL('INSERT INTO ' + table + ' (userid,productid,rating) '
                   'VALUES ({userid},{productid},{rating}); ').format(userid=sql.Literal(str(product_rating["userid"])),productid=sql.Literal(product_rating["productid"]),rating=sql.Literal(product_rating["rating"]))
    cur.execute(stmt)    
    conn.commit()
    cur.close()
    conn.close()
    return 200
