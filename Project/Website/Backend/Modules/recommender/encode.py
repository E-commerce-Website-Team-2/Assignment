from datasets import Dataset
from transformers import AutoTokenizer, TFAutoModel
import pickle
import sys
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