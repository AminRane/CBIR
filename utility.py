import os
import numpy as np 
import joblib
from PIL import Image
import io
from keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient 


CLIENT = MongoClient('mongodb://localhost:27017/')
DB = CLIENT['CBIR']
ENCODER = load_model('models\\encoder.h5')
KMEANS = joblib.load('models\\kmeans.pkl')


def get_image_embedding(content):
    img = Image.open(io.BytesIO(content))
    img = img.resize((299, 299))  
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return ENCODER.predict(img_array) 


def query_similar_images(content, top_k=10):

    query_embedding = get_image_embedding(content)
    print(query_embedding.shape)

    query_cluster_index = int(KMEANS.predict(query_embedding)[0])
    print(query_cluster_index)

    # Retrieve embeddings from the same cluster
    cluster_data = DB.image_embeddings.find({'cluster_index': query_cluster_index}, {'image_path': 1, 'embedding_vector': 1})
    # Extract _id and embedding_vector into separate lists
    cluster_paths = []
    cluster_embeddings = []

    for doc in cluster_data:
        cluster_paths.append(doc['image_path'])
        cluster_embeddings.append(doc['embedding_vector'])

    # Calculate cosine similarity between the query embedding and all embeddings in the cluster
    similarities = cosine_similarity(query_embedding.reshape(1, -1), cluster_embeddings)

    # Get indices of top-k similar images
    top_k_indices = similarities.argsort()[0][-top_k:][::-1]

    similar_images = [cluster_paths[_] for _ in top_k_indices]

    return similar_images


