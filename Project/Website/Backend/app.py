from flask import Flask ,request
from flask_cors import CORS
import psycopg2,requests,json
from Database import *
from Validate import *
from Category import *
from Products import *
from Trending import *
from Search import *


app = Flask(__name__)
CORS(app)


#This will be able to search for products that have been passed as a query and will be re-routed to the Unbxd Search API. 
@app.route('/products/search/<pagenumber>', methods=["GET"])
def querycaller(pagenumber:int):
    return query(pagenumber)

#This will be able perform category filtering and will return products with an exact match. 
@app.route('/products/category/<pagenumber>', methods=["GET"])
def categorycaller(pagenumber):
    return category(pagenumber)


#This would be what is shown on the start when the page is loaded. At the moment its a call to get all the products in the database. 
@app.route('/products/trending/<pagenumber>', methods=["GET"])
def trendingcaller(pagenumber):
    trending(pagenumber)


#Will be able to load the entire category tree and send back a JSON to the front-end
@app.route('/products/getcategory', methods = ["GET"])
def getcategorycaller():
    return getcategory()


#Will be able to send the extra details that need to be sent when the product itself is clicked. 
@app.route('/products/details/<productId>', methods=["GET"])
def detailscaller(productId):
    return details(productId)


app.run()