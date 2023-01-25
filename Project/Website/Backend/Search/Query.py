from flask import request
import requests ,json




#This will be able to search for products that have been passed as a query and will be re-routed to the Unbxd Search API. 
def query(pagenumber:int):
    searchquery = request.args.get('query')
    start = (int(pagenumber) - 1)*9
    rows = 9
    unbxdsearchAPI = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?q="
    finalquery = unbxdsearchAPI + searchquery + "&start=" + str(start) + "&rows=" + str(rows) + "&fields=" + "uniqueId,name,price,productImage"
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