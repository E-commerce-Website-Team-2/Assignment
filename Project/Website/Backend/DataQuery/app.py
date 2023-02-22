from flask import Flask ,request
from flask_cors import CORS
from flask_caching import Cache
import psycopg2
import requests
import json
import sys
sys.path.append("..")
from Modules.category  import *
from Modules.database import *
from Modules.products import *
from Modules.search import *
from Modules.trending import *
from Modules.validate import *
from Modules.recommender import *


app = Flask(__name__)
CORS(app)
app.config.from_object('config.BaseConfig') 
cache = Cache(app) 


#This will be able to search for products that have been passed as a query and will be re-routed to the Unbxd Search API. 
@app.route('/products/search/<searchquery>/<pagenumber>/<sort>', methods=["GET"])
@app.route('/products/search/<searchquery>/<pagenumber>/', methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def query_caller(searchquery,pagenumber:int,sort=""):
    return query(searchquery,sort,pagenumber)

#This will be able perform category filtering and will return products with an exact match. 
@app.route('/products/category/<categoryid>/<pagenumber>/<sort>', methods=["GET"])
@app.route('/products/category/<categoryid>/<pagenumber>/', methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def category_caller(pagenumber,categoryid,sort=""):
    return category(pagenumber,categoryid,sort)


#This would be what is shown on the start when the page is loaded. At the moment its a call to get all the products in the database. 
@app.route('/products/trending/<pagenumber>/<sort>', methods=["GET"])
@app.route('/products/trending/<pagenumber>/', methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def trending_caller(pagenumber,sort=""):
    return trending(pagenumber,sort)


#Will be able to load the entire category tree and send back a JSON to the front-end
@app.route('/category/<categoryid>/tree', methods = ["GET"])
@app.route('/category/tree', methods = ["GET"])
@cache.cached(timeout=30, query_string=True)
def category_tree_caller(categoryid=None):
    return get_category(categoryid)


#Will be able to send the extra details that need to be sent when the product itself is clicked. 
@app.route('/products/<productId>/details', methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def details_caller(productId):
    return details(productId)

@app.route('/products/<productId>/recommendation/similar',  methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def recommended_similar(productId):
    #return recommend(productId)
    return recommend_ANN(productId)

@app.route('/products/<productId>/recommendation/liked',  methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def recommended_user(productId):
    #return recommend(productId)
    return user_specific_recommendation(productId)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)