from Database import *
from flask import  request


#Will be able to load the entire category tree and send back a JSON to the front-end
def getcategory():
    final = {}
    table1 = readDB('categorylevel1',"*")
    #This would have read the table that stores category level 1. 
    if(table1[0] == 200):
        for level1 in table1[1]:
            catlevel1 = level1[0]
            table2 = readDB("categorylevel2",["catlevel2"],{"catlevel1":catlevel1})
            catlevel2 = table2[1]
            for i in range(len(catlevel2)):
                catlevel2[i] = catlevel2[i][0]
            final[catlevel1] = catlevel2
    return final



#This will be the part of the API that will be able to add/update the category table. We will be expecting data 
#to be given in the following format. {"catLevel1":["List of all"] "catlevel2:["List of all"]}
def categoryTree():
    if request.method == "POST":
        data = request.get_json()
        final_response = ""
        for category in data:
            level1status  = writeCategoryLevel1(list(category.keys())[0],"CategoryLevel1",[])
            if(level1status == 200):
                final_response += "The category " + list(category.keys())[0] + " has been added \n"
                for categories in category[list(category.keys())[0]]:
                    level2status = writeCategoryLevel2(list(category.keys())[0],categories,"CategoryLevel2")
                    if(level2status != 200):
                        final_response += "The category " + list(category.keys())[0] + " Sub-category " + categories + " Failed due to database error. Please retry.\n"
                    else:
                        final_response += "The category " + list(category.keys())[0] + " Sub-category " + categories + " Has been added.\n"
            else:
                final_response += "The " + list(category.keys())[0] + " has failed due to database error. \n"
        return final_response