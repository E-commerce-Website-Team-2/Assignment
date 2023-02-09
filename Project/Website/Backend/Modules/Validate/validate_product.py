import sys
sys.path.append("..")
from Modules.database import check_id


#This function will be able to validate any product that comes as input to the catalog. It will check if all the 
# necessary features are provided and if these features are valid or not. It will also check if the product is 
# being updated or a new one. The documentation explaining the meaning behind each error code will be given
def validate(product):
    string = "<class 'str'>"
    required = ['uniqueId','name','price','productDescription','catlevel1Name','catlevel2Name','productImage']
    if(all(x in list(product.keys()) for x in required)):
        pass
    else:
        missingFeatures = set(required) - set(list(product.keys()))
        error  = ""
        for i in missingFeatures:
            error += " " + i
        return [301,error]
    if(str(type(product['price'])) not in ["<class 'float'>","<class 'int'>","<class 'double'>"]) :
        return [302,"Price feature is wrong"]
    if(str(type(product['name'])) != string):
        return [303,"Name feature is wrong"]
    if(str(type(product['uniqueId'])) != string):
        return [304,"Unique Id is specified wrongly"]
    if(str(type(product['productDescription'])) != string):
        return [305,"Product Description is wrong"]
    if(str(type(product['productImage'])) != string):
        return [306,"Product Image is wrong"]
    if(str(type(product['catlevel1Name'])) != string):
        return [307,"Category Level 1 is wrong"]
    if(str(type(product['catlevel2Name'])) != string):
        return [308,"Category Level 2 is wrong"]
    flag = check_id(product['uniqueId'],"products")
    return [flag,"Good for database"]   

