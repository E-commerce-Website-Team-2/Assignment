from flask import Flask ,request
from flask_cors import CORS
from flask_caching import Cache
import psycopg2,requests,json
from Database import *
from Validate import *
from Category import *
from Products import *
from Trending import *
from Search import *


app = Flask(__name__)
CORS(app)
app.config.from_object('config.BaseConfig') 
cache = Cache(app) 


#This will be able to search for products that have been passed as a query and will be re-routed to the Unbxd Search API. 
@app.route('/products/search/<pagenumber>', methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def querycaller(pagenumber:int):
    return query(pagenumber)

#This will be able perform category filtering and will return products with an exact match. 
@app.route('/products/category/<pagenumber>', methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def categorycaller(pagenumber):
    return category(pagenumber)


#This would be what is shown on the start when the page is loaded. At the moment its a call to get all the products in the database. 
@app.route('/products/trending/<pagenumber>', methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def trendingcaller(pagenumber):
    return trending(pagenumber)


#Will be able to load the entire category tree and send back a JSON to the front-end
@app.route('/products/categorytree', methods = ["GET"])
@cache.cached(timeout=30, query_string=True)
def categorytreecaller():
    return getcategory()


#Will be able to send the extra details that need to be sent when the product itself is clicked. 
@app.route('/products/details/<productId>', methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def detailscaller(productId):
    return details(productId)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)