import os
import requests
from tqdm import tqdm
import chromadb
from dotenv import load_dotenv
import hashlib

load_dotenv()

VAULT_PATH = os.getenv("VAULT_PATH")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))
OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("MODEL")
CHROMA_PATH = os.getenv("CHROMA_PATH")

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection("notes")


def get_embedding(text):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": text
        })
        return response.json()["embedding"]
    except Exception as e:
        print(f"Embedding error: {e}")
        return None


def chunk_text(text):
    step = max(1, CHUNK_SIZE - CHUNK_OVERLAP)
    return [text[i:i+CHUNK_SIZE] for i in range(0, len(text), step)]


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

            chunk_id = hashlib.sha256(
                (path + str(i) + chunk).encode()
            ).hexdigest()

            try:
                collection.add(
                    documents=[chunk],
                    embeddings=[embedding],
                    ids=[chunk_id],
                    metadatas=[{"path": path, "chunk": i}]
                )
            except Exception as e:
                print(f"Index error: {e}")


if __name__ == "__main__":
    index()