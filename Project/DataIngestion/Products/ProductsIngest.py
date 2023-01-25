from Database import *
from Validate import *
from flask import request


#This is the main API function that will be called with a POST HTTP request when needed to add products into the database
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