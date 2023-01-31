from Database import *
from flask import  request


#Will be able to load the category tree based on the category id passed to it and send back a JSON to the front-end
def getcategory():
    category = request.args.get('cat')
    #To get a level 1 call we will use None. 
    if(category == None):
        categories = readDB("category",["catid","categoryname"],{"parentname":"None"})
        for i in range(len(categories[1])):
            categories[1][i] = list(categories[1][i])
        return categories
    catid = readDB("category",["categoryname"],{"catid":category})
    catid = catid[1][0][0]
    categories = readDB("category",["catid","categoryname"],{"parentname":catid})
    for i in range(len(categories[1])):
        categories[1][i] = list(categories[1][i])
    return categories



#This will be the part of the API that will be able to add/update the category table. We will be expecting data 
#to be given in the following format. {"catLevel1":["List of all"] "catlevel2:["List of all"]}
def categoryTree():
    if request.method == "POST":
        data = request.get_json()
        final_response = ""
        for category in data:
            level1status  = writeCategoryLevel1(list(category.keys())[0],"category",[])
            if(level1status == 200):
                final_response += "The category " + list(category.keys())[0] + " has been added \n"
                for categories in category[list(category.keys())[0]]:
                    level2status = writeCategoryLevel2(list(category.keys())[0],categories,"category")
                    if(level2status != 200):
                        final_response += "The category " + list(category.keys())[0] + " Sub-category " + categories + " Failed due to database error. Please retry.\n"
                    else:
                        final_response += "The category " + list(category.keys())[0] + " Sub-category " + categories + " Has been added.\n"
            else:
                final_response += "The " + list(category.keys())[0] + " has failed due to database error. \n"
        return final_response