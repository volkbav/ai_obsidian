import sys
import requests
import chromadb
from config import *

client = chromadb.Client()
collection = client.get_or_create_collection("notes")


def get_embedding(text):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": text
    })
    return response.json()["embedding"]


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