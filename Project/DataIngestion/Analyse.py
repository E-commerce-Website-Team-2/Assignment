#This file has been created in the start of the project to study the many different 
#attributes that we have receieved as part of the search API and the out.json file that we received as data
import json 
with open('out.json', 'r') as fcc_file:
    fcc_data = json.load(fcc_file)
    x = 0
    categories = set()
    size = set()
    color = set()
    gender = set()
    final = set()
    catlevel1  = set()
    catlevel2 = set()
    catlevelmen = set()
    catlevelwomen = set()
    catlevelexp = set()
    missing = 0
    for i in fcc_data:
        x = x + 1
        for j in i.keys():
            final.add(j)
        for j in i['category']:
            categories.add(j)
        for j in i['color']:
            color.add(j)
        for j in i['gender']:
            gender.add(j)
        if('size' in i.keys()):
            for j in i['size']:
                size.add(j);
        else:
            #print(i['name'])
            y = 0
        if(i['name'] != i['title']):
            #print("Case")
            z = 0
        catlevel1.add(i['catlevel1Name'])
        if('catlevel2Name' in i.keys()):
            catlevel2.add(i['catlevel2Name'])
        else:
            missing += 1
            #print("I am missing the data for catlevel2 in ",i['uniqueId'])
    #print("I am missing total catlevel2Name in ",missing)
        if(i['catlevel1Name'] == "men"):
            if('catlevel2Name' in i.keys()):
                catlevelmen.add(i['catlevel2Name'])
        if(i['catlevel1Name'] == "women"):
            if('catlevel2Name' in i.keys()):
                catlevelwomen.add(i['catlevel2Name'])
        if(i['catlevel1Name'] == "exp"):
            if('catlevel2Name' in i.keys()):
                catlevelexp.add(i['catlevel2Name'])
    x =  0
    for i in final:
        x += 1
        #print(i)
    #print(x)
    x = 0
    for i in fcc_data[7]:
        x += 1
        #print(i,fcc_data[7][i])
    #print(x)
    #print(len(categories),fcc_data[0]['category'])
    # print("This is category level 1",catlevel1)
    # print("----------------------------------------")
    # print("This is category level 2",catlevel2,".")
    # print("----------------------------------------")
    # print(" There are ",len(catlevel2)," in the second category")
    # print("Now we will be building the category tree to link the both of them")
    # print("This is for the men ",len(catlevelmen))
    # print(catlevelmen)
    # print("This is for the women",len(catlevelwomen))
    # print(catlevelwomen)
    # print("This is for the exp")
    # print(catlevelexp)
    # print("Cateogries that is an intersection between men and women ")
    # print(catlevelmen.intersection(catlevelwomen))"
    # print(type(fcc_data[3]['price']))
