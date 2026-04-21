import os
import sys
import requests
import chromadb
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("MODEL")
CHROMA_PATH = os.getenv("CHROMA_PATH")

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection("notes")


def get_embedding(text):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": text
    })
    return response.json()["embedding"]


def format_results(results):
    output = []

    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        filename = os.path.basename(meta["path"]).replace(".md", "")

        output.append(f"## [[{filename}]] (score: {dist:.3f})\n")
        output.append(doc[:300] + "\n")

    return "\n".join(output)


def search(query):
    embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=5
    )

    if not results.get("documents") or not results["documents"][0]:
        print("No results found")
        return

    print(format_results(results))


if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    search(query)