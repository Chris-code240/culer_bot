import os
import chromadb
from chromadb.utils import embedding_functions

hf_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

CHROMA_CLIENT = chromadb.Client()
COLLECTION = CHROMA_CLIENT.get_or_create_collection(
    name="barca",
    embedding_function=hf_ef
)

results = COLLECTION.query(
    query_texts=["Who is Barcelona's all-time top scorer?"],
    n_results=2
)
print(results)

