from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
import sys
sys.path.append("..")
from Modules.database import *


# I am loading all products of the database and will attempt 
# to create an embedding for the sentence and then the name of the product
def product_encoding(product):        
    bert_embedding = SentenceTransformer('bert-base-nli-mean-tokens')
    name_embeddings = bert_embedding.encode(product["name"])
    product_embeddings = bert_embedding.encode(product["productDescription"])
    encoding = {"uniqueID":product["uniqueId"],"name_encoding":name_embeddings,"product_encoding":product_embeddings}
    status = writeEncoding(encoding,"encoding")
    return status

def product_encoding_count_vectorizer():
    name = list(read("products",["name"])[1])
    name_encode = []
    desc_encode = []
    id = read("products",["uniqueid"])[1]
    ids = []
    description = list(read("products",["product_description"])[1])
    for product in range(len(id)):
        name_encode.append(name[product][0])
        desc_encode.append(description[product][0])
        ids.append(id[product][0])
    vectorizer = CountVectorizer()
    vectorizer.fit(name_encode)
    name_vector = vectorizer.transform(name_encode)
    vectorizer1 = CountVectorizer()
    vectorizer1.fit(desc_encode)
    desc_vector = vectorizer1.transform(desc_encode)
    name_vector = (name_vector.toarray()).tolist()
    desc_vector = (desc_vector.toarray()).tolist()
    for product in range(len(id)):
        encoding = {}
        encoding["name_encoding"] = name_vector[product]
        encoding["product_encoding"] = desc_vector[product]
        encoding["uniqueID"] = ids[product]
        status = writeEncoding_vectorizer(encoding,"encoding_vectorizer")
    return 
