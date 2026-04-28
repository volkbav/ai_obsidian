import os
import requests
from tqdm import tqdm
import chromadb
from dotenv import load_dotenv
import hashlib

load_dotenv()

VAULT_PATH = os.getenv("VAULT_PATH")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))
OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("MODEL")
CHROMA_PATH = os.getenv("CHROMA_PATH")

EXCLUDE_DIRS = set(
    d.strip() for d in os.getenv("EXCLUDE_DIRS", "").split(",") if d.strip()
)

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection("notes")


# ---------- EMBEDDING ----------
def get_embedding(text):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": text
        })
        return response.json().get("embedding")
    except Exception as e:
        print(f"Embedding error: {e}")
        return None


# ---------- CHUNKING ----------
def chunk_text(text):
    step = max(1, CHUNK_SIZE - CHUNK_OVERLAP)
    return [text[i:i+CHUNK_SIZE] for i in range(0, len(text), step)]


# ---------- FILE HASH ----------
def file_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


# ---------- LOAD NOTES ----------
def load_notes():
    notes = []

    for root, dirs, files in os.walk(VAULT_PATH):

        # 🔥 фильтруем папки ДО обхода
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                notes.append((path, content))

    return notes


# ---------- CHECK IF FILE CHANGED ----------
def is_file_changed(path: str, content_hash: str) -> bool:
    result = collection.get(
        where={"path": path},
        include=["metadatas"]
    )

    if not result["metadatas"]:
        return True

    for meta in result["metadatas"]:
        if meta.get("file_hash") == content_hash:
            return False

    return True


# ---------- INDEX ----------
def index():
    notes = load_notes()

    for path, content in tqdm(notes):
        content_hash = file_hash(content)

        # 🔥 SKIP IF NOT CHANGED
        if not is_file_changed(path, content_hash):
            continue

        chunks = chunk_text(content)

        for i, chunk in enumerate(chunks):
            chunk = f"{filename}\n\n{chunk}"
            
            embedding = get_embedding(chunk)

            if embedding is None:
                continue

            chunk_id = hashlib.sha256(
                (path + str(i) + chunk).encode()
            ).hexdigest()

            try:
                collection.add(
                    documents=[chunk],
                    embeddings=[embedding],
                    ids=[chunk_id],
                    metadatas=[{
                        "path": path,
                        "chunk": i,
                        "file_hash": content_hash
                    }]
                )
            except Exception as e:
                print(f"[INDEX ERROR] {path} chunk={i}: {e}")


if __name__ == "__main__":
    index()