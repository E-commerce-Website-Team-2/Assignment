import sys
sys.path.append("..")
from Modules.Database import *
import requests,json


#Will be able to send the extra details that need to be sent when the product itself is clicked. 
def details(productId):
    response = readDB("products",["product_description"],{"uniqueId":productId})
    if response[1] == []:
        unbxdsearchAPI = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?q="
        finalquery = unbxdsearchAPI + str(productId) + "&fields=" + "productDescription"
        responseFromSearch = (requests.get(finalquery).content)
        responseFromSearch = json.loads(responseFromSearch) 
        return [str(responseFromSearch["response"]["products"][0]["productDescription"])]
    else:
        return response[1] 