from Database import *
from Validate import *
from flask import request




#This will be able perform category filtering and will return products with an exact match.
def category(pagenumber : int):
    catlevel1 = request.args.get('cat1')
    catlevel2 = request.args.get('cat2')
    order = request.args.get('sort')
    if(order == None or order == ""):
        pass
    elif(order.isdigit()):
        order = int(order)
        if(order not in [1,2]):
            return [400,0,{}]
    else:
        return [400,0,{}]
    start = (int(pagenumber) - 1)*9
    rows = 9
    if(catlevel1 == None):
        if(catlevel2 == None):
            return [400,0,{}]
            #This means that both were null. There is no way for me to filter from the database. 
        else:
            #This means only catlevel2 was given
            response = readDB("categorylevel2","*",{"catlevel2":catlevel2})
            if(response[1] != []):
                #This means that the category 2 is valid. Then we can query the products and return first 9. 
                response = readDB("products",["uniqueID","name","price","productimage"],{"catlevel2name":catlevel2},order)
                finalresponse = checkResponse(response,start,rows)
                return finalresponse
            else:
                return [400,0,{}]
    elif(catlevel2 == None):
        #This means that only catlevel1 was given
        response = readDB("categorylevel1","*",{"catlevel1":catlevel1})
        if(response[1] != []):
            #This means that the category 1 is valid. Then we can query the products and return first 9.
            response = readDB("products",["uniqueID","name","price","productimage"],{"catlevel1name":catlevel1},order)
            finalresponse = checkResponse(response,start,rows)
            return finalresponse
        else:
            return [400,0,{}] 
    else:
        #This means that both were given
        response = readDB("categorylevel2","*",{"catlevel1":catlevel1 , "catlevel2":catlevel2})
        if(response[1] != [] ):
            ##This means that both level of categories that have been given are correct. Therefore, we can query the products and return ther first 9. 
            response = readDB("products",["uniqueID","name","price","productimage"],{"catlevel1name":catlevel1 , "catlevel2name":catlevel2},order)
            finalresponse = checkResponse(response,start,rows)
            return finalresponse
        else:
            return [400,0,{}]



