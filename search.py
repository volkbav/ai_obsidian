import sys
import requests
import chromadb
from config import *
from index import (
    OLLAMA_URL,
    MODEL
)

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("notes")


def get_embedding(text):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": text  # Изменено с "input" на "prompt"
    })
    return response.json()["embedding"]  # Убран [0], так как embedding уже вектор


def search(query):
    embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=5
    )

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print("\n---")
        print(meta["path"])
        print(doc[:300])


if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    search(query)