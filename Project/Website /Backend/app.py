import json
from flask import Flask ,request, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    return json.dumps({'category':'hello world'},indent = 4)
    



@app.route("/products/details/<product_id>", methods=["GET"])
def details(productId):
    pass

if __name__ == "__main__":
    app.run(debug=True)