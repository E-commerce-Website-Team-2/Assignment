from datasets import Dataset
from transformers import AutoTokenizer, TFAutoModel
import pickle
import sys
import numpy as np
from scipy.sparse import csr_matrix
sys.path.append("..")
from Modules.database import *


def encode_bert():
    response = read("products",["uniqueid","name","price","product_description"])[1]
    products_df = pd.DataFrame(response, columns=["uniqueid","name","price","product_description"])
    products_df["text"] = products_df["name"] + " " + products_df["product_description"]
    products_dataset = Dataset.from_pandas(products_df)
    model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
    tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
    model = TFAutoModel.from_pretrained(model_ckpt, from_pt=True)
    print("I have started encoding")
    embeddings_dataset = products_dataset.map(lambda x: {"embeddings": get_embeddings(x["text"],tokenizer,model).numpy()[0]})
    embeddings_dataset.add_faiss_index(column="embeddings")
    pickle_out = open("/Modules/recommender/encoding.pkl","wb")
    pickle.dump(embeddings_dataset,pickle_out)


def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]


def get_embeddings(text_list,tokenizer,model):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="tf"
    )
    encoded_input = {k: v for k, v in encoded_input.items()}
    model_output = model(**encoded_input)
    return cls_pooling(model_output)

def encode_rating_matrix():
    ratings = read("ratings","*")[1]
    ratings = pd.DataFrame(ratings, columns =['userid', 'productid','rating'])
    n_ratings = len(ratings)
    n_products = len(ratings['productid'].unique())
    n_users = len(ratings['userid'].unique())
    X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix(ratings)
    scipy.sparse.save_npz("/Modules/recommender/encoding_matrix.npz",X)
    return "Succesfully encoded ratings and added them to database."


def create_matrix(df): 
    N = len(df['userid'].unique())
    M = len(df['productid'].unique())
    # Map Ids to indices
    user_mapper = dict(zip(np.unique(df["userid"]), list(range(N))))
    movie_mapper = dict(zip(np.unique(df["productid"]), list(range(M)))) 
    # Map indices to IDs
    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["userid"])))
    movie_inv_mapper = dict(zip(list(range(M)), np.unique(df["productid"])))
    user_index = [user_mapper[i] for i in df['userid']]
    movie_index = [movie_mapper[i] for i in df['productid']]
    X = csr_matrix((df["rating"], (movie_index, user_index)), shape=(M, N))
    return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper