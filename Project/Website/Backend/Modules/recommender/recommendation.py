from Modules.database import *
from Modules.validate import *
from sentence_transformers import SentenceTransformer, util
import numpy as np
import torch 
import heapq

#This function is responsible for running a similarity check between the given productID and return the top 5 products
def recommend(productId):
    current_encoding = read("encoding",["uniqueid","name_encoding","product_encoding"],{"uniqueid":productId})
    name_current_encoding = current_encoding[1][0][1]
    product_current_encoding = current_encoding[1][0][2]
    current_id = current_encoding[1][0][0]
    name_embeddings = read("encoding",["name_encoding"])[1]
    product_embeddings = read("encoding",["product_encoding"])[1]
    for embedding in range(len(name_embeddings)):
        name_embeddings[embedding] = torch.from_numpy(np.array(name_embeddings[embedding],dtype="float64"))
        product_embeddings[embedding] = torch.from_numpy(np.array(product_embeddings[embedding],dtype="float64"))
    uniqueIds = read("encoding",["uniqueid"])[1]
    top_products = []
    #We have now loaded all the embeddings to run a similarity metric against them all to now get a score. 
    #Embeddings is now a list of all the products and their embeddings. 
    for product in range(len(uniqueIds)):
        if(uniqueIds[product] == current_id):
            continue
        cosine_scores_name = util.cos_sim(torch.from_numpy(np.array(name_current_encoding,dtype="float64")), name_embeddings[product])
        score_name = (cosine_scores_name.numpy()).tolist()[0]
        cosine_scores_desc = util.cos_sim(torch.from_numpy(np.array(product_current_encoding,dtype="float64")), product_embeddings[product])
        score_desc = (cosine_scores_desc.numpy()).tolist()[0]
        id = uniqueIds[product]
        score = 0.6*score_desc[0] + 0.4*score_name[0]
        if(len(top_products) < 4):
            heapq.heappush(top_products,[score,id])
        else:
            #Check if the score is greater then the minimum
            if(score > top_products[0][0]):
                #If it is greater, remove the minimum element and add this element.
                heapq.heappop(top_products)
                heapq.heappush(top_products,[score,id])
    recommended_products = "("
    for product in top_products:
        recommended_products += "'" + product[1][0] + "'" + ","
    recommended_products = recommended_products[:-1]
    recommended_products += ")"
    response = read("products",["uniqueID","name","price","productimage"],{"uniqueid":recommended_products},check = 1)
    finalresponse = check_response(response,0,4)
    return finalresponse

    
    
