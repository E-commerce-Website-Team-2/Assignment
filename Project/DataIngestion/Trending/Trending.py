from Database import *
from Validate import *



#This would be what is shown on the start when the page is loaded. At the moment its a call to get all the products in the database. 
def trending(pagenumber):
    start = (int(pagenumber) - 1)*9
    rows = 9
    response = readDB("products",["uniqueID","name","price","productimage"])
    finalresponse = checkResponse(response,start,rows)
    return finalresponse



# This will be part of the API that will be able to load the trending items that are meant to be shown when 
# the user visits the website. Has not been implemeneted in either side. 
def settrending():
    pass

