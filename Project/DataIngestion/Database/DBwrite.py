import psycopg2
from Database.DBmain import *
from Database.DBcheck import *


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



