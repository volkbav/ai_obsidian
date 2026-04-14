import os
import requests
from tqdm import tqdm
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


def chunk_text(text):
    chunks = []
    for i in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP):
        chunks.append(text[i:i + CHUNK_SIZE])
    return chunks


def load_notes():
    notes = []
    for root, _, files in os.walk(VAULT_PATH):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    notes.append((path, f.read()))
    return notes


def index():
    notes = load_notes()

    for path, content in tqdm(notes):
        chunks = chunk_text(content)

        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)

            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[f"{path}_{i}"],
                metadatas=[{"path": path}]
            )


if __name__ == "__main__":
    index()