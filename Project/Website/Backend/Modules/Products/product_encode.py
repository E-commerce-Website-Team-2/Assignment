from sentence_transformers import SentenceTransformer
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

