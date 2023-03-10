import sys
sys.path.append("..")
from Modules.database import *
from Modules.validate import *
from flask import request



#This will be able perform category filtering and will return products with an exact match.
def category(pagenumber,categoryid,sort):
    catid = categoryid
    if(catid.isdigit()):
        catid = int(catid)
        status = read("category",["categoryname"],{"catid":str(catid)})[1]
        if(status == []):
            return [400,[],{}]
    print(catid,sort)
    order = sort
    if(order == None or order == "" or order == " "):
        print("I am making sure it can be passed as nothing")
        pass
    elif(order.isdigit()):
        order = int(order)
        if(order not in [1,2]):
            print("Wrong integer passed")
            return [400,0,{}]
    else:
        print("It is not an integer")
        return [400,0,{}]
    start = (int(pagenumber) - 1)*9
    rows = 9 
    #Have to call a function to get back all the category ids. Then merge all the responses to into 1. 
    categoryids = category_ids(catid)
    condition = "("
    for id in categoryids:
        condition += str(id) +","
    condition = condition[:-1]
    condition += ")"
    response = read("products",["uniqueID","name","price","productimage"],{"catid":condition},order = order,check = 1)
    finalresponse = check_response(response,start,rows)
    return finalresponse
 
#Will have to perform a DFS traversal of the tree to get all the catids   
def category_ids(catid):
    final = set()
    stack = [catid]
    while(len(stack) > 0):
        parentid = stack.pop()
        final.add(int(parentid))
        parentname = read("category",["categoryname"],{"catid":str(parentid)})[1][0][0]
        children = read("category",["catid"],{"parentname":parentname})[1]
        for child in children:
            stack.append(child[0])    
    return list(final)