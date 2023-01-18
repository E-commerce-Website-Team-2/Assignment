from flask import Flask ,request, jsonify, request
app = Flask(__name__)


@app.route('/products/search', methods=["GET"])
def query():
    searchquery = request.args.get('query')
    unbxdsearchAPI = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?q="
    finalquery = unbxdsearchAPI + searchquery
    responseFromSearch = request.get(finalquery).content
    


@app.route('/products/category', methods=["GET"])
def category():
    pass




@app.route('/products/trending', methods=["GET"])
def trending():
    pass


@app.route('/products/getcategory', methods = ["GET"])
def getcategory():
    pass



@app.route('/products/details/</product-id>', methods=["GET"])
def details(productId):
    pass