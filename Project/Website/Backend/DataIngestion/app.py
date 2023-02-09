import os
import psycopg2
from flask import Flask, request,url_for,redirect
import sys
sys.path.append("..")
from Modules.category  import *
from Modules.database import *
from Modules.products import *
from Modules.search import *
from Modules.trending import *
from Modules.validate import *


app = Flask(__name__)


#This is the main API function that will be called with a POST HTTP request when needed to add products into the database
@app.route('/products',methods = (['POST']))
def products_caller():
    return products()


#This will be the part of the API that will be able to add/update the category table. We will be expecting data 
#to be given in the following format. {"catLevel1":["List of all"] "catlevel2:["List of all"]}
@app.route('/category',methods = (['POST']))
def category_tree_caller():
    return category_tree()


# This will be part of the API that will be able to load the trending items that are meant to be shown when 
# the user visits the website. Has not been implemeneted in either side. 
@app.route('/trending',methods = (['POST']))
def set_trending_caller():
    return set_trending()



app.run(debug=True, host="0.0.0.0", port=6000)


