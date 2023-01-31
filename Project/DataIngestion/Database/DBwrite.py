from psycopg2 import sql
from Database.DBmain import *
from Database.DBcheck import *
from Database.DBread import *



# This function will be capable of writing to the products table present in the database. 
def write(product,field,table,update):
    #Have to write code to get the category ID
    catid = readDB("category",["catid"],{"categoryname" : product["catlevel2Name"], "parentname": product["catlevel1Name"]})
    catid = catid[1][0][0]
    conn = db_connection('data')
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
def writeCategoryLevel1(category,table,field):
    tablepresent = check_table(table)
    present = False
    category = str(category)
    if tablepresent:
        present = CategoryPresent(category,table)
    if present[0][0] == False:
        conn = db_connection('data')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS ' + table + '(catid SERIAL  PRIMARY KEY,  '
                                                            'categoryname varchar(10485760) ,'
                                                            'parentname varchar(10485760) )' 
                                                              )
        cur.execute('INSERT INTO ' + table + ' (categoryname,parentname) VALUES (\'{0}\',\'{1}\'); '.format(str(category),"None"))
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
        cur.execute('CREATE TABLE IF NOT EXISTS ' + table + '(catid SERIAL PRIMARY KEY ,  '
                                                            'categoryname varchar(10485760) ,'
                                                            'parentname varchar(10485760) )'
                                                               )
        cur.execute('INSERT INTO ' + table + ' (categoryname,parentname) VALUES (\'{0}\',\'{1}\'); '.format(str(subCategory),str(category1)))
        conn.commit()
        cur.close()
        conn.close()
    return 200



