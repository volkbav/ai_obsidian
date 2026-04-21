# search.py
import os
import sys
import requests
import chromadb

from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv('OLLAMA_URL')
MODEL = os.getenv('MODEL')
CHROMA_PATH = os.getenv('CHROMA_PATH')


client = chromadb.PersistentClient(path=CHROMA_PATH)
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
        print("\n---\n")
        print(format_results(results))


def format_results(results):
    output = []

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        filename = os.path.basename(meta["path"]).replace(".md", "")

        output.append(f"## [[{filename}]]\n")
        output.append(doc[:300] + "\n")

    return "\n".join(output)


if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    search(query)