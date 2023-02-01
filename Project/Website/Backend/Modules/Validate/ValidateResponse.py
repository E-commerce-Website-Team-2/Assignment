import sys
sys.path.append("..")
#This will put the products that we have in the right format and also check if the page number given is valid or not 
def checkResponse(response,start,rows):
    numberofProducts = len(response[1])
    finalresponse = []
    #This means that the page number given is invalid
    if(numberofProducts < start):
        return [400,0]
    #This means that the products left to show are not more then 9.
    elif(numberofProducts < start + rows):
        finalresponse.append(200)
        finalresponse.append(numberofProducts)
        for product in response[1][start:start+rows]:
            finalresponse.append({"uniqueID":product[0],"name":product[1],"price":product[2],"productimage":product[3]})
        return finalresponse
    #This means that there are all products in the page that was given
    else:
        finalresponse.append(200)
        finalresponse.append(numberofProducts)
        for product in response[1][start:start+rows]:
            finalresponse.append({"uniqueID":product[0],"name":product[1],"price":product[2],"productimage":product[3]})
        return finalresponse