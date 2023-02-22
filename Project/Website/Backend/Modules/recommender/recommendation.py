from Modules.database import *
from Modules.validate import *
from Modules.recommender.encode import *
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer,TFAutoModel
import numpy as np
import torch 
import heapq
import pandas as pd
import sys
from datasets import Dataset
import random 
from flask import request
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from scipy.sparse import load_npz
sys.path.append("..")




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

    




#This function will be responsibile for implementing Approximate Nearest Neighbours to the BERT encodings
def recommend_ANN(productId):
    embeddings_dataset = pd.read_pickle("Modules/recommender/encoding.pkl")
    for product in range(len(embeddings_dataset)):
        if(embeddings_dataset[product]["uniqueid"] == productId):
            question_embedding = np.array(embeddings_dataset[product]["embeddings"])
    scores, samples = embeddings_dataset.get_nearest_examples("embeddings",question_embedding, k=5)
    samples_df = pd.DataFrame.from_dict(samples)
    samples_df["scores"] = scores
    samples_df.sort_values("scores", ascending=False, inplace=True)
    recommended_products = "("
    for id in samples_df["uniqueid"].tolist():
        if(id != productId):
            recommended_products += "'" + id + "'" + ","
    recommended_products = recommended_products[:-1]
    recommended_products += ")"
    response = read("products",["uniqueID","name","price","productimage"],{"uniqueid":recommended_products},check = 1)
    finalresponse = check_response(response,0,4)
    return finalresponse



#This function will be able to load the matrix stored in the 
def user_specific_recommendation(productId):
    ratings = read("ratings","*")[1]
    ratings = pd.DataFrame(ratings, columns =['userid', 'productid','rating'])
    N = len(ratings['userid'].unique())
    M = len(ratings['productid'].unique())
    user_mapper = dict(zip(np.unique(ratings["userid"]), list(range(N))))
    product_mapper = dict(zip(np.unique(ratings["productid"]), list(range(M)))) 
    user_inv_mapper = dict(zip(list(range(N)), np.unique(ratings["userid"])))
    product_inv_mapper = dict(zip(list(range(M)), np.unique(ratings["productid"])))
    X = load_npz('Modules/recommender/encoding_matrix.npz')
    #Now based on the CSR matrix have to learn how to give a recommendation. 
    k = 4
    neighbour_ids = []
    product_ind = product_mapper[productId]
    product_vec = X[product_ind]
    k+=1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric='cosine')
    kNN.fit(X)
    product_vec = product_vec.reshape(1,-1)
    neighbour = kNN.kneighbors(product_vec, return_distance=False)
    for i in range(0,k):
        n = neighbour.item(i)
        neighbour_ids.append(product_inv_mapper[n])
    neighbour_ids.pop(0)
    recommended_products = "("
    for id in neighbour_ids:
        if(id != productId):
            recommended_products += "'" + id + "'" + ","
    recommended_products = recommended_products[:-1]
    recommended_products += ")"
    response = read("products",["uniqueID","name","price","productimage"],{"uniqueid":recommended_products},check = 1)
    finalresponse = check_response(response,0,4)
    return finalresponse
    #Now based on the CSR matrix have to learn how to give a recommendation. 
    


# #This function is only called once and then will be commented. This would generate random data and populate the database with ratings. 
# def user_rating_generation():
#     productIds = read("products",["uniqueid"])
#     if(productIds[0] == 200):
#         productIds = productIds[1]
#         productIds = sum(productIds,())
#         number_of_products = len(productIds)
#         #Now I have to generate a random product that the user will rate. I have to also randomize the number of products that are being ordered. 
#         for user in range(10000):
#             #This would be the number of products that the user will rate
#             rating_products_count = random.randint(4,8)
#             all_products = []
#             for product in range(rating_products_count):
#                 #This would be the index of the productId that the user is going to rate. 
#                 index = random.randint(0,number_of_products-1)
#                 while(index in all_products):
#                     index = random.randint(0,number_of_products-1)
#                 all_products.append(index)
#                 product_id = productIds[index]
#                 #This would be the rating that the product is being given. 
#                 rating = random.randint(1,5)
#                 #Now we should create a dictionary of this rating so that we can load it into the database
#                 product_rating = {"userid":user,"productid":product_id,"rating":rating}
#                 status = write_product_rating(product_rating,"ratings")
#                 if(status != 200):
#                     print("Could not add record. Error in write function.")
#         return "Successfully added random ratings into the database"
#     else:
#         return "Couldnt read the database. Please retry after some time"


#This function will be able to add ratings that are passed in a json to the database and will encode the similarity matrix with the records in the database 
def user_rating_generation():
    #First add a record into the database.
    data = request.get_json()
    for rating in data:
        status = write_product_rating(rating,"ratings")
        if(status != 200):
            return "Could not add encoding due to database error"
    #Then call the encoding function to re-encode and store a pickle file so that we can recommend products
    return encode_rating_matrix()




