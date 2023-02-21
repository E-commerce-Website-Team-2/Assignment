import sys
sys.path.append("..")
from Modules.database import *
from Modules.validate import *
from flask import request



#This would be what is shown on the start when the page is loaded. At the moment its a call to get all the products in the database. 
def trending(pagenumber,sort):
    order = sort
    if(order == None or order == "" or order== " "):
        #print("I am making sure it can be passed as nothing")
        pass
    elif(order.isdigit()):
        order = int(order)
        if(order not in [1,2]):
            #print("Wrong integer passed")
            return [400,0,{}]
    else:
        #print("It is not an integer")
        return [400,0,{}]
    start = (int(pagenumber) - 1)*9
    rows = 9
    if(order == None or order == "" or order == " "):
        response = read(["ratings","products"],["uniqueid","name","price","productimage"],condition = {"products.uniqueid":"ratings.productid"},order = 3,average = "rating",groupby = "products.uniqueid")
    else:
        response = read("products",["uniqueID","name","price","productimage"],order = order)
    finalresponse = check_response(response,start,rows)
    return finalresponse



# This will be part of the API that will be able to load the trending items that are meant to be shown when 
# the user visits the website. Has not been implemeneted in either side. 
def set_trending():
    pass

