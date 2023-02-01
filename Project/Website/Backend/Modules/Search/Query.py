from flask import request
import requests ,json

import sys
sys.path.append("..")


#This will be able to search for products that have been passed as a query and will be re-routed to the Unbxd Search API. 
def query(pagenumber:int):
    searchquery = request.args.get('query')
    order = request.args.get('sort')
    if(order == None or order == ""):
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
    ordering = ""
    if(order == 1):
        ordering = "price asc"
    elif(order == 2):
        ordering = "price desc"
    unbxdsearchAPI = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?q="
    finalquery = unbxdsearchAPI + searchquery + "&start=" + str(start) + "&rows=" + str(rows) + "&fields=" + "uniqueId,name,price,productImage" + "&sort=" + ordering
    responseFromSearch = (requests.get(finalquery).content)
    responseFromSearch = json.loads(responseFromSearch)
    #Pagination has been carried out by using a page number as a variable in the URL 
    final = [responseFromSearch["response"]["numberOfProducts"]]
    if(start > final[0]):
        return [400,0,{}]
    if(final[0] == 0):
        return [400,0,{}]
    final = [200] + final + responseFromSearch["response"]["products"]
    return final